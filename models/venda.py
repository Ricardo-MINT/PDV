"""
Modelos de Venda - Cabeçalho e Itens
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database.db import Base

class Venda(Base):
    __tablename__ = 'vendas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_venda = Column(Integer, unique=True, nullable=False, index=True)
    
    # Informações da venda
    data_venda = Column(DateTime, default=datetime.now, nullable=False)
    valor_total = Column(Float, nullable=False)
    valor_desconto = Column(Float, default=0.0)
    valor_final = Column(Float, nullable=False)
    
    # Pagamento
    forma_pagamento = Column(String(20), default='DINHEIRO')  # DINHEIRO, PIX, CARTAO_CREDITO, CARTAO_DEBITO
    valor_pago = Column(Float, nullable=False)
    troco = Column(Float, default=0.0)
    
    # Cliente (opcional para MVP)
    nome_cliente = Column(String(120), nullable=True)
    cpf_cliente = Column(String(11), nullable=True)
    
    # Status fiscal (para expansão futura)
    status_fiscal = Column(String(20), default='SEM_EMISSAO')  # SEM_EMISSAO, EMITIDA, CANCELADA, DENEGADA
    chave_nfe = Column(String(44), nullable=True)
    numero_nfe = Column(Integer, nullable=True)
    
    # Relacionamentos
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")
    
    # Auditoria
    usuario = Column(String(50), default='CAIXA')
    observacoes = Column(Text, nullable=True)
    
    def __repr__(self):
        return f"<Venda #{self.numero_venda}: R$ {self.valor_final:.2f}>"
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero_venda': self.numero_venda,
            'data_venda': self.data_venda.strftime('%d/%m/%Y %H:%M:%S'),
            'valor_total': self.valor_total,
            'valor_desconto': self.valor_desconto,
            'valor_final': self.valor_final,
            'forma_pagamento': self.forma_pagamento,
            'troco': self.troco,
            'status_fiscal': self.status_fiscal
        }


class ItemVenda(Base):
    __tablename__ = 'itens_venda'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    venda_id = Column(Integer, ForeignKey('vendas.id'), nullable=False)
    produto_id = Column(Integer, ForeignKey('produtos.id'), nullable=False)
    
    # Informações do item
    sequencia = Column(Integer, nullable=False)  # Ordem do item na venda
    codigo_barras = Column(String(13), nullable=False)
    descricao = Column(String(120), nullable=False)
    quantidade = Column(Float, nullable=False)
    preco_unitario = Column(Float, nullable=False)
    preco_total = Column(Float, nullable=False)
    desconto_item = Column(Float, default=0.0)
    
    # Relacionamentos
    venda = relationship("Venda", back_populates="itens")
    
    def __repr__(self):
        return f"<ItemVenda: {self.descricao} x{self.quantidade}>"
    
    def to_dict(self):
        return {
            'sequencia': self.sequencia,
            'codigo_barras': self.codigo_barras,
            'descricao': self.descricao,
            'quantidade': self.quantidade,
            'preco_unitario': self.preco_unitario,
            'preco_total': self.preco_total
        }