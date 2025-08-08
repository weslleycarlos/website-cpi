# run.py
from app import create_app, db
from app.models import Depoimento, Post

app = create_app()

# === ADICIONE ESTE BLOCO NO FINAL ===
if __name__ == '__main__':
    app.run(debug=True)