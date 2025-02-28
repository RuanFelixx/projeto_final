from gestao_pedidos.database.config import mysql
from flask import flash


class Products:
    def __init__(self, nome, descricao, preco, quantidade):
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade = quantidade

    def save(self):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO tb_produtos (pro_nome, pro_desc, pro_preco, pro_quantidade) VALUES (%s, %s, %s, %s)",
            (self.nome, self.descricao, self.preco, self.quantidade)
        )
        mysql.connection.commit()
        cursor.close()
        flash("Produto cadastrado com sucesso!", "success")
        return True