# Importe as funções 'request' e 'redirect' do Flask
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Nova rota para lidar com o formulário
@app.route('/enviar_contato', methods=['POST'])
def enviar_contato():
    # A mágica acontece aqui!
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        mensagem = request.form['mensagem']
        
        # POR ENQUANTO: Vamos apenas imprimir no terminal para ver se funcionou
        print(f"Nova mensagem de contato:")
        print(f"Nome: {nome}")
        print(f"Email: {email}")
        print(f"Mensagem: {mensagem}")
        
        # Futuramente, aqui você pode adicionar o código para enviar um e-mail.
        
        # Redireciona o usuário de volta para a página inicial
        return redirect('/#contato')

if __name__ == '__main__':
    app.run(debug=True)