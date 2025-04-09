from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv
from jinja2 import FileSystemLoader

# Load .env variables
load_dotenv()

db = SQLAlchemy()

def create_app(config_name="production"):
    basedir = os.path.abspath(os.path.dirname(__file__))
    # Explicitly set template and static folder paths
    app = Flask(
        __name__,
        template_folder=os.path.join(basedir, "templates"),
        static_folder=os.path.join(basedir, "static")
    )
    # Force Jinja2 to use FileSystemLoader
    app.jinja_loader = FileSystemLoader(os.path.join(basedir, "templates"))
    
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)

    # Register blueprints (all blueprints defined in routes/)
    from routes.auth import auth_bp
    from routes.contacts import contacts_bp
    from routes.leads import leads_bp
    from routes.sales import sales_bp
    from routes.tasks import tasks_bp
    from routes.email_campaigns import email_campaigns_bp
    from routes.support import support_bp
    from routes.dashboard import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(contacts_bp, url_prefix="/api/contacts")
    app.register_blueprint(leads_bp, url_prefix="/api/leads")
    app.register_blueprint(sales_bp, url_prefix="/api/sales")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(email_campaigns_bp, url_prefix="/api/email")
    app.register_blueprint(support_bp, url_prefix="/api/support")
    app.register_blueprint(dashboard_bp)
    # app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

    # Logging configuration
    if not app.debug:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler("logs/crm.log", maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info("CRM startup")

    # Health-check endpoint
    @app.route("/health")
    def health():
        return jsonify({"status": "OK"}), 200

    # Landing page endpoint
    @app.route("/")
    def landing():
        return render_template("landing.html")

    return app

if __name__ == "__main__":
    application = create_app("development")
    application.run(host="0.0.0.0", port=5000, debug=True)
