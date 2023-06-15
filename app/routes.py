# importing app to route different web directories
from app import app

# if url = localhost:5000/ call this function and return this
@app.route('/')
def index():
    return "Home page"