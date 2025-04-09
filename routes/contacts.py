from routes.auth import login_required
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from models import Contact

contacts_bp = Blueprint('contacts', __name__, url_prefix='/contacts')

# @contacts_bp.route('/')
# def contacts_home():
#     return render_template('contacts.html')

@contacts_bp.route('/')
@login_required
def contacts_home():
    contacts = Contact.query.all()
    return render_template('contacts/list.html', contacts=contacts)

# Add new contact
@contacts_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        if Contact.query.filter_by(email=email).first():
            flash("A contact with this email already exists.", "danger")
            return redirect(url_for('contacts.add_contact'))

        new_contact = Contact(name=name, email=email, phone=phone)
        db.session.add(new_contact)
        db.session.commit()
        flash("Contact added successfully!", "success")
        return redirect(url_for('contacts.contacts_home'))

    return render_template('contacts/add.html')


# Edit contact
@contacts_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_contact(id):
    contact = Contact.query.get_or_404(id)

    if request.method == 'POST':
        contact.name = request.form['name']
        contact.email = request.form['email']
        contact.phone = request.form['phone']
        db.session.commit()
        flash("Contact updated successfully!", "success")
        return redirect(url_for('contacts.contacts_home'))

    return render_template('contacts/edit.html', contact=contact)


# Delete contact
@contacts_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    flash("Contact deleted successfully!", "success")
    return redirect(url_for('contacts.contacts_home'))


