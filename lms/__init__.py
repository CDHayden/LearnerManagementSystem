from flask import Flask

from .views.home import mod as home
from .views.student import mod as student
from .views.admin import mod as admin
from .views.staff import mod as staff

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

app.register_blueprint(home)
app.register_blueprint(student, url_prefix="/student")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(staff, url_prefix="/staff")