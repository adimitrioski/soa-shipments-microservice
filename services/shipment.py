from flask import make_response, abort
from config import db, db_breaker
from models.shipment import Shipment, ShipmentSchema, Status, Rating
from models.shipment_product import ShipmentProduct
from models.shipments_metadata import ShipmentsMetadata


@db_breaker
def get_all(status=None, rating=None, username=None, product_id=None):
    shipments = Shipment.query
    if status is not None:
        shipments = shipments.filter(Shipment.status == status)
    if rating is not None:
        shipments = shipments.filter(Shipment.rating == rating)
    if username is not None:
        shipments = shipments.filter(Shipment.username == username)
    if product_id is not None:
        shipments = shipments.join(ShipmentProduct).filter(ShipmentProduct.product_id == product_id)
    shipments = shipments.all()
    schema = ShipmentSchema(many=True)
    data = schema.dump(shipments).data
    return data


@db_breaker
def get_one(shipment_id):
    shipment = Shipment.query.filter(Shipment.id == shipment_id).one_or_none()

    if shipment is not None:
        schema = ShipmentSchema()
        data = schema.dump(shipment).data
        return data
    else:
        abort(404, "Shipment not found")


@db_breaker
def create(shipment):
    schema = ShipmentSchema()
    new_shipment = schema.load(shipment, session=db.session).data
    db.session.add(new_shipment)
    db.session.commit()

    data = schema.dump(new_shipment).data

    return data


@db_breaker
def update(shipment_id, shipment):
    update_shipment = (
        Shipment.query.filter(Shipment.id == shipment_id).one_or_none()
    )

    if update_shipment is not None:
        schema = ShipmentSchema()
        update_shipment_schema = schema.load(shipment, session=db.session).data

        update_shipment_schema.id = update_shipment.id
        db.session.merge(update_shipment_schema)
        db.session.commit()

        return make_response("Person deleted", 200)
    else:
        abort(404, "Shipment not found")


@db_breaker
def delete(shipment_id):
    shipment = Shipment.query.filter(Shipment.id == shipment_id).one_or_none()

    if shipment is not None:
        db.session.delete(shipment)
        db.session.commit()

        return make_response("Shipment deleted", 200)
    else:
        abort(404, "Shipment not found")


@db_breaker
def get_metadata():
    shipments_metadata = ShipmentsMetadata()

    shipments_metadata.total_shipments = Shipment.query.count()
    shipments_metadata.total_in_progress = Shipment.query.filter(Shipment.status == Status.IN_PROGRESS).count()
    shipments_metadata.total_arrived = Shipment.query.filter(Shipment.status == Status.ARRIVED).count()
    shipments_metadata.total_not_successful = Shipment.query.filter(Shipment.status == Status.NOT_SUCCESSFUL).count()
    shipments_metadata.total_returned = Shipment.query.filter(Shipment.status == Status.RETURNED).count()
    shipments_metadata.total_rating_very_good = Shipment.query.filter(Shipment.rating == Rating.VERY_GOOD).count()
    shipments_metadata.total_rating_good = Shipment.query.filter(Shipment.rating == Rating.GOOD).count()
    shipments_metadata.total_rating_ok = Shipment.query.filter(Shipment.rating == Rating.OK).count()
    shipments_metadata.total_rating_bad = Shipment.query.filter(Shipment.rating == Rating.BAD).count()
    shipments_metadata.total_rating_very_bad = Shipment.query.filter(Shipment.rating == Rating.VERY_BAD).count()

    data = vars(shipments_metadata)

    return data




