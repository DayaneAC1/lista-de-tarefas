from flask import Flask, render_template, request, url_for, redirect, flash, session
import database
app = Flask(__name__)
app.secret_key = "chave_muito_segura"

@app.route('/') #rota para a página inicial
def index():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"]) #rota para a página de login
def login():
    if request.method == "POST":
        form = request.form
        if database.verificar_usuario(form) == True:
            session['email'] = form['email']
            return redirect("/home")
        else:
            return redirect("/login")
    else:    
        return render_template('login.html')

@app.route('/home')
def home():
    musicas = database.pegar_musicas(session['email'])
    return render_template('home.html', musicas=musicas)

@app.route('/cadastro', methods=["GET", "POST"]) #rota para a página de login
def cadastro():
    if request.method == "POST":
        form = request.form
        if database.criar_usuario(form) == True:
            return render_template('login.html')
        else:
            return "Ocorreu um erro ao cadastrar usuário."
    else:    
        return render_template('cadastro.html')
    
@app.route('/criar-musica', methods=["GET", "POST"])
def criar_musica():
    if request.method == "POST":
        form = request.form
        database.criar_musica(form, session['email'])
        return redirect("/home")
    else:
        return render_template("criar_musica.html")

@app.route('/editar-musica/<int:id>', methods=["GET"])
def editar_musica(id):
    if database.editar_musica(id):
        return redirect(url_for('home'))
    else:
        return "Ocorreu um erro ao editar a música."
    

# parte principal do
if __name__ == '__main__':
    app.run(debug=True)