from flask import Blueprint, render_template

leads_bp = Blueprint('leads', __name__, url_prefix='/leads')

@leads_bp.route('/')
def leads_home():
    return render_template('leads.html')
