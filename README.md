# API para Gestión de Empleados

Este proyecto es una API RESTful construida con FastAPI y SQLAlchemy para gestionar empleados, departamentos y trabajos. Permite cargar datos desde archivos CSV y consultar métricas específicas.

## Requisitos

- Python 3.7+
- FastAPI
- SQLAlchemy
- pandas
- pyodbc
- Uvicorn

## Endpoints
Cargar Departamentos
POST /upload_departments/ - Carga un archivo CSV de departamentos.
Cargar Empleados
POST /upload_employees/ - Carga un archivo CSV de empleados.
Métricas
GET /metrics/hired_per_job_and_department - Número de empleados contratados por cada trabajo y departamento en 2021, dividido por trimestre.

GET /metrics/departments_above_average - Lista de departamentos que contrataron más empleados que el promedio en 2021.

