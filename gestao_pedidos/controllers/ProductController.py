from flask import request, redirect, url_for, render_template, session, flash, Blueprint
from flask_login import login_required, current_user
from extensions import db
from models.models import Produto

produto_bp = Blueprint('produtos', __name__)

@produto_bp.route('/cadastrar_produto', methods=['GET', 'POST'])
def cadastrar_produto():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        preco = float(request.form['precouni'])  # Converter para float
        quantidade = int(request.form['quantidade'])  # Converter para int

        produto = Produto(nome=nome, descricao=descricao, preco=preco, quantidade=quantidade)
        produto.save()  # Salvar no banco de dados

        return redirect(url_for('home'))
    
    return render_template('cadastrar_produto.html')

@produto_bp.route('/listar_produtos', methods=['GET', 'POST'])
def listar_produtos():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))
    
    if 'produtos_adicionados' not in session:
        session['produtos_adicionados'] = []

    if request.method == 'POST':
        pro_id = int(request.form['pro_id'])
        pro_nome = request.form['pro_nome']
        pro_preco = float(request.form['pro_preco'])
        quantidade = int(request.form['quantidade'])

        produto_existente = next((prod for prod in session['produtos_adicionados'] if prod['pro_id'] == pro_id), None)

        if produto_existente:
            produto_existente['pro_qdproduto'] += quantidade
            produto_existente['pro_subtotal'] = produto_existente['pro_qdproduto'] * produto_existente['pro_preco']
        else:
            produto = {
                'pro_id': pro_id,
                'pro_nome': pro_nome,
                'pro_preco': pro_preco,
                'pro_qdproduto': quantidade,
                'pro_subtotal': pro_preco * quantidade
            }
            session['produtos_adicionados'].append(produto)

        session.modified = True
        return redirect(url_for('listar_produtos'))

    produtos = Produto.query.order_by(Produto.pro_nome.asc()).all()
    return render_template('listar_produtos.html', dados=produtos)

@produto_bp.route('/editar_produto/<int:pro_id>', methods=['GET', 'POST'])
def editar_produto(pro_id):
    if not current_user.is_authenticated:
        return redirect(url_for('register'))

    produto = Produto.query.get(pro_id)
    if not produto:
        flash("Produto não encontrado.", "danger")
        return redirect(url_for('listar_produtos'))

    if request.method == 'POST':
        produto.pro_nome = request.form['nome']
        produto.pro_desc = request.form['descricao']
        produto.pro_preco = float(request.form['precouni'])  # Converter para float
        produto.pro_quantidade = int(request.form['quantidade'])  # Converter para int
        produto.save()  # Atualiza o produto no banco de dados

        flash("Produto atualizado com sucesso!", "success")
        return redirect(url_for('listar_produtos'))

    return render_template('editar_produto.html', produto=produto)

@produto_bp.route('/excluir_produto/<int:pro_id>', methods=['GET', 'POST'])
def excluir_produto(pro_id):
    produto = Produto.query.get(pro_id)
    if produto:
        produto.delete()  # Exclui o produto do banco de dados
        flash("Produto excluído com sucesso!", "success")
    else:
        flash("Produto não encontrado.", "danger")
    
    return redirect(url_for('listar_produtos'))
