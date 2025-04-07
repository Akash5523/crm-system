from flask import Blueprint, render_template

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/')
def sales_home():
    return render_template('sales.html')
