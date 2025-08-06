from flask import Flask, render_template

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

# Define a rota para a página inicial ("/")
@app.route('/')
def home():
    # Renderiza (exibe) o arquivo index.html da pasta 'templates'
    return render_template('index.html')

# Permite que o script seja executado diretamente
if __name__ == '__main__':
    app.run(debug=True)