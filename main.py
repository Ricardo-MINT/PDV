"""
Sistema PDV - Ponto de Entrada Principal
"""
# No main.py, tente esta ordem:
import sys
from PyQt5.QtWidgets import QApplication
from database.db import init_db
from views.pdv_window import PDVWindow
from utils.log_config import logger

def main():
    """Função principal"""
    logger.info("="*60)
    logger.info("Iniciando Sistema PDV MVP")
    logger.info("="*60)
    
    # Inicializar banco de dados
    try:
        init_db()
        logger.info("Banco de dados inicializado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao inicializar banco: {str(e)}")
        sys.exit(1)
    
    # Criar aplicação Qt
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Estilo mais moderno
    
    # Criar e mostrar janela principal
    window = PDVWindow()
    window.show()
    
    logger.info("Interface gráfica carregada")
    
    # Executar aplicação
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()