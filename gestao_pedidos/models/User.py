from gestao_pedidos import app
from gestao_pedidos.database.config import mysql
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin):
    def __init__(self, email, nome, senha):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.id = None
    
    @classmethod
    def save(self, nome, email, senha_hash):
        cursor = mysql.connection.cursor()
        INSERT = "INSERT INTO tb_usuarios (usu_nome, usu_email, usu_senha) VALUES (%s,%s,%s)"
        cursor.execute(INSERT, (nome, email, senha_hash))
        mysql.connection.commit()
        cursor.close()
        return True
    
    @classmethod
    def get(cls, id):
        cursor = mysql.connection.cursor()
        SELECT = "SELECT * FROM tb_usuarios WHERE usu_id = %s"
        cursor.execute(SELECT, (id,))
        dados = cursor.fetchone()
        cursor.close()
        if dados:
            user = User(dados["usu_nome"], dados['usu_email'], dados['usu_senha'])
            user.id = dados['usu_id']
            return user
        return None

    @classmethod
    def get_by_email(cls, email):
        cursor = mysql.connection.cursor()
        SELECT = "SELECT * FROM tb_usuarios WHERE usu_email = %s"
        cursor.execute(SELECT, (email,))
        dados = cursor.fetchone()
        cursor.close()
        if dados:
            user = User(dados["usu_nome"], dados['usu_email'], dados['usu_senha'])
            user.id = dados['usu_id']
            return user
        return None
    
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
