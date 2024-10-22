import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from app.main import app  # Asegúrate de que el nombre de tu archivo sea correcto

# Crear un cliente de prueba para FastAPI
client = TestClient(app)


@pytest.fixture
def mock_db_session():
    """Fixture para simular la sesión de la base de datos."""
    # Crear un objeto MagicMock que simule la sesión de la base de datos
    mock_session = MagicMock()

    # Simular el comportamiento del método query().filter().first()
    mock_session.query.return_value.filter.return_value.first.return_value = None  # Simula que no hay departamentos existentes

    yield mock_session
    # Aquí podrías limpiar o realizar otras acciones si fuera necesario.


@patch('app.main.get_db')
def test_upload_departments(mock_get_db, mock_db_session):
    """Test para la función de carga de departamentos."""
    # Asignar el mock de sesión al retorno de get_db
    mock_get_db.return_value = mock_db_session

    # Crear un archivo CSV simulado
    csv_file = ('test.csv', b"1,Test Department\n2,Another Department")

    # Hacer una solicitud POST a la ruta
    response = client.post("/upload_departments/", files={"file": csv_file})

    # Verificar la respuesta
    assert response.status_code == 200
    assert response.json() == {"status": "Departments uploaded successfully"}

    # Comprobar que se ha añadido un departamento
    assert mock_db_session.add.call_count == 2  # Se deberían añadir 2 departamentos
    mock_db_session.commit.assert_called_once()  # Se debería haber llamado a commit una vez


@patch('app.main.get_db')
def test_upload_departments_existing_id(mock_get_db, mock_db_session):
    """Test para la función de carga de departamentos con ID existente."""
    # Simular que ya existe un departamento con ID 1
    mock_session = MagicMock()
    existing_department = MagicMock()
    mock_session.query.return_value.filter.return_value.first.return_value = existing_department
    mock_get_db.return_value = mock_session

    # Crear un archivo CSV simulado
    csv_file = ('test.csv', b"1,Test Department\n2,Another Department")

    # Hacer una solicitud POST a la ruta
    response = client.post("/upload_departments/", files={"file": csv_file})

    # Verificar la respuesta
    assert response.status_code == 400  # Esperamos un error por ID existente
    assert "Error: Department ID might already exist." in response.json()['detail']
