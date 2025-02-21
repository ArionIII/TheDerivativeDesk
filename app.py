from flask import Flask, render_template, request, jsonify, send_from_directory
from configurations.tool_config.futures_forwards.futures_forwards_pricing_tool_config import FUTURES_FORWARDS_TOOL_CONFIG
from routes.futures_forward_routes import forwards_routes, futures_routes
from routes.hedging_routes import hedging_basics_routes, equity_hedging_routes
from routes.search_routes import search_routes
from routes.contract_valuation_routes import value_forward_routes, delivery_timing_decision_routes

from configurations.sub_config.futures_forwards.futures_forwards_sub_categories_config import tool_category_future_forwards_routes
from configurations.sub_config.statistics.statistics_sub_categories_config import tool_category_statistics_routes
from routes.auth_routes import auth_routes
from config import logger
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
from flask import session
from config import Config
from routes.basic_statistical_analysis_routes import descriptive_statistics_routes, inferential_statistics_routes, probability_tools_routes
from routes.time_series_and_modeling_routes import time_series_and_modeling_routes
from routes.simulation_and_bayesian_analysis_routes import simulation_and_bayesian_analysis_routes
from routes.linear_algebra_and_advanced_calculation_routes import linear_algebra_and_advanced_calculations_routes
from routes.interest_rates_fundamentals_routes import interest_rate_fundamentals_routes
from routes.interest_rate_derivatives_routes import interest_rate_derivatives_routes
from routes.stock_routes import stocks_routes, stock_chart_routes
from configurations.sub_config.interest_rates.interest_rate_sub_categories_config import tool_category_interest_rates_routes
import os
from web_parsing.news_rss_parser import get_news_from_rss
from routes.stock_routes import stock_news_routes

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
app.register_blueprint(tool_category_statistics_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(descriptive_statistics_routes)
app.register_blueprint(inferential_statistics_routes)
app.register_blueprint(probability_tools_routes)
app.register_blueprint(stocks_routes)
app.register_blueprint(stock_chart_routes)
app.register_blueprint(time_series_and_modeling_routes)
app.register_blueprint(simulation_and_bayesian_analysis_routes)
app.register_blueprint(linear_algebra_and_advanced_calculations_routes)
app.register_blueprint(interest_rate_fundamentals_routes)
app.register_blueprint(tool_category_interest_rates_routes)
app.register_blueprint(interest_rate_derivatives_routes)
app.register_blueprint(stock_news_routes)

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory("static", "sitemap.xml", mimetype="application/xml")

# Route pour la page d'accueil
@app.route("/")
def index():
    return render_template("index.html")

# Route pour la page "À propos"
@app.route("/about")
def about():
    return render_template("under_construction.html")

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
    return render_template("under_construction.html", success=False)

# Route pour les outils
@app.route("/tools")
def tools():
    return render_template("tools.html")

# Route pour le blog
@app.route("/blog")
def blog():
    return render_template("under_construction.html")

# Route pour la page futures-forwards
@app.route("/tools/futures-forwards")
def futures_forwards():
    return render_template("futures-forwards.html")

# Route pour la page statistics
@app.route("/tools/statistics")
def statistics():
    return render_template("statistics.html")

# Route pour la page interest rates
@app.route("/tools/interest-rates")
def interest_rates():
    return render_template("interest_rates.html")


@app.context_processor
def inject_user():
    return {
        "user_authenticated": "user_id" in session,
        "user": {
            "first_name": session.get("first_name"),
            "profile_picture": session.get("profile_picture", "/static/images/default-profile.png"),
        } if "user_id" in session else None
    }

@app.route("/news", methods=["GET"])
def news_page():
    """Affiche la page HTML avec la liste des news."""
    return render_template("news.html")  # NE RENVOIE QUE DU HTML

@app.route("/api/news", methods=["GET"])
def get_news():
    """Retourne les news au format JSON pour le JavaScript."""
    logger.info("Fetching news from app...")
    news = get_news_from_rss()
    logger.info("News fetched successfully.")

    response = jsonify(news)
    response.headers["Content-Type"] = "application/json"
    return response

# Lancer le serveur Flask
if __name__ == "__main__":
    logger.info("Starting the Flask application...")
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=True, host='0.0.0.0', port=port)
