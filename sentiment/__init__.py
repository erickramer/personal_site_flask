from flask import Blueprint

# Create Blueprint but don't register routes yet
app = Blueprint('sentiment', __name__, static_folder='static', template_folder='templates')

# Import views at the bottom to avoid circular imports
from sentiment import views
