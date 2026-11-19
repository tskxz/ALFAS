from flask import Blueprint, jsonify

from models import Schoolyear

schoolyears_bp = Blueprint('schoolyears', __name__)

@schoolyears_bp.get("/schoolyears")
def get_schoolyears():
    schoolyears = Schoolyear.query.order_by(Schoolyear.id).all()
    return jsonify([
        {"id": schoolyear.id, "schoolyear": schoolyear.schoolyear}
        for schoolyear in schoolyears
    ])


