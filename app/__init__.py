from flask import Flask
from flask_sqlalchemy import SQLAlchemy



# SECRET_KEY is needed for session security, the flash() method in this case stores the message in a session
SECRET_KEY = 'Sup3r$3cretkey'
UPLOAD_FOLDER = './app/static/uploads'


#configuartion uploads
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://project1:password@localhost/project1"
app.config['UPLOAD_FOLDER']
Allowed_uploads=['png','jpg']
db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views
