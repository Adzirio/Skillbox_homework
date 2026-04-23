from datetime import datetime

from flask import Blueprint, g, jsonify, request

from .models import Client, ClientParking, Parking

bp = Blueprint("api", __name__)


@bp.get("/clients")
def get_clients():
    clients = g.session.query(Client).all()
    return (
        jsonify(
            [
                {
                    "id": c.id,
                    "name": c.name,
                    "surname": c.surname,
                    "credit_card": c.credit_card,
                    "car_number": c.car_number,
                }
                for c in clients
            ]
        ),
        200,
    )


@bp.get("/clients/<int:client_id>")
def get_client(client_id):
    client = g.session.get(Client, client_id)
    if not client:
        return jsonify({"error": "client not found"}), 404

    return (
        jsonify(
            {
                "id": client.id,
                "name": client.name,
                "surname": client.surname,
                "credit_card": client.credit_card,
                "car_number": client.car_number,
            }
        ),
        200,
    )


@bp.post("/clients")
def create_client():
    data = request.get_json(silent=True) or {}
    client = Client(
        name=data.get("name"),
        surname=data.get("surname"),
        credit_card=data.get("credit_card"),
        car_number=data.get("car_number"),
    )

    if not client.name or not client.surname:
        return jsonify({"error": "name and surname are required"}), 400

    g.session.add(client)
    g.session.commit()

    return jsonify({"id": client.id}), 201


@bp.post("/parkings")
def create_parking():
    data = request.get_json(silent=True) or {}
    parking = Parking(
        address=data.get("address"),
        opened=data.get("opened", True),
        count_places=data.get("count_places"),
        count_available_places=data.get("count_available_places"),
    )

    if (
        not parking.address
        or parking.count_places is None
        or parking.count_available_places is None
    ):
        return (
            jsonify(
                {
                    "error": "address, count_places "
                             "and count_available_places are required"
                }
            ),
            400,
        )

    g.session.add(parking)
    g.session.commit()

    return jsonify({"id": parking.id}), 201


# ЗАЕЗД И ВЫЕЗД


@bp.post("/client_parkings")
def enter_parking():
    data = request.get_json(silent=True) or {}
    client_id = data.get("client_id")
    parking_id = data.get("parking_id")

    if not client_id or not parking_id:
        return jsonify({"error": "client_id and parking_id are required"}), 400

    client = g.session.get(Client, client_id)
    parking = g.session.get(Parking, parking_id)

    if not client or not parking:
        return jsonify({"error": "client or parking not found"}), 404

    if not parking.opened:
        return jsonify({"error": "parking is closed"}), 409

    if parking.count_available_places <= 0:
        return jsonify({"error": "no available places"}), 409

    existing = (
        g.session.query(ClientParking)
        .filter_by(client_id=client_id, parking_id=parking_id)
        .first()
    )
    if existing and existing.time_out is None:
        return jsonify({"error": "client already parked here"}), 409

    row = ClientParking(
        client_id=client_id,
        parking_id=parking_id,
        time_in=datetime.now(),
        time_out=None,
    )
    parking.count_available_places -= 1

    g.session.add(row)
    g.session.commit()

    return jsonify({"message": "entered parking", "id": row.id}), 201


@bp.delete("/client_parkings")
def leave_parking():
    data = request.get_json(silent=True) or {}
    client_id = data.get("client_id")
    parking_id = data.get("parking_id")

    if not client_id or not parking_id:
        return jsonify({"error": "client_id and parking_id are required"}), 400

    client = g.session.get(Client, client_id)
    parking = g.session.get(Parking, parking_id)

    if not client or not parking:
        return jsonify({"error": "client or parking not found"}), 404

    if not client.credit_card:
        return jsonify({"error": "client has no credit card"}), 409

    row = (
        g.session.query(ClientParking)
        .filter_by(client_id=client_id, parking_id=parking_id, time_out=None)
        .first()
    )
    if not row:
        return jsonify({"error": "active parking record not found"}), 404

    row.time_out = datetime.now()
    parking.count_available_places += 1

    g.session.commit()

    return jsonify({"message": "left parking"}), 200
