from app import create_app
import os

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