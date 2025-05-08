from sqlalchemy import Column, Integer, String
from db import Base 

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    rut = Column(String(20), Unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    adress_street = Column(String(100), nullable=False)
    adress_number = Column(String(10), nullable=False)
    adress_comune = Column(String(50), nullable=False)
    adress_city = Column(String(50), nullable=False)
    phones = Column(String(200), nullable=True)

def __repr__(self):
    return f"<Client {self.name} - {self.rut}>"