from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required
from app import db
from models import Task, Lead
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

# List all tasks
@tasks_bp.route('/')
@login_required
def list_tasks():
    tasks = Task.query.order_by(Task.due_date.asc()).all()
    return render_template('tasks/list.html', tasks=tasks)

# Add a new task
@tasks_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_task():
    leads = Lead.query.all()
    if request.method == 'POST':
        lead_id = request.form.get('lead_id')
        title = request.form.get('title')
        due_date = request.form.get('due_date')
        assigned_to = request.form.get('assigned_to')
        status = request.form.get('status') or 'Pending'

        if not title or not lead_id:
            flash("Lead and title are required fields.", "error")
            return redirect(url_for('tasks.add_task'))

        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "error")
            return redirect(url_for('tasks.add_task'))

        new_task = Task(
            lead_id=lead_id,
            title=title,
            due_date=due_date,
            assigned_to=assigned_to,
            status=status
        )
        db.session.add(new_task)
        db.session.commit()
        flash("Task added successfully.", "success")
        return redirect(url_for('tasks.list_tasks'))

    return render_template('tasks/add.html', leads=leads)

# Edit task
@tasks_bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    leads = Lead.query.all()

    if request.method == 'POST':
        task.title = request.form.get('title')
        task.lead_id = request.form.get('lead_id')
        task.assigned_to = request.form.get('assigned_to')
        task.status = request.form.get('status')

        due_date = request.form.get('due_date')
        try:
            task.due_date = datetime.strptime(due_date, "%Y-%m-%d") if due_date else None
        except ValueError:
            flash("Invalid date format. Please use YYYY-MM-DD.", "error")
            return redirect(url_for('tasks.edit_task', task_id=task.id))

        db.session.commit()
        flash("Task updated successfully.", "success")
        return redirect(url_for('tasks.list_tasks'))

    return render_template('tasks/edit.html', task=task, leads=leads)

# Delete task
@tasks_bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully.", "success")
    return redirect(url_for('tasks.list_tasks'))
