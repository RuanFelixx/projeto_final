from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from app import db

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'tb_clientes'
    cli_id = Column(Integer, primary_key=True, autoincrement=True)
    cli_nome = Column(String(100), nullable=False)
    cli_email = Column(String(255), nullable=False, unique=True)
    cli_telefone = Column(String(15), nullable=False)
    cli_endereco = Column(Text, nullable=False)

class Produto(Base):
    __tablename__ = 'tb_produtos'
    pro_id = Column(Integer, primary_key=True, autoincrement=True)
    pro_nome = Column(String(200), nullable=False)
    pro_desc = Column(Text, nullable=False)
    pro_quantidade = Column(Integer, nullable=False)
    pro_preco = Column(Numeric(10, 2), nullable=False)
   
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Pedido(Base):
    __tablename__ = 'tb_pedidos'
    ped_id = Column(Integer, primary_key=True, autoincrement=True)
    ped_cli_id = Column(Integer, ForeignKey('tb_clientes.cli_id'), nullable=False)
    ped_data = Column(DateTime, nullable=False, default=func.current_timestamp())
    ped_total = Column(Numeric(10, 2), nullable=False)
    cliente = relationship('Cliente', backref='pedidos')

class ProdutoPorPedido(Base):
    __tablename__ = 'tb_proPed'
    proPed_id = Column(Integer, primary_key=True, autoincrement=True)
    proPed_ped_id = Column(Integer, ForeignKey('tb_pedidos.ped_id'), nullable=False)
    proPed_pro_id = Column(Integer, ForeignKey('tb_produtos.pro_id'), nullable=False)
    proPed_qdproduto = Column(Integer, nullable=False)
    proPed_subtotal = Column(Numeric(10, 2), nullable=False)
    pedido = relationship('Pedido', backref='produtos_pedidos')
    produto = relationship('Produto', backref='produtos_por_pedido')

class Usuario(Base):
    __tablename__ = 'tb_usuarios'
    usu_id = Column(Integer, primary_key=True, autoincrement=True)
    usu_nome = Column(String(150), nullable=False)
    usu_email = Column(String(150), nullable=False)
    usu_senha = Column(String(500), nullable=False)

# Conexão com o banco de dados SQLite
engine = create_engine('sqlite:///db_pedidos.db', echo=True)

# Criação das tabelas no banco de dados
Base.metadata.create_all(engine)
