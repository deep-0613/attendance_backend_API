from flask import Blueprint, request, jsonify
from services.announcement_service import create_announcement_service, get_announcements_service

announcements_bp = Blueprint("announcements", __name__)


# API — Create Announcement
@announcements_bp.route("/announcements", methods=["POST"])
def create_announcement():
    
    data = request.json
    
    response, status = create_announcement_service(data)
    return jsonify(response), status


# API — Get Announcements by Batch
@announcements_bp.route("/announcements", methods=["GET"])
def get_announcements():
    
    batch = request.args.get("batch")
    
    response, status = get_announcements_service(batch)
    return jsonify(response), status
