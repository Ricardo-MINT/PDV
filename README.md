# Sistema PDV MVP - Desktop

Aplicação desktop de **Ponto de Venda (PDV)** desenvolvida em Python, com foco em simplicidade, resiliência para operações offline e interface de rápida navegação por atalhos de teclado.

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Interface Gráfica:** PyQt5 (Tema Fusion)
* **ORM / Banco de Dados:** SQLAlchemy 2.0 com SQLite local
* **Segurança:** Bcrypt para hashing de senhas e autenticação
* **Arquitetura:** Padrão MVC (Model-View-Controller) desacoplado

## 🚀 Funcionalidades

* **Operação de Caixa:** Atalhos de teclado operacionais (`F1` Código de Barras, `F2` Quantidade, `F3` Remover Item, `F4` Desconto, `F10` Finalizar, `F12` Cadastrar Produto).
* **Gestão de Produtos:** Cadastro com preço, estoque e campos fiscais básicos (NCM / CFOP).
* **Validações de UX:** Alertas visuais e prevenção de operações inválidas (descontos, itens nulos, vendas vazias).
* **Resiliência:** Persistência local em SQLite, operando perfeitamente sem dependência de internet ou servidor remoto.

## 📦 Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/Ricardo-MINT/PDV.git](https://github.com/Ricardo-MINT/PDV.git)
   cd PDV

## Crie e ative o ambiente virtual:

python -m venv .venv
source .venv/bin/activate

## Instale as dependências:

pip install -r requirements.txt

## Execute a aplicação:

python main.py
