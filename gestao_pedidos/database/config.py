from gestao_pedidos import app
from flask_mysqldb import MySQL

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_pedidos.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

db = SQLAlchemy(app)