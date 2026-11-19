"""Ponto de entrada. Local: `flask --app wsgi run --debug`. PythonAnywhere: `from wsgi import app as application`."""
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
