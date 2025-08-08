# run.py
from app import create_app, db
from app.models import Depoimento, Post

app = create_app()

@app.cli.command("seed-db")
def seed_db():
    """Semeia o banco de dados com dados iniciais."""
    # Limpa dados existentes para evitar duplicatas
    db.session.query(Depoimento).delete()
    db.session.query(Post).delete()

    depoimentos = [
        Depoimento(quote="A mentoria do CPI foi um divisor de águas para nós. Aprendemos a dialogar em vez de brigar e a colocar Deus no centro de tudo.", author="João & Maria S."),
        Depoimento(quote="Estávamos quase desistindo, mas encontramos no CPI a esperança e as ferramentas que precisávamos. Hoje, nosso casamento é mais forte do que nunca.", author="Pedro & Ana L."),
        Depoimento(quote="Como noivos, fazer a mentoria nos deu uma base sólida e realista para o casamento. Entramos nessa nova fase muito mais seguros e alinhados.", author="Lucas & Gabriela F.")
    ]
    
    for d in depoimentos:
        db.session.add(d)

    db.session.commit()
    print("Banco de dados semeado com depoimentos!")


# === ADICIONE ESTE BLOCO NO FINAL ===
if __name__ == '__main__':
    app.run(debug=True)