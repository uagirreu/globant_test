from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db import SessionLocal
import app.models as models
from app.sql_querys import GET_EMPLOYEES_BY_QUARTER, GET_DEPARTMENTS_ABOVE_AVERAGE

app = FastAPI()

# Dependencia para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Función para cargar CSV de departamentos
@app.post("/upload_departments/")
async def upload_departments(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Leer el CSV
        df = pd.read_csv(file.file, header=None)

        # Asignar nombres de columnas manualmente
        df.columns = ['id', 'department']

        # Imprimir el DataFrame para depuración
        print(df)

        # Iterar sobre cada fila del DataFrame
        for index, row in df.iterrows():
            # Crear un nuevo departamento
            department = models.Department(id=row['id'], department=row['department'])
            db.add(department)

        db.commit()  # Confirmar la transacción
        return {"status": "Departments uploaded successfully"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error: Department ID might already exist.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error uploading department: {str(e)}")


# Función para cargar CSV de trabajos
@app.post("/upload_jobs/")
async def upload_jobs(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # Leer el CSV sin cabeceras
        df = pd.read_csv(file.file, header=None)

        # Asignar nombres de columnas manualmente
        df.columns = ['id', 'job']

        # Imprimir el DataFrame para depuración
        print(df)

        # Iterar sobre cada fila del DataFrame
        for index, row in df.iterrows():
            # Crear un nuevo trabajo
            job = models.Job(id=row['id'], job=row['job'])
            db.add(job)

        db.commit()  # Confirmar la transacción
        return {"status": "Jobs uploaded successfully"}

    except IntegrityError:
        db.rollback()  # Revertir en caso de error
        raise HTTPException(status_code=400, detail="Error: Job IDs might already exist.")
    except Exception as e:
        db.rollback()  # Revertir en caso de error
        raise HTTPException(status_code=400, detail=f"Error uploading jobs: {str(e)}")


@app.post("/upload_employees/")
async def upload_employees(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(file.file, header=None)
        employees_to_add = []
        batch_size = 100  # Puedes ajustar este tamaño según sea necesario
        default_date = pd.to_datetime('2000-01-01')  # Fecha por defecto si no hay fecha

        for index, row in df.iterrows():
            # Rellena los valores nulos con 1 para department_id y job_id
            department_id = row[3] if pd.notna(row[3]) else 1
            job_id = row[4] if pd.notna(row[4]) else 1

            # Asigna nombre como None si es nulo
            name = row[1] if pd.notna(row[1]) else None

            # Asigna fecha como None si es nulo, o a la fecha por defecto
            employee_date = pd.to_datetime(row[2]) if pd.notna(row[2]) else default_date

            # Crear un nuevo empleado
            employee = models.Employee(
                id=int(row[0]),  # Asegúrate de convertir a int
                name=name,
                datetime=employee_date,
                department_id=int(department_id),
                job_id=int(job_id)
            )
            employees_to_add.append(employee)

            # Realiza un commit cada 'batch_size' empleados
            if len(employees_to_add) >= batch_size:
                try:
                    db.add_all(employees_to_add)
                    db.commit()
                except Exception as e:
                    db.rollback()
                    print(f"Error en la inserción de lote: {e}")
                    raise HTTPException(status_code=400, detail=f"Error en la inserción de empleados en lote: {str(e)}")
                employees_to_add = []  # Reinicia la lista

        # Inserta cualquier empleado restante
        if employees_to_add:
            try:
                db.add_all(employees_to_add)
                db.commit()
            except Exception as e:
                db.rollback()
                print(f"Error en la inserción de lote final: {e}")
                raise HTTPException(status_code=400,
                                    detail=f"Error en la inserción de empleados en lote final: {str(e)}")

        return {"status": "Employees uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error uploading employees: {str(e)}")

@app.get("/employees_by_quarter/")
def get_employees_by_quarter(db: Session = Depends(get_db)):
    results = db.execute(GET_EMPLOYEES_BY_QUARTER).fetchall()

    return [{"department": row[0], "job": row[1], "Q1": row[2], "Q2": row[3], "Q3": row[4], "Q4": row[5]} for row in results]

@app.get("/departments_hiring_above_average/")
def get_departments_above_average(db: Session = Depends(get_db)):
    results = db.execute(GET_DEPARTMENTS_ABOVE_AVERAGE).fetchall()

    return [{"id": row[0], "department": row[1], "hired": row[2]} for row in results]
