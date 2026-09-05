"""
Interface Principal do PDV - PyQt5
Foco em atalhos de teclado e operação rápida
"""
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QPushButton, QTableWidget, 
                             QTableWidgetItem, QMessageBox, QInputDialog,
                             QComboBox, QDialog, QFormLayout, QDoubleSpinBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QKeySequence
from controllers.pdv_controller import PDVController
from utils.log_config import logger

class PDVWindow(QMainWindow):
    """Janela principal do PDV"""
    
    def __init__(self):
        super().__init__()
        self.controller = PDVController()
        self.init_ui()
        self.controller.nova_venda()
        logger.info("Interface PDV inicializada")
    
    def init_ui(self):
        """Configura a interface"""
        self.setWindowTitle("Sistema PDV - MVP")
        self.setGeometry(100, 100, 1000, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # ========== CABEÇALHO ==========
        header_layout = QHBoxLayout()
        
        # Entrada de código de barras
        barcode_layout = QVBoxLayout()
        barcode_label = QLabel("Código de Barras [F1]:")
        barcode_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.barcode_input = QLineEdit()
        self.barcode_input.setFont(QFont("Arial", 14))
        self.barcode_input.setPlaceholderText("Digite ou escaneie o código...")
        self.barcode_input.returnPressed.connect(self.adicionar_item)
        barcode_layout.addWidget(barcode_label)
        barcode_layout.addWidget(self.barcode_input)
        
        # Quantidade
        qtd_layout = QVBoxLayout()
        qtd_label = QLabel("Qtd [F2]:")
        qtd_label.setFont(QFont("Arial", 10, QFont.Bold))
        self.qtd_input = QLineEdit("1")
        self.qtd_input.setFont(QFont("Arial", 14))
        self.qtd_input.setMaximumWidth(100)
        qtd_layout.addWidget(qtd_label)
        qtd_layout.addWidget(self.qtd_input)
        
        header_layout.addLayout(barcode_layout, 3)
        header_layout.addLayout(qtd_layout, 1)
        
        main_layout.addLayout(header_layout)
        
        # ========== TABELA DE ITENS ==========
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['Seq', 'Código', 'Descrição', 'Qtd', 'Total'])
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 120)
        self.table.setColumnWidth(2, 400)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 100)
        self.table.setFont(QFont("Arial", 11))
        main_layout.addWidget(self.table)
        
        # ========== TOTALIZADORES ==========
        totais_layout = QHBoxLayout()
        
        # Subtotal
        self.label_subtotal = QLabel("Subtotal: R$ 0,00")
        self.label_subtotal.setFont(QFont("Arial", 16, QFont.Bold))
        
        # Desconto
        self.label_desconto = QLabel("Desconto: R$ 0,00")
        self.label_desconto.setFont(QFont("Arial", 14))
        
        # Total
        self.label_total = QLabel("TOTAL: R$ 0,00")
        self.label_total.setFont(QFont("Arial", 20, QFont.Bold))
        self.label_total.setStyleSheet("color: #2ecc71; background-color: #000; padding: 10px;")
        
        totais_layout.addWidget(self.label_subtotal)
        totais_layout.addWidget(self.label_desconto)
        totais_layout.addStretch()
        totais_layout.addWidget(self.label_total)
        
        main_layout.addLayout(totais_layout)
        
        # ========== BOTÕES DE AÇÃO ==========
        buttons_layout = QHBoxLayout()
        
        # Botão Remover Item
        btn_remover = QPushButton("Remover Item [F3]")
        btn_remover.setFont(QFont("Arial", 12))
        btn_remover.clicked.connect(self.remover_item)
        btn_remover.setStyleSheet("background-color: #e74c3c; color: white; padding: 10px;")
        
        # Botão Desconto
        btn_desconto = QPushButton("Desconto [F4]")
        btn_desconto.setFont(QFont("Arial", 12))
        btn_desconto.clicked.connect(self.aplicar_desconto)
        btn_desconto.setStyleSheet("background-color: #f39c12; color: white; padding: 10px;")
        
        # Botão Cancelar Venda
        btn_cancelar = QPushButton("Cancelar Venda [F8]")
        btn_cancelar.setFont(QFont("Arial", 12))
        btn_cancelar.clicked.connect(self.cancelar_venda)
        btn_cancelar.setStyleSheet("background-color: #95a5a6; color: white; padding: 10px;")
        
        # Botão Finalizar
        btn_finalizar = QPushButton("Finalizar [F10]")
        btn_finalizar.setFont(QFont("Arial", 14, QFont.Bold))
        btn_finalizar.clicked.connect(self.finalizar_venda)
        btn_finalizar.setStyleSheet("background-color: #27ae60; color: white; padding: 15px;")
        
        # Botão Cadastrar Produto
        btn_cadastrar = QPushButton("Cadastrar Produto [F12]")
        btn_cadastrar.setFont(QFont("Arial", 12))
        btn_cadastrar.clicked.connect(self.cadastrar_produto)
        btn_cadastrar.setStyleSheet("background-color: #3498db; color: white; padding: 10px;")
        
        buttons_layout.addWidget(btn_remover)
        buttons_layout.addWidget(btn_desconto)
        buttons_layout.addWidget(btn_cancelar)
        buttons_layout.addWidget(btn_finalizar)
        buttons_layout.addWidget(btn_cadastrar)
        
        main_layout.addLayout(buttons_layout)
        
        # Status bar
        self.statusBar().showMessage("Sistema Pronto | Use F1 para focar no código de barras")
        
        # Configurar atalhos
        self.configurar_atalhos()
        
        # Focar no campo de código
        self.barcode_input.setFocus()
    
    def configurar_atalhos(self):
        """Configura atalhos de teclado"""
        from PyQt5.QtWidgets import QShortcut
        
        # F1 - Foco no código de barras
        QShortcut(QKeySequence("F1"), self, self.focar_codigo)
        # F2 - Foco na quantidade
        QShortcut(QKeySequence("F2"), self, lambda: self.qtd_input.setFocus())
        # F3 - Remover item
        QShortcut(QKeySequence("F3"), self, self.remover_item)
        # F4 - Desconto
        QShortcut(QKeySequence("F4"), self, self.aplicar_desconto)
        # F8 - Cancelar venda
        QShortcut(QKeySequence("F8"), self, self.cancelar_venda)
        # F10 - Finalizar
        QShortcut(QKeySequence("F10"), self, self.finalizar_venda)
        # F12 - Cadastrar produto
        QShortcut(QKeySequence("F12"), self, self.cadastrar_produto)
    
    def focar_codigo(self):
        """Foca no campo de código e limpa"""
        self.barcode_input.clear()
        self.barcode_input.setFocus()
    
    def adicionar_item(self):
        """Adiciona item à venda"""
        codigo = self.barcode_input.text().strip()
        
        if not codigo:
            return
        
        try:
            quantidade = float(self.qtd_input.text())
        except:
            quantidade = 1
        
        # Adicionar item via controller
        sucesso, mensagem, item = self.controller.adicionar_item(codigo, quantidade)
        
        if sucesso:
            # Adicionar na tabela
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            self.table.setItem(row, 0, QTableWidgetItem(str(item['sequencia'])))
            self.table.setItem(row, 1, QTableWidgetItem(item['codigo_barras']))
            self.table.setItem(row, 2, QTableWidgetItem(item['descricao']))
            self.table.setItem(row, 3, QTableWidgetItem(f"{item['quantidade']:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"R$ {item['preco_total']:.2f}"))
            
            # Atualizar totais
            self.atualizar_totais()
            
            # Limpar campos
            self.barcode_input.clear()
            self.qtd_input.setText("1")
            self.barcode_input.setFocus()
            
            self.statusBar().showMessage(f"Item adicionado: {item['descricao']}", 2000)
        else:
            QMessageBox.warning(self, "Aviso", mensagem)
            self.barcode_input.selectAll()
    
    def remover_item(self):
        """Remove item selecionado"""
        current_row = self.table.currentRow()
        
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um item para remover!")
            return
        
        # Pegar sequência do item
        sequencia = int(self.table.item(current_row, 0).text())
        
        # Confirmar remoção
        reply = QMessageBox.question(self, "Confirmar", 
                                     "Remover este item?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            sucesso, mensagem = self.controller.remover_item(sequencia)
            if sucesso:
                self.table.removeRow(current_row)
                self.atualizar_totais()
                self.statusBar().showMessage(mensagem, 2000)
    
    def aplicar_desconto(self):
        """Aplica desconto percentual na venda"""
        desconto, ok = QInputDialog.getDouble(self, "Desconto", 
                                              "Desconto (%)", 
                                              0, 0, 100, 2)
        if ok:
            self.desconto_atual = desconto
            self.atualizar_totais()
    
    def atualizar_totais(self):
        """Atualiza os valores totais"""
        desconto = getattr(self, 'desconto_atual', 0)
        totais = self.controller.calcular_totais(desconto)
        
        self.label_subtotal.setText(f"Subtotal: R$ {totais['valor_total']:.2f}")
        self.label_desconto.setText(f"Desconto: R$ {totais['valor_desconto']:.2f}")
        self.label_total.setText(f"TOTAL: R$ {totais['valor_final']:.2f}")
    
    def finalizar_venda(self):
        """Finaliza a venda"""
        if not self.controller.itens_venda:
            QMessageBox.warning(self, "Aviso", "Nenhum item na venda!")
            return
        
        # Dialog de pagamento
        dialog = DialogPagamento(self, self.controller)
        if dialog.exec_():
            # Limpar tela
            self.table.setRowCount(0)
            self.desconto_atual = 0
            self.atualizar_totais()
            self.barcode_input.setFocus()
    
    def cancelar_venda(self):
        """Cancela a venda atual"""
        if not self.controller.itens_venda:
            return
        
        reply = QMessageBox.question(self, "Confirmar", 
                                     "Cancelar esta venda?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.controller.cancelar_venda()
            self.table.setRowCount(0)
            self.desconto_atual = 0
            self.atualizar_totais()
            self.statusBar().showMessage("Venda cancelada!", 2000)
    
    def cadastrar_produto(self):
        """Abre dialog de cadastro de produto"""
        dialog = DialogCadastroProduto(self, self.controller)
        dialog.exec_()


class DialogPagamento(QDialog):
    """Dialog para finalização de pagamento"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.desconto = getattr(parent, 'desconto_atual', 0)
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Finalizar Pagamento")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QFormLayout()
        
        # Calcular totais
        totais = self.controller.calcular_totais(self.desconto)
        valor_final = totais['valor_final']
        
        # Mostrar total
        label_total = QLabel(f"R$ {valor_final:.2f}")
        label_total.setFont(QFont("Arial", 24, QFont.Bold))
        label_total.setStyleSheet("color: #27ae60;")
        layout.addRow("Total a Pagar:", label_total)
        
        # Forma de pagamento
        self.combo_pagamento = QComboBox()
        self.combo_pagamento.addItems(['DINHEIRO', 'PIX', 'CARTAO_DEBITO', 'CARTAO_CREDITO'])
        layout.addRow("Forma Pagamento:", self.combo_pagamento)
        
        # Valor pago
        self.valor_pago = QDoubleSpinBox()
        self.valor_pago.setMaximum(999999.99)
        self.valor_pago.setValue(valor_final)
        self.valor_pago.setPrefix("R$ ")
        self.valor_pago.valueChanged.connect(self.calcular_troco)
        layout.addRow("Valor Pago:", self.valor_pago)
        
        # Troco
        self.label_troco = QLabel("R$ 0,00")
        self.label_troco.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addRow("Troco:", self.label_troco)
        
        # Botões
        buttons = QHBoxLayout()
        btn_confirmar = QPushButton("Confirmar [Enter]")
        btn_confirmar.clicked.connect(self.confirmar)
        btn_cancelar = QPushButton("Cancelar [Esc]")
        btn_cancelar.clicked.connect(self.reject)
        
        buttons.addWidget(btn_confirmar)
        buttons.addWidget(btn_cancelar)
        layout.addRow("", buttons)
        
        self.setLayout(layout)
        self.valor_pago.setFocus()
    
    def calcular_troco(self):
        """Calcula e mostra o troco"""
        totais = self.controller.calcular_totais(self.desconto)
        valor_final = totais['valor_final']
        valor_pago = self.valor_pago.value()
        
        troco = self.controller.calcular_troco(valor_final, valor_pago)
        self.label_troco.setText(f"R$ {troco:.2f}")
        
        if valor_pago < valor_final:
            self.label_troco.setStyleSheet("color: red;")
        else:
            self.label_troco.setStyleSheet("color: green;")
    
    def confirmar(self):
        """Confirma o pagamento"""
        forma = self.combo_pagamento.currentText()
        valor = self.valor_pago.value()
        
        sucesso, mensagem, venda = self.controller.finalizar_venda(
            forma, valor, self.desconto
        )
        
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", mensagem)


class DialogCadastroProduto(QDialog):
    """Dialog para cadastro de produtos"""
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Cadastrar Produto")
        self.setModal(True)
        self.setMinimumWidth(500)
        
        layout = QFormLayout()
        
        # Campos básicos
        self.input_codigo = QLineEdit()
        layout.addRow("Código de Barras*:", self.input_codigo)
        
        self.input_descricao = QLineEdit()
        layout.addRow("Descrição*:", self.input_descricao)
        
        self.input_preco = QDoubleSpinBox()
        self.input_preco.setMaximum(999999.99)
        self.input_preco.setPrefix("R$ ")
        layout.addRow("Preço de Venda*:", self.input_preco)
        
        self.input_unidade = QComboBox()
        self.input_unidade.addItems(['UN', 'KG', 'LT', 'M', 'M2', 'CX'])
        layout.addRow("Unidade:", self.input_unidade)
        
        self.input_estoque = QDoubleSpinBox()
        self.input_estoque.setMaximum(999999.99)
        layout.addRow("Estoque Inicial:", self.input_estoque)
        
        # Campos fiscais (opcionais)
        self.input_ncm = QLineEdit()
        self.input_ncm.setPlaceholderText("Ex: 12345678")
        layout.addRow("NCM (opcional):", self.input_ncm)
        
        self.input_cfop = QLineEdit("5102")
        layout.addRow("CFOP:", self.input_cfop)
        
        # Botões
        buttons = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_salvar.clicked.connect(self.salvar)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        
        buttons.addWidget(btn_salvar)
        buttons.addWidget(btn_cancelar)
        layout.addRow("", buttons)
        
        self.setLayout(layout)
    
    def salvar(self):
        """Salva o produto"""
        dados = {
            'codigo_barras': self.input_codigo.text().strip(),
            'descricao': self.input_descricao.text().strip(),
            'preco_venda': self.input_preco.value(),
            'unidade': self.input_unidade.currentText(),
            'estoque_atual': self.input_estoque.value(),
            'ncm': self.input_ncm.text().strip(),
            'cfop': self.input_cfop.text().strip()
        }
        
        # Validar
        if not dados['codigo_barras'] or not dados['descricao']:
            QMessageBox.warning(self, "Aviso", "Preencha os campos obrigatórios!")
            return
        
        if dados['preco_venda'] <= 0:
            QMessageBox.warning(self, "Aviso", "Preço deve ser maior que zero!")
            return
        
        # Cadastrar
        sucesso, mensagem, produto = self.controller.cadastrar_produto(dados)
        
        if sucesso:
            QMessageBox.information(self, "Sucesso", mensagem)
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", mensagem)