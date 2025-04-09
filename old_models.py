from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True, nullable=False)
    email = db.Column(db.String(120), unique=True, index=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default="user")  # e.g., admin, sales, support, marketing

    def set_password(self, password):
        # Use pbkdf2:sha256 for compatibility
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
    interactions = db.relationship("Interaction", backref="contact", lazy="dynamic")

class Interaction(db.Model):
    __tablename__ = "interactions"
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable=False)
    note = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Lead(db.Model):
    __tablename__ = "leads"
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey("contacts.id"), nullable=False)
    status = db.Column(db.String(20), default="new")  # new, contacted, converted, lost
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    contact = db.relationship("Contact", backref="lead", uselist=False)

class SalesOpportunity(db.Model):
    __tablename__ = "sales_opportunities"
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey("leads.id"), nullable=False)
    stage = db.Column(db.String(50), default="qualification")  # qualification, proposal, negotiation, closed
    amount = db.Column(db.Float)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    lead = db.relationship("Lead", backref="opportunity", uselist=False)

class Task(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    assigned_to = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="pending")  # pending, completed
    user = db.relationship("User", backref="tasks", lazy="joined")

class EmailCampaign(db.Model):
    __tablename__ = "email_campaigns"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    subject = db.Column(db.String(256))
    content = db.Column(db.Text)
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="open")  # open, in_progress, resolved, closed
    priority = db.Column(db.String(20), default="medium")  # low, medium, high
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship("User", backref="tickets", lazy="joined")
