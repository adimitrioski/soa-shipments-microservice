from datetime import datetime
from config import db, ma
from enum import Enum
from marshmallow import fields
from marshmallow_enum import EnumField

from models.shipment_product import ShipmentProduct


class Status(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    ARRIVED = "ARRIVED"
    NOT_SUCCESSFUL = "NOT_SUCCESSFUL"
    RETURNED = "RETURNED"


class TransportationType(Enum):
    NO_INFORMATION_AVAILABLE = "NO_INFORMATION_AVAILABLE"
    AIRPLANE = "AIRPLANE"
    SHIP = "SHIP"
    TRUCK = "TRUCK"


class Rating(Enum):
    NO_INPUT_AVAILABLE = "NO_INPUT_AVAILABLE"
    VERY_GOOD = "VERY_GOOD"
    GOOD = "GOOD"
    OK = "OK"
    BAD = "BAD"
    VERY_BAD = "VERY_BAD"


class Shipment(db.Model):
    __tablename__ = "shipment"
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(32))
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    products = db.relationship(
        ShipmentProduct,
        cascade="all, delete, delete-orphan",
        single_parent=True)
    address = db.Column(db.String(64))
    last_known_location = db.Column(db.String(64))
    status = db.Column(db.Enum(Status), default=Status.IN_PROGRESS)
    current_transportation_type = db.Column(
        db.Enum(TransportationType),
        default=TransportationType.NO_INFORMATION_AVAILABLE)
    rating = db.Column(db.Enum(Rating), default=Rating.NO_INPUT_AVAILABLE)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(
            self,
            username=None,
            first_name=None,
            last_name=None,
            products=None,
            address=None,
            last_known_location=None,
            status=None,
            current_transportation_type=None,
            rating=None):

        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.products = products
        self.address = address
        self.last_known_location = last_known_location
        self.status = status
        self.current_transportation_type = current_transportation_type
        self.rating = rating


class ShipmentSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = Shipment
        sqla_session = db.session

    status = EnumField(Status, by_value=True)
    current_transportation_type = EnumField(TransportationType, by_value=True)
    rating = EnumField(Rating, by_value=True)

    products = fields.Nested("ShipmentProductSchema", default=[], many=True)
