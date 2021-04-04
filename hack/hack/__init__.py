from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#from flask_login import LoginManager
from flask_login import LoginManager 
from os.path import join, dirname, realpath



app = Flask(__name__ )
app.config['SECRET_KEY'] = 'thisisthesecretkeyforvesithacks21project'


app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:12345@localhost/event_dashboard"

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads')
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) 


login_manager.login_view = 'login'
#login_manager.login_message_category = 'info'



from hack import routes

