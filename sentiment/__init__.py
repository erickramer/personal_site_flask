from flask import Flask, Blueprint

app = Blueprint('sentiment', __name__, static_folder='static', template_folder='templates')

import views
