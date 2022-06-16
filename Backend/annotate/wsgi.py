from annotate import create_app
from annotate.extensions import db

app = create_app()
with app.app_context():
    db.create_all()
