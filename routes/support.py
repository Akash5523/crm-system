from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models import SupportTicket, Lead
from routes.auth import login_required
from datetime import date

support_bp = Blueprint('support', __name__, url_prefix='/support')

# List support tickets
@support_bp.route('/')
@login_required
def list_tickets():
    search = request.args.get('search', '').strip()
    status = request.args.get('status', '').strip()

    query = SupportTicket.query.join(Lead)

    if search:
        query = query.filter(
            (Lead.company_name.ilike(f'%{search}%')) |
            (SupportTicket.subject.ilike(f'%{search}%'))
        )

    if status:
        query = query.filter(SupportTicket.status == status)

    tickets = query.order_by(SupportTicket.last_contacted.desc()).all()

    return render_template('support/list.html', tickets=tickets)
    # tickets = SupportTicket.query.order_by(SupportTicket.last_contacted.desc()).all()
    # return render_template('support/list.html', tickets=tickets)

# Add support ticket
@support_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_ticket():
    leads = Lead.query.all()
    if request.method == 'POST':
        lead_id = request.form.get('lead_id')
        subject = request.form.get('subject')
        status = request.form.get('status', 'Open')
        last_contacted = request.form.get('last_contacted') or date.today()
        next_step = request.form.get('next_step')

        new_ticket = SupportTicket(
            lead_id=lead_id,
            subject=subject,
            status=status,
            last_contacted=last_contacted,
            next_step=next_step
        )

        db.session.add(new_ticket)
        db.session.commit()
        flash('Support ticket added.', 'success')
        return redirect(url_for('support.list_tickets'))

    return render_template('support/add.html', leads=leads)

# Edit support ticket
@support_bp.route('/edit/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def edit_ticket(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    leads = Lead.query.all()

    if request.method == 'POST':
        ticket.lead_id = request.form.get('lead_id')
        ticket.subject = request.form.get('subject')
        ticket.status = request.form.get('status')
        ticket.last_contacted = request.form.get('last_contacted') or date.today()
        ticket.next_step = request.form.get('next_step')

        db.session.commit()
        flash('Support ticket updated.', 'success')
        return redirect(url_for('support.list_tickets'))

    return render_template('support/edit.html', ticket=ticket, leads=leads)

# Delete support ticket
@support_bp.route('/delete/<int:ticket_id>', methods=['POST'])
@login_required
def delete_ticket(ticket_id):
    ticket = SupportTicket.query.get_or_404(ticket_id)
    db.session.delete(ticket)
    db.session.commit()
    flash('Support ticket deleted.', 'info')
    return redirect(url_for('support.list_tickets'))