from ..extensions import db
from ..models.models import Cliente, Produto, Pedido, ProdutoPorPedido, Usuario
from flask import render_template, request, flash, redirect, url_for, Blueprint
from flask_login import login_required, current_user
from sqlalchemy import func

relatorios_bp = Blueprint(name ='relatorios',import_name = __name__)

@relatorios_bp.route('/relatorios', methods=['GET', 'POST'])
@login_required
def relatorios():
    if not current_user.is_authenticated:
        return redirect(url_for('register'))
    
    resultado = None
    
    if request.method == 'POST':
        filtro = request.form.get('filtro')

        try:
            if filtro == 'total_vendas_cliente':
                # Relatório de total de vendas por cliente
                resultado = (
                    db.session.query(Cliente.cli_nome, func.sum(Pedido.ped_total).label("total_vendas"))
                    .join(Pedido, Cliente.cli_id == Pedido.ped_cli_id)
                    .group_by(Cliente.cli_nome)
                    .all()
                )

            elif filtro == 'clientes_acima_1000':
                # Relatório de clientes que gastaram mais de 1000
                resultado = (
                    db.session.query(Cliente.cli_nome, func.sum(Pedido.ped_total).label("total_vendas"))
                    .join(Pedido, Cliente.cli_id == Pedido.ped_cli_id)
                    .group_by(Cliente.cli_nome)
                    .having(func.sum(Pedido.ped_total) > 1000)
                    .all()
                )

            elif filtro == 'top_produtos':
                # Relatório dos 10 produtos mais vendidos nos últimos 30 dias
                resultado = (
                    db.session.query(Produto.pro_nome, func.sum(ProdutoPorPedido.proPed_qdproduto).label("qtd_total"))
                    .join(ProdutoPorPedido, Produto.pro_id == ProdutoPorPedido.proPed_pro_id)
                    .join(Pedido, ProdutoPorPedido.proPed_ped_id == Pedido.ped_id)
                    .filter(Pedido.ped_data.between(func.date_sub(func.now(), func.interval(30, 'DAY')), func.now()))
                    .group_by(Produto.pro_nome)
                    .order_by(func.sum(ProdutoPorPedido.proPed_qdproduto).desc())
                    .limit(10)
                    .all()
                )

            elif filtro == 'produtos_nao_vendidos':
                # Relatório de produtos não vendidos nos últimos 30 dias
                resultado = (
                    db.session.query(Produto.pro_nome)
                    .filter(~Produto.pro_id.in_(
                        db.session.query(ProdutoPorPedido.proPed_pro_id)
                        .join(Pedido, ProdutoPorPedido.proPed_ped_id == Pedido.ped_id)
                        .filter(Pedido.ped_data.between(func.date_sub(func.now(), func.interval(30, 'DAY')), func.now()))
                    ))
                    .all()
                )
            else:
                flash("Filtro inválido.", 'warning')
        except Exception as e:
            flash(f"Erro ao executar o filtro: {str(e)}", 'danger')

    return render_template('relatorios.html', resultado=resultado)
