import os

file_path = r"c:\Users\henri\OneDrive\Documents\python_projects\ecommerce_analytics\src\ecommerce_analytics\dashboard\app.py"
with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

replacements = {
    '"Username:"': '"Usuário:"',
    '"Password:"': '"Senha:"',
    '"Login"': '"Entrar"',
    'label="📈 Overview"': 'label="📈 Visão Geral"',
    '"Total Revenue"': '"Receita Total"',
    '"Total Orders"': '"Total de Pedidos"',
    '"Avg Order Value"': '"Ticket Médio"',
    '"Total Customers"': '"Total de Clientes"',
    'label="🏆 Top Products"': 'label="🏆 Top Produtos"',
    '"Limit:"': '"Quantidade:"',
    'label="📊 Sales by Category"': 'label="📊 Vendas por Categoria"',
    'label="🔮 Forecasting"': 'label="🔮 Previsões"',
    '"Months Ahead:"': '"Meses à frente:"',
    'label="💡 Recommendations"': 'label="💡 Recomendações"',
    '"Customer ID:"': '"ID do Cliente:"',
    '"Top N:"': '"Top N:"',
    '"Revenue Trend"': '"Evolução da Receita"',
    '"Month"': '"Mês"',
    '"Revenue ($)"': '"Receita (R$)"',
    '"Orders Trend"': '"Evolução de Pedidos"',
    '"Number of Orders"': '"Quantidade de Pedidos"',
    'title=f"Top {limit} Products"': 'title=f"Top {limit} Produtos"',
    '"Product"': '"Produto"',
    '"Sales"': '"Vendas"',
    '"Sales by Category"': '"Vendas por Categoria"',
    'title=f"Revenue Forecast - {months} Months"': 'title=f"Previsão de Receita - {months} Meses"',
    'title=f"Recommendations for {customer_id}"': 'title=f"Recomendações para {customer_id}"',
    '"Score"': '"Relevância"'
}

# Fix Entrar conflict with something else? No string "Login" is exactly that text.
for k, v in replacements.items():
    code = code.replace(k, v)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)
