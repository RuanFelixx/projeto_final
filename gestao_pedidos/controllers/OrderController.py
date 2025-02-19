from ..extensions import db
from ..models.models import Cliente, Produto, Pedido, ProdutoPorPedido, Usuario
from flask import request, render_template, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user

pedidos_bp = Blueprint(name ='pedidos',import_name = __name__)

@pedidos_bp.route('/cadastrar_pedido', methods=['GET', 'POST'])
@login_required
def cadastrar_pedido():
    clientes = Cliente.query.all()
    produtos = Produto.query.all()

    if request.method == 'POST':
        data = request.form.get('data')
        cli_id = int(request.form.get('cli_id'))
        produtos_selecionados = []
        total_pedido = 0

        for produto in produtos:
            produto_id = str(produto.pro_id)
            if produto_id in request.form.getlist('produtos'):
                quantidade = int(request.form.get(f'quantidade_{produto_id}', 1))
                subtotal = produto.pro_preco * quantidade
                total_pedido += subtotal
                produtos_selecionados.append({'id': produto.pro_id, 'quantidade': quantidade, 'subtotal': subtotal})

        novo_pedido = Pedido(cli_id=cli_id, ped_data=data, ped_total=total_pedido)
        db.session.add(novo_pedido)
        db.session.commit()

        # Associando os produtos ao pedido
        for produto_selecionado in produtos_selecionados:
            produto_por_pedido = ProdutoPorPedido(
                proPed_ped_id=novo_pedido.ped_id,
                proPed_pro_id=produto_selecionado['id'],
                proPed_qdproduto=produto_selecionado['quantidade'],
                proPed_subtotal=produto_selecionado['subtotal']
            )
            db.session.add(produto_por_pedido)

        db.session.commit()

        flash("Pedido cadastrado com sucesso!", 'success')
        return redirect(url_for('pedidos.listar_pedidos'))

    return render_template('cadastrar_pedido.html', clientes=clientes, produtos=produtos)

@pedidos_bp.route('/listar_pedidos', methods=['GET'])
@login_required
def listar_pedidos():
    ordem = request.args.get('ordem', 'asc')
    pedidos = Pedido.query.order_by(Pedido.ped_data.asc() if ordem == 'asc' else Pedido.ped_data.desc()).all()
    return render_template('listar_pedidos.html', pedidos=pedidos, ordem=ordem)

@pedidos_bp.route('/editar_pedido/<int:ped_id>', methods=['GET', 'POST'])
@login_required
def editar_pedido(ped_id):
    pedido = Pedido.query.get_or_404(ped_id)
    clientes = Cliente.query.all()

    if request.method == 'POST':
        pedido.cli_id = request.form.get('cli_id')
        pedido.ped_data = request.form.get('data')
        db.session.commit()
        flash("Pedido atualizado com sucesso!", "success")
        return redirect(url_for('pedidos.listar_pedidos'))

    return render_template('editar_pedido.html', pedido=pedido, clientes=clientes)

@pedidos_bp.route('/excluir_pedido/<int:ped_id>', methods=['POST'])
@login_required
def excluir_pedido(ped_id):
    pedido = Pedido.query.get_or_404(ped_id)

    # Excluindo produtos associados ao pedido
    ProdutoPorPedido.query.filter_by(proPed_ped_id=ped_id).delete()

    db.session.delete(pedido)
    db.session.commit()
    flash("Pedido excluído com sucesso!", "success")
    return redirect(url_for('pedidos.listar_pedidos'))
