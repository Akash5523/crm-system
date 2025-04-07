from flask import Blueprint, jsonify, render_template
from models import Contact, Lead, Ticket, Task
from app import db

dashboard_bp = Blueprint("dashboard_bp", __name__)

# API endpoint for dashboard (if needed)
@dashboard_bp.route("/api", methods=["GET"])
def get_dashboard():
    total_contacts = Contact.query.count()
    total_leads = Lead.query.count()
    open_tickets = Ticket.query.filter_by(status="open").count()
    pending_tasks = Task.query.filter_by(status="pending").count()

    stats = {
        "total_contacts": total_contacts,
        "total_leads": total_leads,
        "open_tickets": open_tickets,
        "pending_tasks": pending_tasks
    }
    return jsonify(stats), 200

# HTML dashboard page (for form-based login)
@dashboard_bp.route("/", methods=["GET"])
def dashboard_home():
    total_contacts = Contact.query.count()
    total_leads = Lead.query.count()
    open_tickets = Ticket.query.filter_by(status="open").count()
    pending_tasks = Task.query.filter_by(status="pending").count()

    return render_template("dashboard.html",
                           total_contacts=total_contacts,
                           total_leads=total_leads,
                           open_tickets=open_tickets,
                           pending_tasks=pending_tasks)
