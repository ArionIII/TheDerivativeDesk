from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from bson import ObjectId
from config import db

requests_bp = Blueprint("requests", __name__)

@requests_bp.route("/create", methods=["POST"])
@jwt_required()
def create_request():
    user_id = get_jwt_identity()
    data = request.get_json()

    required_fields = ["type", "tool_key", "description"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
    
    if data["type"] not in ["feature", "issue"]:
        return jsonify({"error": "Invalid request type"}), 400

    new_request = {
        "user_id": ObjectId(user_id),
        "type": data["type"],
        "tool_key": data["tool_key"],
        "description": data["description"],
        "status": "open",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    db.requests.insert_one(new_request)
    return jsonify({"message": "Request submitted successfully"}), 201


@requests_bp.route("/list", methods=["GET"])
@jwt_required()
def list_requests():
    user_id = get_jwt_identity()
    requests = list(db.requests.find({"user_id": ObjectId(user_id)}))
    
    for req in requests:
        req["_id"] = str(req["_id"])
        req["user_id"] = str(req["user_id"])

    return jsonify(requests), 200


@requests_bp.route("/update/<request_id>", methods=["PATCH"])
@jwt_required()
def update_request(request_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    update_data = { "updated_at": datetime.utcnow() }
    if "status" in data:
        update_data["status"] = data["status"]

    result = db.requests.update_one(
        {"_id": ObjectId(request_id), "user_id": ObjectId(user_id)},
        {"$set": update_data}
    )

    if result.modified_count == 0:
        return jsonify({"error": "Request not found or not modified"}), 404

    return jsonify({"message": "Request updated"}), 200


@requests_bp.route("/delete/<request_id>", methods=["DELETE"])
@jwt_required()
def delete_request(request_id):
    user_id = get_jwt_identity()
    
    result = db.requests.delete_one({"_id": ObjectId(request_id), "user_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Request not found"}), 404

    return jsonify({"message": "Request deleted"}), 200

