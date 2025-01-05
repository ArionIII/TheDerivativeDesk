from flask import Flask, render_template, request
from configurations.futures_forwards_tool_config import FUTURES_FORWARDS_TOOL_CONFIG
from routes.futures_forward_routes import forwards_routes, futures_routes
from routes.hedging_routes import hedging_basics_routes, equity_hedging_routes
from routes.search_routes import search_routes
from routes.contract_valuation_routes import value_forward_routes, delivery_timing_decision_routes

from sub_categories_config import tool_category_future_forwards_routes
from routes.auth_routes import auth_routes
from config import logger
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask import session
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

# Initialize JWT
jwt = JWTManager(app)

# MongoDB connection
client = MongoClient(app.config["MONGO_URI"])
db = client.get_database()

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Register Blueprints
app.register_blueprint(forwards_routes)
app.register_blueprint(futures_routes)
app.register_blueprint(search_routes)
app.register_blueprint(hedging_basics_routes)   
app.register_blueprint(equity_hedging_routes)
app.register_blueprint(tool_category_future_forwards_routes) 
app.register_blueprint(value_forward_routes)  
app.register_blueprint(delivery_timing_decision_routes)

app.register_blueprint(auth_routes)


# Route pour la page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Route pour la page "À propos"
@app.route("/about")
def about():
    return render_template("about.html")

# Route pour la page "Contact"
@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Récupération des données du formulaire
        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")
        
        # Simuler l'envoi de message (vous pouvez connecter un service email ici)
        print(f"Message reçu de {name} ({email}): {message}")
        
        # Retourner une confirmation
        return render_template("contact.html", success=True)
    return render_template("contact.html", success=False)

# Route pour les outils
@app.route("/tools")
def tools():
    return render_template("tools.html")

# Route pour le blog
@app.route("/blog")
def blog():
    return render_template("blog.html")

# Route pour la page d'apprentissage
@app.route("/learn")
def learn():
    return render_template("learn.html")

# Route pour la page futures-forwards
@app.route("/tools/futures-forwards")
def futures_forwards():
    return render_template("futures-forwards.html")


@app.context_processor
def inject_user():
    return {
        "user_authenticated": "user_id" in session,
        "user": {
            "first_name": session.get("first_name"),
            "profile_picture": session.get("profile_picture", "/static/images/default-profile.png"),
        } if "user_id" in session else None
    }


# Lancer le serveur Flask
if __name__ == "__main__":
    logger.info("Starting the Flask application...")
    app.run(debug=True)
