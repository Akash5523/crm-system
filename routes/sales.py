import math
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app import db
from models import Sale, Lead
from routes.auth import login_required
from decimal import Decimal
import logging

sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

# List all sales
@sales_bp.route('/')
@login_required
def list_sales():
    sales = Sale.query.order_by(Sale.expected_close_date.asc()).all()
    return render_template('sales/list.html', sales=sales)

# Add a new sale
# @sales_bp.route('/add', methods=['GET', 'POST'])
# @login_required
# def add_sale():
#     leads = Lead.query.all()

#     if request.method == 'POST':
#         lead_id = request.form.get('lead_id')
#         value = Decimal(request.form.get('value'))
#         probability = Decimal(request.form.get('probability'))
#         expected_close_date = request.form.get('expected_close_date')
#         expected_revenue = value * (probability / Decimal('100'))
#         progress_to_won = Decimal(request.form.get('progress_to_won') or 0)

#         try:
#             value = float(value)
#             probability = float(probability)
#             expected_revenue = value * (probability / 100)
#         except ValueError:
#             flash("Invalid numeric input.", "error")
#             return redirect(url_for('sales.add_sale'))

#         new_sale = Sale(
#             lead_id=lead_id,
#             value=value,
#             probability=probability,
#             expected_revenue=expected_revenue,
#             expected_close_date=expected_close_date,
#             progress_to_won=progress_to_won or 0
#         )

#         db.session.add(new_sale)
#         db.session.commit()
#         flash("Sale added successfully.", "success")
#         return redirect(url_for('sales.list_sales'))

#     return render_template('sales/add.html', leads=leads)

# Add a new sale
@sales_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_sale():
    leads = Lead.query.all()

    if request.method == 'POST':
        try:
            lead_id = int(request.form.get('lead_id'))
            value = float(request.form.get('value'))
            probability = float(request.form.get('probability'))
            progress_to_won = float(request.form.get('progress_to_won') or 0)
            expected_close_date = request.form.get('expected_close_date')

            # Ensure probability is within 0–100
            if not (0 <= probability <= 100):
                flash("Probability must be between 0 and 100.", "error")
                return redirect(url_for('sales.add_sale'))
            
            # Recalculate expected revenue in the backend
            cal_expected_revenue = value * (probability / 100)

            new_sale = Sale(
                lead_id=lead_id,
                value=value,
                probability=probability,
                expected_revenue=cal_expected_revenue,  # Use backend-calculated value
                expected_close_date=expected_close_date,
                progress_to_won=progress_to_won
            )

            db.session.add(new_sale)
            db.session.commit()
            flash("Sale added successfully.", "success")
            return redirect(url_for('sales.list_sales'))

        except (ValueError, TypeError) as e:
            current_app.logger.error(f"Error processing form data: {e}")
            flash("Please enter valid numeric values.", "error")
            return redirect(url_for('sales.add_sale'))

    return render_template('sales/add.html', leads=leads)



# Edit an existing sale
# @sales_bp.route('/edit/<int:sale_id>', methods=['GET', 'POST'])
# @login_required
# def edit_sale(sale_id):
#     sale = Sale.query.get_or_404(sale_id)
#     leads = Lead.query.all()

#     if request.method == 'POST':
#         sale.lead_id = request.form.get('lead_id')
#         sale.value = Decimal(request.form.get('value'))
#         sale.probability = Decimal(request.form.get('probability'))
#         sale.expected_revenue = sale.value * (sale.probability / Decimal('100'))
#         sale.expected_close_date = request.form.get('expected_close_date')
#         sale.progress_to_won = Decimal(request.form.get('progress_to_won') or 0)

#         db.session.commit()
#         flash("Sale updated successfully.", "success")
#         return redirect(url_for('sales.list_sales'))

#     return render_template('sales/edit.html', sale=sale, leads=leads)

@sales_bp.route('/edit/<int:sale_id>', methods=['GET', 'POST'])
@login_required
def edit_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    leads = Lead.query.all()

    if request.method == 'POST':
        try:
            sale.lead_id = int(request.form.get('lead_id'))
            sale.value = Decimal(request.form.get('value'))
            sale.probability = Decimal(request.form.get('probability'))
            sale.expected_close_date = request.form.get('expected_close_date')
            sale.progress_to_won = Decimal(request.form.get('progress_to_won') or 0)

            # Recalculate expected revenue in the backend
            sale.expected_revenue = sale.value * (sale.probability / Decimal('100'))

            db.session.commit()
            flash("Sale updated successfully.", "success")
            return redirect(url_for('sales.list_sales'))

        except (ValueError, TypeError) as e:
            current_app.logger.error(f"Error processing form data: {e}")
            flash("Please enter valid numeric values.", "error")
            return redirect(url_for('sales.edit_sale', sale_id=sale.id))

    return render_template('sales/edit.html', sale=sale, leads=leads)

# Delete a sale
@sales_bp.route('/delete/<int:sale_id>', methods=['POST'])
@login_required
def delete_sale(sale_id):
    sale = Sale.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    flash("Sale deleted.", "info")
    return redirect(url_for('sales.list_sales'))
