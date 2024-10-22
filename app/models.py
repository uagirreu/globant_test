from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db import Base

# Tabla Department
class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=False, index=True)  # Establecer autoincrement como False
    department = Column(String, index=True)  # Nombre del departamento

# Tabla Job
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=False, index=True)  # Establecer autoincrement como False
    job = Column(String, index=True)  # Nombre del trabajo

# Tabla Employee (Hired Employees)
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=False, index=True)  # Establecer autoincrement como False
    name = Column(String, index=True)  # Nombre y apellido del empleado
    datetime = Column(DateTime, index=True)  # Fecha y hora de contratación
    department_id = Column(Integer, ForeignKey('departments.id'))  # Id del departamento
    job_id = Column(Integer, ForeignKey('jobs.id'))  # Id del trabajo

    # Relaciones
    job = relationship("Job")
    department = relationship("Department")
