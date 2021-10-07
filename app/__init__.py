from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app) # This line is necessary for other applications to call your server.

    import app.routes as routes
    app.register_blueprint(routes.bp)    
    
    return app
