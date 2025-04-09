from flask import Blueprint, render_template, request, redirect, url_for, flash
from routes.auth import login_required
from datetime import date
from app import db
from models import Lead

leads_bp = Blueprint('leads', __name__, template_folder='templates/leads')

@leads_bp.route('/leads')
@login_required
def leads_home():
    leads = Lead.query.all()
    return render_template('leads/list.html', leads=leads)

@leads_bp.route('/leads/add', methods=['GET', 'POST'])
@login_required
def add_lead():
    if request.method == 'POST':
        company_name = request.form['company_name']
        contact_name = request.form['contact_name']
        contact_email = request.form['contact_email']
        stage = request.form['stage']
        team_member = request.form['team_member']

        new_lead = Lead(
            company_name=company_name,
            contact_name=contact_name,
            contact_email=contact_email,
            stage=stage,
            creation_date=date.today(),
            team_member=team_member
        )
        db.session.add(new_lead)
        db.session.commit()
        flash('Lead added successfully!', 'success')
        return redirect(url_for('leads.leads_home'))

    return render_template('leads/add.html')

@leads_bp.route('/leads/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_lead(id):
    lead = Lead.query.get_or_404(id)
    if request.method == 'POST':
        lead.company_name = request.form['company_name']
        lead.contact_name = request.form['contact_name']
        lead.contact_email = request.form['contact_email']
        lead.stage = request.form['stage']
        lead.team_member = request.form['team_member']

        db.session.commit()
        flash('Lead updated successfully!', 'success')
        return redirect(url_for('leads.leads_home'))

    return render_template('leads/edit.html', lead=lead)

@leads_bp.route('/leads/delete/<int:id>', methods=['POST'])
@login_required
def delete_lead(id):
    lead = Lead.query.get_or_404(id)
    db.session.delete(lead)
    db.session.commit()
    flash('Lead deleted successfully!', 'success')
    return redirect(url_for('leads.leads_home'))
