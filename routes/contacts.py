from flask import Blueprint, render_template

contacts_bp = Blueprint('contacts', __name__, url_prefix='/contacts')

@contacts_bp.route('/')
def contacts_home():
    return render_template('contacts.html')
