from flask import Blueprint, render_template, request, jsonify
from config import logger
from configurations.tool_config.futures_forwards.futures_forwards_pricing_tool_config import FUTURES_FORWARDS_TOOL_CONFIG
from configurations.tool_config.futures_forwards.hedging_tool_config import HEDGING_TOOL_CONFIG
from configurations.tool_config.futures_forwards.contract_valuation_tool_config import CONTRACT_VALUATION_TOOL_CONFIG

ALL_TOOLS = FUTURES_FORWARDS_TOOL_CONFIG | HEDGING_TOOL_CONFIG | CONTRACT_VALUATION_TOOL_CONFIG

search_routes = Blueprint("search", __name__)

@search_routes.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "").strip().lower()
    
    if not query:
        return render_template("search.html", results=[])

    query_tokens = query.split()  # Split query into tokens
    results = []

    for tool_key, tool in ALL_TOOLS.items():
        score = 0

        # Normalize title, description, and keywords
        title_tokens = tool["title"].lower().split()
        description_tokens = tool["description"].lower().split()
        keyword_tokens = [kw.lower() for kw in tool.get("keywords", [])]

        # Match full query in title, description, or keywords
        if query in tool["title"].lower():
            score += 100  # Highest weight for exact match in title
        if query in tool["description"].lower():
            score += 70  # Medium weight for exact match in description
        if any(query in keyword for keyword in keyword_tokens):
            score += 50  # Lower weight for exact match in keywords

        # Match individual tokens in title, description, or keywords
        for token in query_tokens:
            if token in title_tokens:
                score += 20
            if token in description_tokens:
                score += 15
            if any(token in keyword for keyword in keyword_tokens):
                score += 10

        # Add result if score is greater than 0
        if score > 0:
            results.append({
                "name": tool["title"],
                "url": tool['url'],
                "description": tool["description"],
                "score": score
            })

    # Sort results by score in descending order
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return render_template("search.html", results=results, query=query)

@search_routes.route("/suggest", methods=["GET"])
def suggest():
    logger.info("Handling suggestion request")
    query = request.args.get("q", "").strip().lower()

    if not query:
        return jsonify([])

    query_tokens = query.split()
    suggestions = []

    for tool_key, tool in ALL_TOOLS.items():
        score = 0

        # Normalize title, description, and keywords
        title_tokens = tool["title"].lower().split()
        description_tokens = tool["description"].lower().split()
        keyword_tokens = [kw.lower() for kw in tool.get("keywords", [])]

        # Match full query in title, description, or keywords
        if query in tool["title"].lower():
            score += 100
        if query in tool["description"].lower():
            score += 70
        if any(query in keyword for keyword in keyword_tokens):
            score += 50

        # Match individual tokens
        for token in query_tokens:
            if token in title_tokens:
                score += 20
            if token in description_tokens:
                score += 15
            if any(token in keyword for keyword in keyword_tokens):
                score += 10

        # Add suggestion if score > 0
        if score > 0:
            suggestions.append({
                "name": tool["title"],
                "url": tool["url"],
                "description": tool["description"],
            })

    # Sort suggestions by relevance
    suggestions = sorted(suggestions, key=lambda x: x["name"])
    logger.info(f"Returning {len(suggestions)} suggestions")
    logger.info(suggestions)
    return jsonify(suggestions)
