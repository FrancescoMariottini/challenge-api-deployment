from base import Base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String, Boolean



class PropertyData(Base):

    __tablename__ = 'property_data'
    id = Column(String, primary_key=True)
    postcode = Column(Integer)
    house_is = Column(Boolean)
    property_subtype = Column(String)
    price = Column(Integer)
    room_number = Column(Integer)
    area = Column(Integer)
    equipped_kitchen_has = Column(Boolean)
    furnished = Column(Boolean)
    open_fire = Column(Boolean)
    terrace = Column(Boolean)
    garden = Column(Boolean)
    terrace_area = Column(Integer)
    garden_area = Column(Integer)
    facades_number = Column(Integer)
    swimming_pool_has = Column(Boolean)
    building_state_agg = Column(String)

    def __init__(self, id, postcode, house_is, property_subtype, price, room_number, area, equipped_kitchen_has, furnished,
    open_fire, terrace, garden, terrace_area, garden_area, facades_number, swimming_pool_has, building_state_agg):
        self.id = id
        self.postcode = postcode
        self.house_is = house_is
        self.property_subtype = property_subtype
        self.price = price
        self.room_number = room_number
        self.area = area
        self.equipped_kitchen_has = equipped_kitchen_has
        self.furnished = furnished
        self.open_fire = open_fire
        self.terrace = terrace
        self.garden = garden
        self.terrace_area = terrace_area
        self.garden_area = garden_area
        self.facades_number = facades_number
        self.swimming_pool_has = swimming_pool_has
        self.building_state_agg = building_state_agg