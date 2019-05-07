from datetime import datetime

from sqlalchemy import ForeignKey

from config import db, ma


class ShipmentProduct(db.Model):
    __tablename__ = "shipment_product"
    id = db.Column(db.BigInteger, primary_key=True)
    shipment_id = db.Column(db.BigInteger, ForeignKey('shipment.id'))
    product_id = db.Column(db.BigInteger)
    product_name = db.Column(db.String(64))
    quantity = db.Column(db.Integer)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, product_id=None, product_name=None, quantity=None):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity


class ShipmentProductSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(strict=True, **kwargs)

    class Meta:
        model = ShipmentProduct
        sqla_session = db.session

