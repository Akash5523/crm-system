from flask import Blueprint, render_template

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/')
def tasks_home():
    return render_template('tasks.html')
