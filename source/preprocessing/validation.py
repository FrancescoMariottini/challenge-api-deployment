from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Length, Range

class DataFeatures(Schema):
    area = fields.Int(required=True)
    property_type = fields.Str(required=True, validate=Length(max=30))
    rooms_number = fields.Int(required=True,validate=Range(min=1))
    zip_code = fields.Int(required=True, validate=Range(min=1000, max=9999))
    land_area = fields.Int(required=False,validate=Range(min=1))
    garden =  fields.Bool(required=False)
    garden_area = fields.Int(required=False,validate=Range(min=1))
    equipped_kitchen = fields.Bool(required=False)
    full_address = fields.Str(required=False, validate=Length(max=100))
    swimmingpool = fields.Bool(required=False)
    furnished= fields.Bool(required=False)
    open_fire = fields.Bool(required=False)
    terrace = fields.Bool(required=False)
    terrace_area = fields.Int(required=False,validate=Range(min=1))
    facades_number = fields.Int(required=False,validate=Range(min=1))
    building_state =  fields.Str(required=False, validate=Length(max=30))

    @validates('property_type')
    def prop_type_validation(value):
        if value.lower() not in ["apartment", "house", "others"]:
            raise ValidationError("This type doesn't exist, please select between: apartment, house or others")

    @validates('building_state')
    def build_state_validation(value):
        if value.lower() not in ["new", "good", "to renovate", "just renovated", "to rebuild"]:
            raise ValidationError("This state doesn't exist, please select one bewteen: new, good, to renovate, just renovated or to rebuil")