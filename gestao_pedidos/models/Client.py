from gestao_pedidos.database.config import mysql
from flask import flash

class Client:
    def __init__(self, nome, email, telefone, endereco):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.endereco = endereco

    def save(self):
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM tb_clientes WHERE cli_email = %s", (self.email,))
        cliente = cursor.fetchone()

        if cliente:
            flash("O cliente já está cadastrado!", "danger")
        else:
            cursor.execute(
                "INSERT INTO tb_clientes (cli_nome, cli_email, cli_endereco, cli_telefone) VALUES (%s, %s, %s, %s)",
                (self.nome, self.email, self.endereco, self.telefone)
            )
            mysql.connection.commit()
            flash("Cadastro efetuado com sucesso!", "success")
        cursor.close()
        return True

    @staticmethod
    def get_all_clients():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT cli_id, cli_nome FROM tb_clientes ORDER BY cli_nome ASC")
        clientes = cursor.fetchall() 
        cursor.close()
        return clientes
