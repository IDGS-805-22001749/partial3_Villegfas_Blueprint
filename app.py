from flask import Flask, render_template, request, redirect, url_for, flash 
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, User
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from blueprints.alumnos_blueprint import alumnos_blueprint
from blueprints.profesores_blueprint import profesores_blueprint
from blueprints.login_blueprint import login_blueprint

import logging




app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login.login'
login_manager.login_message = "Por favor, inicia sesión para continuar."
login_manager.login_message_category = "warning"

logging.basicConfig(filename='app.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]')

logger = logging.getLogger(__name__)


logger.info("Aplicación Flask iniciada con éxito.")

app.register_blueprint(alumnos_blueprint, url_prefix='/alumnos')
app.register_blueprint(profesores_blueprint, url_prefix='/profesores')
app.register_blueprint(login_blueprint, url_prefix='/login')



@app.route('/')
@login_required
def index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run(debug=True)
