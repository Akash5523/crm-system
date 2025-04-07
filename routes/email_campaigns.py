from flask import Blueprint, render_template

email_campaigns_bp = Blueprint('email_campaigns', __name__, url_prefix='/email-campaigns')

@email_campaigns_bp.route('/')
def email_home():
    return render_template('email_campaigns.html')
