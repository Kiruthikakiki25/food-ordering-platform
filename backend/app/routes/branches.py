from flask import Blueprint, jsonify
from app.models import Branch

branches_bp = Blueprint('branches', __name__)


@branches_bp.route('/branches', methods=['GET'])
def list_branches():
    branches = Branch.query.filter_by(is_active=True).all()
    return jsonify([
        {
            "id": b.id,
            "name": b.name,
            "address": b.address,
            "city": b.city,
            "pincode": b.pincode,
            "phone": b.phone,
            "opening_time": b.opening_time.strftime("%H:%M") if b.opening_time else None,
            "closing_time": b.closing_time.strftime("%H:%M") if b.closing_time else None,
        }
        for b in branches
    ])


@branches_bp.route('/branches/<int:branch_id>', methods=['GET'])
def get_branch(branch_id):
    b = Branch.query.get_or_404(branch_id)
    return jsonify({
        "id": b.id,
        "name": b.name,
        "address": b.address,
        "city": b.city,
        "pincode": b.pincode,
        "phone": b.phone,
        "opening_time": b.opening_time.strftime("%H:%M") if b.opening_time else None,
        "closing_time": b.closing_time.strftime("%H:%M") if b.closing_time else None,
    })