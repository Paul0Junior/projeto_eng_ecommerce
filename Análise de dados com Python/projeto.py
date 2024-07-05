# pip install pandas, numpy
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

# Gerando os dados fictícios

np.random.seed(0)
data = {
    'order_id': np.arange(1, 101),
    'data': pd.date_range(start='2023-01-01', periods=100),
    'product_id': np.random.randint(1, 20, size=100),
    'quantity': np.random.randint(1, 10, size=100),
    'price': np.round(np.random.uniform(5, 100, size=100), 2),
    'category': np.random.choice(['Eletrônicos', 'Roupas', 'Livros', 'Remédios'], size=100)
}

df = pd.DataFrame(data)
df.to_csv('dados_ecommerce.csv', index=False)
# print(df.head())

# Salvando dados no no BD SQLITE
# Conectando no banco de dados
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()

# Criando a tabela de vendas
# cursor.execute('''
# CREATE TABLE sales (
#     order_id INTEGER,
#     date DATE,
#     product_id INTEGER,
#     quantity INTEGER,
#     price FLOAT,
#     category TEXT
# )
# ''')

# Carregar dados na tabela sales

df.to_sql('sales', conn, if_exists='replace', index=False)
conn.commit()
conn.close()

# Limpeza e transformação
# df['date'] = pd.to_datetime(df['date'])
df.drop_duplicates(inplace=True)
print(df.info())

# Análise de dados
# Análise de vendas por categoria
category_sales = df.groupby('category')['quantity'].sum()
category_sales.plot(kind='bar')
plt.title('Vendas por categoria')
plt.xlabel('Categoria')
plt.ylabel('Quantidade vendida')
plt.show()

# Análise de tendências ao longo do tempo
df.set_index('data', inplace=True)
sales_tren = df['quantity'].resample('ME').sum()
sales_tren.plot()
plt.title('Tendências de vendas ao longo do tempo')
plt.xlabel('Data')
plt.ylabel('Quantidade vendida')
plt.show()
