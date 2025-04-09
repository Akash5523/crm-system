from flask import Blueprint, jsonify, render_template, session
from models import Contact, Lead, SupportTicket, Task, Sale
from app import db
from routes.auth import login_required

dashboard_bp = Blueprint("dashboard_bp", __name__, url_prefix="/dashboard")

@dashboard_bp.route("/api", methods=["GET"])
@login_required
def get_dashboard_data():
    stats = {
        "total_contacts": Contact.query.count(),
        "total_leads": Lead.query.count(),
        "open_support_tickets": SupportTicket.query.filter_by(status="open").count(),
        "pending_tasks": Task.query.filter_by(status="pending").count(),
        "total_sales": Sale.query.count(),
    }
    return jsonify(stats), 200

@dashboard_bp.route("/", methods=["GET"])
@login_required
def dashboard_home():
    stats = {
        "total_contacts": Contact.query.count(),
        "total_leads": Lead.query.count(),
        "open_support_tickets": SupportTicket.query.filter_by(status="open").count(),
        "pending_tasks": Task.query.filter_by(status="pending").count(),
        "total_sales": Sale.query.count(),
    }
    return render_template("dashboard.html", username=session.get("username"), **stats)
