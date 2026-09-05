"""
Controller do PDV - Lógica de Negócio
Implementa a "Regra do 100% ou 0%" com transações atômicas
"""
from sqlalchemy.exc import SQLAlchemyError
from models.produto import Produto
from models.venda import Venda, ItemVenda
from database.db import get_db
from utils.log_config import logger, log_venda, log_produto_cadastrado
from datetime import datetime

class PDVController:
    """Controlador principal do sistema PDV"""
    
    def __init__(self):
        self.db = get_db()
        self.venda_atual = None
        self.itens_venda = []
        self.sequencia_item = 0
        logger.info("PDVController inicializado")
    
    # ==================== PRODUTOS ====================
    
    def cadastrar_produto(self, dados_produto):
        """
        Cadastra um novo produto no sistema
        Retorna: (sucesso: bool, mensagem: str, produto: Produto ou None)
        """
        try:
            # Verificar se código de barras já existe
            existente = self.db.query(Produto).filter_by(
                codigo_barras=dados_produto['codigo_barras']
            ).first()
            
            if existente:
                return False, "Código de barras já cadastrado!", None
            
            # Criar novo produto
            produto = Produto(
                codigo_barras=dados_produto['codigo_barras'],
                descricao=dados_produto['descricao'],
                preco_venda=float(dados_produto['preco_venda']),
                unidade=dados_produto.get('unidade', 'UN'),
                estoque_atual=float(dados_produto.get('estoque_atual', 0)),
                ncm=dados_produto.get('ncm', ''),
                cfop=dados_produto.get('cfop', '5102'),
                csosn=dados_produto.get('csosn', '102')
            )
            
            self.db.add(produto)
            self.db.commit()
            self.db.refresh(produto)
            
            log_produto_cadastrado(produto.to_dict())
            return True, "Produto cadastrado com sucesso!", produto
            
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao cadastrar produto: {str(e)}")
            return False, f"Erro ao cadastrar: {str(e)}", None
    
    def buscar_produto(self, codigo_barras):
        """
        Busca produto por código de barras
        Retorna: Produto ou None
        """
        try:
            produto = self.db.query(Produto).filter_by(
                codigo_barras=codigo_barras,
                ativo=True
            ).first()
            
            if produto:
                logger.debug(f"Produto encontrado: {produto.descricao}")
            else:
                logger.warning(f"Produto não encontrado: {codigo_barras}")
            
            return produto
            
        except Exception as e:
            logger.error(f"Erro ao buscar produto: {str(e)}")
            return None
    
    def listar_produtos(self, filtro=''):
        """Lista produtos ativos com filtro opcional"""
        try:
            query = self.db.query(Produto).filter_by(ativo=True)
            
            if filtro:
                query = query.filter(
                    (Produto.descricao.ilike(f'%{filtro}%')) |
                    (Produto.codigo_barras.ilike(f'%{filtro}%'))
                )
            
            return query.all()
            
        except Exception as e:
            logger.error(f"Erro ao listar produtos: {str(e)}")
            return []
    
    # ==================== VENDA ====================
    
    def nova_venda(self):
        """Inicia uma nova venda"""
        self.itens_venda = []
        self.sequencia_item = 0
        logger.info("Nova venda iniciada")
        return True
    
    def adicionar_item(self, codigo_barras, quantidade=1):
        """
        Adiciona item à venda atual
        Retorna: (sucesso: bool, mensagem: str, item_dict ou None)
        """
        try:
            # Buscar produto
            produto = self.buscar_produto(codigo_barras)
            if not produto:
                return False, "Produto não encontrado!", None
            
            # Verificar estoque (opcional para MVP)
            if produto.estoque_atual < quantidade:
                logger.warning(f"Estoque insuficiente: {produto.descricao}")
                # Não bloqueia para MVP, apenas avisa
            
            # Criar item
            self.sequencia_item += 1
            item = {
                'sequencia': self.sequencia_item,
                'codigo_barras': produto.codigo_barras,
                'descricao': produto.descricao,
                'quantidade': quantidade,
                'preco_unitario': produto.preco_venda,
                'preco_total': produto.preco_venda * quantidade,
                'produto_id': produto.id
            }
            
            self.itens_venda.append(item)
            logger.debug(f"Item adicionado: {item['descricao']} x{quantidade}")
            
            return True, "Item adicionado!", item
            
        except Exception as e:
            logger.error(f"Erro ao adicionar item: {str(e)}")
            return False, f"Erro: {str(e)}", None
    
    def remover_item(self, sequencia):
        """Remove item da venda por sequência"""
        try:
            self.itens_venda = [i for i in self.itens_venda if i['sequencia'] != sequencia]
            logger.debug(f"Item {sequencia} removido")
            return True, "Item removido!"
        except Exception as e:
            logger.error(f"Erro ao remover item: {str(e)}")
            return False, f"Erro: {str(e)}"
    
    def calcular_totais(self, desconto_percentual=0):
        """
        Calcula totais da venda
        Retorna: dict com valor_total, valor_desconto, valor_final
        """
        valor_total = sum(item['preco_total'] for item in self.itens_venda)
        valor_desconto = valor_total * (desconto_percentual / 100)
        valor_final = valor_total - valor_desconto
        
        return {
            'valor_total': valor_total,
            'valor_desconto': valor_desconto,
            'valor_final': valor_final
        }
    
    def calcular_troco(self, valor_final, valor_pago):
        """Calcula troco"""
        return max(0, valor_pago - valor_final)
    
    def finalizar_venda(self, forma_pagamento, valor_pago, desconto_percentual=0):
        """
        Finaliza venda com transação atômica (100% ou 0%)
        Retorna: (sucesso: bool, mensagem: str, venda_dict ou None)
        """
        try:
            if not self.itens_venda:
                return False, "Nenhum item na venda!", None
            
            # Calcular totais
            totais = self.calcular_totais(desconto_percentual)
            valor_final = totais['valor_final']
            
            # Validar pagamento
            if valor_pago < valor_final:
                return False, f"Valor insuficiente! Falta R$ {valor_final - valor_pago:.2f}", None
            
            troco = self.calcular_troco(valor_final, valor_pago)
            
            # Obter próximo número de venda
            ultima_venda = self.db.query(Venda).order_by(Venda.numero_venda.desc()).first()
            proximo_numero = (ultima_venda.numero_venda + 1) if ultima_venda else 1
            
            # TRANSAÇÃO ATÔMICA - Começa aqui
            venda = Venda(
                numero_venda=proximo_numero,
                valor_total=totais['valor_total'],
                valor_desconto=totais['valor_desconto'],
                valor_final=valor_final,
                forma_pagamento=forma_pagamento,
                valor_pago=valor_pago,
                troco=troco,
                data_venda=datetime.now()
            )
            
            self.db.add(venda)
            self.db.flush()  # Garante que venda.id está disponível
            
            # Adicionar itens
            for item_data in self.itens_venda:
                item = ItemVenda(
                    venda_id=venda.id,
                    produto_id=item_data['produto_id'],
                    sequencia=item_data['sequencia'],
                    codigo_barras=item_data['codigo_barras'],
                    descricao=item_data['descricao'],
                    quantidade=item_data['quantidade'],
                    preco_unitario=item_data['preco_unitario'],
                    preco_total=item_data['preco_total']
                )
                self.db.add(item)
            
            # Commit da transação
            self.db.commit()
            self.db.refresh(venda)
            
            # Log da venda
            log_venda(venda.to_dict())
            
            # Limpar venda atual
            self.nova_venda()
            
            return True, f"Venda finalizada! Troco: R$ {troco:.2f}", venda.to_dict()
            
        except SQLAlchemyError as e:
            self.db.rollback()
            logger.error(f"Erro no banco de dados: {str(e)}")
            return False, "Erro ao finalizar venda! Transação cancelada.", None
        except Exception as e:
            self.db.rollback()
            logger.error(f"Erro ao finalizar venda: {str(e)}")
            return False, f"Erro: {str(e)}", None
    
    def cancelar_venda(self):
        """Cancela a venda atual"""
        self.nova_venda()
        logger.info("Venda cancelada")
        return True, "Venda cancelada!"
    
    # ==================== CONSULTAS ====================
    
    def listar_vendas(self, data_inicio=None, data_fim=None):
        """Lista vendas por período"""
        try:
            query = self.db.query(Venda)
            
            if data_inicio:
                query = query.filter(Venda.data_venda >= data_inicio)
            if data_fim:
                query = query.filter(Venda.data_venda <= data_fim)
            
            return query.order_by(Venda.data_venda.desc()).all()
            
        except Exception as e:
            logger.error(f"Erro ao listar vendas: {str(e)}")
            return []
    
    def __del__(self):
        """Fecha conexão com banco ao destruir controller"""
        if hasattr(self, 'db'):
            self.db.close()