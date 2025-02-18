from gestao_pedidos import app
from gestao_pedidos.database.config import db
from gestao_pedidos.models.Cliente import Cliente
from flask import request, render_template, redirect, url_for, flash
from flask_login import login_required,current_user



@app.route('/cadastrar_cliente', methods=['GET', 'POST'])
def cadastrar_cliente():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        endereco = request.form['endereco']
        telefone = request.form['telefone']
        client = Cliente(nome, email, telefone, endereco)
        db.sesseion.add(client)
        de.session.commit()
           
        return redirect(url_for('home'))
    return render_template('cadastrar_cliente.html')



@app.route('/listar_clientes', methods=['GET'])
def listar_clientes():
    # Redireciona para o registro caso o usuário não esteja autenticado
    if not current_user.is_authenticated:
        return redirect(url_for('register'))
        # Pega a ordem da query string, com valor padrão 'asc'
    ordem = request.args.get('ordem', 'asc')

    # Validação da ordem (caso seja passado um valor inesperado)
    if ordem == 'desc':
        dados = Cliente.query.order_by(Cliente.cli_nome.desc()).all()
    else:
        dados = Cliente.query.order_by(Cliente.cli_nome.asc()).all()

    return render_template('listar_clientes.html', dados=dados, ordem=ordem)

@app.route('/editar_cliente/<int:cli_id>', methods=['GET', 'POST'])
def editar_cliente(cli_id):
    if not current_user.is_authenticated:
        return redirect(url_for('register'))

    cliente = Cliente.query.get(cli_id)

    if not cliente:
        flash("cliente não encontrado", "danger")
        return redirect(url_for('listar_clientes'))

    if request.method == 'POST':
        # Atualizando os dados do cliente
        cliente.cli_nome = request.form['nome']
        cliente.cli_email = request.form['email']
        cliente.cli_endereco = request.form['endereco']
        cliente.cli_telefone = request.form['telefone']

        db.sesseion.commit()
        
        flash("Cliente atualizado com sucesso!", "success")
        return redirect(url_for('listar_clientes'))
    
    return render_template('editar_cliente.html', cliente=cliente)


@app.route('/excluir_cliente/<int:cli_id>', methods=['GET', 'POST'])
def excluir_cliente(cli_id):
    if not current_user.is_authenticated:
        return redirect(url_for('register'))

    cliente = Cliente.query.get(cli_id)  # Buscar o cliente pelo ID

    if not cliente:
        flash("Cliente não encontrado.", "danger")
        return redirect(url_for('listar_clientes'))

    # Excluir produtos associados aos pedidos do cliente
    pedidos = Pedido.query.filter_by(ped_cli_id=cli_id).all()
    for pedido in pedidos:
        ProdutoPorPedido.query.filter_by(proPed_ped_id=pedido.ped_id).delete()
        db.session.delete(pedido)

    # Excluir o cliente
    db.session.delete(cliente)
    db.session.commit()

    flash("Cliente e seus dados associados foram excluídos com sucesso!", "success")
    return redirect(url_for('listar_clientes'))
