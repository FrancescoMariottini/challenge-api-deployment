
from base import Session, engine, Base
from property_data import PropertyData

Base.metadata.create_all(engine)

def get_all():
    session = Session()
    return session.query(PropertyData).all()
    session.close()

def insert(list_property_data):
    Base.metadata.create_all(engine)
    session = Session()
    for property_data in list_property_data:
        session.add(property_data)
    session.commit()
    session.close()
