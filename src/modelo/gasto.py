from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from src.modelo.declarative_base import Base

class Gasto(Base):
    __tablename__ = 'gasto'
    id = Column(Integer, primary_key=True)
    concepto = Column(String)
    valor = Column(Float)
    fecha = Column(Date, index=True)
    actividad = Column(Integer, ForeignKey('actividad.id'))
    viajero = Column(Integer, ForeignKey('viajero.id'))


