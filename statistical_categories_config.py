from flask import Blueprint, render_template

tool_category_stat_analysis_routes = Blueprint("tool_category_stat_analysis_routes", __name__)

STAT_ANALYSIS_TOOL_CATEGORIES = {
    # Statistical Analysis Tools
    "statistical-analysis": {
        "title": "Statistical Analysis Tools",
        "description": "Explore tools for statistical analysis, including variability measures and relationships between variables.",
        "parent_category": "analytics",
        "tools": [
            {
                "title": "Variance and Standard Deviation",
                "description": "Calculate variance and standard deviation for a given dataset.",
                "url": "/tools/statistical-analysis/variance_standard_deviation",
            },
            {
                "title": "Covariance",
                "description": "Compute covariance to evaluate the relationship between two variables.",
                "url": "/tools/statistical-analysis/covariance",
            },
            {
                "title": "Correlation",
                "description": "Determine the correlation coefficient to measure the strength of a linear relationship between two variables.",
                "url": "/tools/statistical-analysis/correlation",
            },
        ],
    },
    # Predictive Modeling Tools
    "linear-regression": {
        "title": "Linear Regression Tools",
        "description": "Use linear regression for predictive modeling and analyzing relationships between variables.",
        "parent_category": "predictive-modeling",
        "tools": [
            {
                "title": "Linear Regression",
                "description": "Perform linear regression to predict the relationship between dependent and independent variables.",
                "url": "/tools/linear-regression/linear_regression",
            },
        ],
    },
}

@tool_category_stat_analysis_routes.route("/tools/statistics/<category_key>")
def render_stat_analysis_category(category_key):
    category = STAT_ANALYSIS_TOOL_CATEGORIES.get(category_key)
    if not category:
        return "Category not found", 404
    return render_template("tool_category.html", category=category)
