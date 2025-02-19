from ..extensions import db
from ..models.models import Cliente, Produto, Pedido, ProdutoPorPedido, Usuario
from flask import render_template, redirect, url_for, request, flash, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

usuarios_bp = Blueprint(name = 'usuarios', import_name = __name__)

@usuarios_bp.route('/home')
@login_required
def home():
    return render_template("home.html")

@usuarios_bp.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['password']
        senha_hash = generate_password_hash(senha)

        # Verifica se o usuário já existe
        user = Usuario.query.filter_by(email=email).first()
        if user:
            flash("O usuário já está cadastrado!", "danger")
        else:
            novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash)
            db.session.add(novo_usuario)
            db.session.commit()  # Confirma a adição no banco de dados
            flash("Registro efetuado com sucesso! Use suas credenciais para fazer login.", "success")
            return redirect(url_for("usuarios.login"))
    
    return render_template("register.html")

@usuarios_bp.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        senha = request.form['password']
        
        # Busca o usuário pelo e-mail
        user = Usuario.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.senha, senha):
            login_user(user)  # Realiza o login do usuário
            return redirect(url_for("usuarios.home"))
        else:
            flash("Email ou senha incorretos. Verifique suas credenciais e tente novamente.", "danger")
    
    return render_template("login.html")

@usuarios_bp.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()  # Realiza o logout
    return redirect(url_for("usuarios.login"))
