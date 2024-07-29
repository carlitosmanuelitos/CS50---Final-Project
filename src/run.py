"""
Entry point for the Stock AI Portfolio Tracking app.

This script initializes and runs the Flask application. It imports the `create_app` function
from the `app` package to create an instance of the app. The script also prints various
informative details about the application, such as the current working directory, template
folder, static folder, available templates, registered blueprints, and URL map.
"""
import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from src.app import create_app

app = create_app()

if __name__ == '__main__':
    print("Current working directory:", os.getcwd())
    print("Template folder:", app.template_folder)
    print("Static folder:", app.static_folder)
    print("Available templates:", os.listdir(app.template_folder))
    print("Registered blueprints:", list(app.blueprints.keys()))
    print("URL Map:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")
    app.run(debug=True, port=5001)