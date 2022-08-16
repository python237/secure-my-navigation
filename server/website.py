from flask import redirect, make_response, Flask, request, render_template, jsonify
from six.moves.urllib.parse import urlparse

from db.migrations import DBOperation
from utils.domain import is_malicious_domain


app = Flask(__name__, static_url_path='/static', static_folder="./assets")

# Site config
app.config["DEBUG"] = True
app.config["HOST"] = "localhost"
app.config["PORT"] = 4700
app.config["VERBOSE"] = True

# Init db
db = DBOperation()


# ++++++++++++++++++
# Server route

@app.route("/verify", methods=["GET"])
def verify_site():
    # Vérifie si le site que l'utilisateur souhaite consulter est correct ou doit etre bloqué.
    host_source = request.args.get("host_source", None)

    if host_source:
        host_source = urlparse(host_source.lower()).netloc
        
        return make_response(jsonify({
            "decision": "block" if is_malicious_domain(host_source, db) else "less",
            "source": host_source
        }), 200)

    return redirect("/")


@app.route("/signalment", methods=["GET"])
def signal_site():
    # Enregistre les sites signalés par les utilisateurs.
    host_source: str = request.args.get("host_source", None)
    
    if host_source:
        if "." in host_source and not host_source.endswith(".") and not host_source.startswith("."):
            host_source = (lambda x: x.netloc or x.path)(urlparse(host_source.lower()))
            db.add_signal(host_source)
            
            return make_response(jsonify({"decision": "add", "source": host_source}), 200)
        else:
            return make_response(jsonify({"decision": "invalid"}), 200)

    return redirect("/")


@app.route("/blocked/<path:source>", methods=["GET"])
def blocked_site(source: str):
    # Requete bloqué
    if is_malicious_domain(source, db):
        return render_template("blocked.html", **locals())
    return redirect("/")


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html", **locals())


# +++++++++++++++++
# Start server
def runserver():    
    app.debug = app.config["DEBUG"]
    app.run(host=app.config["HOST"], port=app.config["PORT"])
