from datetime import datetime
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    
        # Pega o ano atual
    current_year = datetime.now().year
    return render_template('index.html', current_year=current_year)


if __name__ == '__main__':
    app.run(debug=True)