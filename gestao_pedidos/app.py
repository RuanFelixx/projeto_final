from flask import Flask, render_template
from flask_login import login_manager
from .extensions import db
from .models.User import User
from .controllers.ClientController import cliente_bp
from .controllers.OrderController import pedidos_bp
from .controllers.ProductController import produto_bp
from .controllers.ReportsController import relatorios_bp
from .controllers.UserController import usuarios_bp

app = Flask(__name__)

app.config['SECRET_KEY'] = 'TEO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_pedidos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  

app.register_blueprint(cliente_bp, url_prefix='/clientes')
app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
app.register_blueprint(produto_bp, url_prefix='/produtos')
app.register_blueprint(relatorios_bp, url_prefix='/relatorios')
app.register_blueprint(usuarios_bp, url_prefix='/usuario')

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


login_manager.init_app(app)


@app.route('/')
def index():
    return render_template('home.html')
    
with app.app_context():
    db.create_all()  
    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    app.run(debug=True)
