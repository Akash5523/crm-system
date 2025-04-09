from datetime import datetime, date
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Contact(db.Model):
    __tablename__ = "contacts"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Lead(db.Model):
    __tablename__ = "leads"
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    contact_name = db.Column(db.String(255), nullable=False)
    contact_email = db.Column(db.String(255), unique=True, nullable=False)
    stage = db.Column(db.String(100), default='Lead')
    creation_date = db.Column(db.Date, default=date.today)
    team_member = db.Column(db.String(100))


class Interaction(db.Model):
    __tablename__ = "interactions"
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    date = db.Column(db.Date, default=date.today)
    notes = db.Column(db.Text)
    lead = db.relationship("Lead", backref="interactions")


class Sale(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    value = db.Column(db.Numeric(12, 2), nullable=False)
    probability = db.Column(db.Numeric(5, 2))
    expected_revenue = db.Column(db.Numeric(12, 2))
    expected_close_date = db.Column(db.Date)
    progress_to_won = db.Column(db.Numeric(5, 2), default=0.00)
    lead = db.relationship("Lead", backref="sales")


class SupportTicket(db.Model):
    __tablename__ = "support_tickets"
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    subject = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='Open')
    last_contacted = db.Column(db.Date, default=date.today)
    next_step = db.Column(db.Text)
    lead = db.relationship("Lead", backref="support_tickets")


class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.Text, nullable=False)
    due_date = db.Column(db.Date)
    assigned_to = db.Column(db.String(100))
    status = db.Column(db.String(50), default='Pending')
    lead = db.relationship("Lead", backref="tasks")
