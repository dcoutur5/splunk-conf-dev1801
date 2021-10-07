import os
from app.wrappers import required
from flask import Blueprint, jsonify
import splunklib.client as client

bp = Blueprint("routes", __name__)

# =============================================================================
# =============== Route Definitions ===========================================
# =============================================================================

# =============== GET Definitions =============================================
@bp.route('/')
def hello():
    """
    This base '/' route returns a simple Hello World message.
    """
    return 'Hello, World! You\'ve successfully called your Flask server!'

# =============== POST Definitions ============================================
@bp.route('/index', methods=["POST"])
# This "@required" decorator helps deliver more readable error messages on  
# ill-formatted POST requests, as opposed to a more cryptic 500 server error.
@required({
    "type": "object",
    "properties": {
        "index_name": {"type": "string"},
    },
    "required": ["index_name"] 
})
def create_index(body):
    """
    The POST '/index' route will take in a json body with the fields:
    {index_name}

    This function will then create an index with the given name within your
    Splunk instance.
    """


    # TODO: Enter your associated Splunk SDK client parameters in the committed
    # .env file ===============================================================
    username = os.environ["username"]
    password = os.environ["password"]
    host = os.environ["splunk_url"]
    port = os.environ["splunk_port"]
    # =========================================================================

    # TODO: update these values with your associated parameters ===============
    data_owner = "admin"
    splunk_app_name = "search"
    sharing = "app"
    homePath = ""
    thawedPath = ""
    coldPath = ""
    # =========================================================================

    # Connect to the Splunk SDK client
    splunk_client = client.connect(
        host=host,
        port=str(port),
        username=username,
        password=password)

    # Grab the index_name from the incoming body
    index_name = body["index_name"]

    # Create the index
    index = splunk_client.indexes.create(
        name=index_name,
        owner=data_owner,
        app=splunk_app_name,
        sharing=sharing,
        homePath=homePath,
        thawedPath=thawedPath,
        coldPath=coldPath,
        )

    return jsonify({
        "status": "success",
        "msg": "Thank you for your submission to create an index.",
    }), 200

    
# =============================================================================
# =============== Exception Handlers ==========================================
# =============================================================================

@bp.errorhandler(Exception)
def exception_handler(error):
    """
    This exception handler returns the associated HTTP response, and lists the root error
    """
    return jsonify({
            "status": "err",
            "error": repr(error),
            "msg": "We're sorry, but there was an issue completing your request :(",
        }), error.code if hasattr(error, "code") else 500
