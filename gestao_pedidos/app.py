from flask import Flask
from extensions import db
from controllers.ClientController import cliente_bp
from controllers.OrderController import pedidos_bp
from controllers.ProductController import produto_bp
from controllers.ReportsController import relatorios_bp
from controllers.UserController import usuarios_bp

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_pedidos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(cliente_bp, url_prefix='/clientes')
app.register_blueprint(pedidos_bp, url_prefix='/pedidos')
app.register_blueprint(produto_bp, url_prefix='/produtos')
app.register_blueprint(relatorios_bp, url_prefix='/relatorios')
app.register_blueprint(usuarios_bp, url_prefix='/usuario')

with app.app_context():
    db.create_all()  # Cria todas as tabelas no banco de dados
    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    app.run(debug=True)