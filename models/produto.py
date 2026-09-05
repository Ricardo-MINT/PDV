"""
Modelo de Produto - Inclui campos fiscais para expansão futura
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime
from database.db import Base

class Produto(Base):
    __tablename__ = 'produtos'
    
    # Identificação básica
    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo_barras = Column(String(13), unique=True, nullable=False, index=True)  # EAN-13
    descricao = Column(String(120), nullable=False)
    unidade = Column(String(6), default='UN')  # UN, KG, LT, etc
    preco_venda = Column(Float, nullable=False)
    estoque_atual = Column(Float, default=0)
    ativo = Column(Boolean, default=True)
    
    # Campos fiscais (preparados para integração futura)
    ncm = Column(String(8), nullable=True)  # Nomenclatura Comum do Mercosul
    cest = Column(String(7), nullable=True)  # Código Especificador da ST
    cfop = Column(String(4), default='5102')  # Venda merc. adq. ou rec. de terceiros
    origem = Column(String(1), default='0')  # 0=Nacional
    
    # CST/CSOSN - Situação Tributária
    # Para Simples Nacional usar CSOSN, para Regime Normal usar CST
    csosn = Column(String(3), default='102')  # 102=Sem cálculo de ICMS
    cst_icms = Column(String(2), nullable=True)
    cst_pis = Column(String(2), default='07')  # 07=Não tributado
    cst_cofins = Column(String(2), default='07')
    
    # Alíquotas (em percentual)
    aliquota_icms = Column(Float, default=0.0)
    aliquota_pis = Column(Float, default=0.0)
    aliquota_cofins = Column(Float, default=0.0)
    
    # Auditoria
    data_cadastro = Column(DateTime, default=datetime.now)
    data_alteracao = Column(DateTime, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Produto {self.codigo_barras}: {self.descricao}>"
    
    def to_dict(self):
        """Converte produto para dicionário"""
        return {
            'id': self.id,
            'codigo_barras': self.codigo_barras,
            'descricao': self.descricao,
            'preco_venda': self.preco_venda,
            'estoque_atual': self.estoque_atual,
            'unidade': self.unidade,
            'ncm': self.ncm,
            'cfop': self.cfop
        }