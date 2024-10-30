### Exploratory Data Analysis with Python Applied to Retail ###

from flask import Flask, jsonify, request, render_template_string
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import io
import base64


app = Flask(__name__)

### Carregando os dados com pandas em Linguagem Python ###
df = pd.read_csv("4-analysis/4-dados/dataset.csv")

# Função auxiliar para verificar se o dataset está carregado
def check_data_loaded():
    if df.empty:
        return {"error": "Dataset could not be loaded or is empty"}, 500
    return None


# ==> Sumário <==

@app.route('/')
def sumario():
    textoinicial = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Perguntas de Negócio</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">  
    </head>
    <body>
        <h1>Perguntas de Negócio</h1>
        <h2>Análise de dados para responder Perguntas de Negócios</h3>
        <p>Este projeto consistiu em uma Análise Exploratória de Dados (EDA) realizada em Linguagem Python, focada no setor de varejo. O objetivo foi extrair insights valiosos a partir de dados, permitindo uma compreensão mais profunda do comportamento dos consumidores e das vendas.</p>
        <p>Esta análise foi desenvolvida como parte de um exercício de um curso de Análise de Dados, onde exploramos um conjunto de dados real. A fonte dos dados utilizada para este exercício pode ser encontrada no seguinte link: <a href="htth3s://community.tableau.com/s/question/0D54T00000CWeX8SAL/sample-superstore-sales-excelxls">Sample Superstore Sales Data.</a></p>
        <h2>Sumário:</h2>
        <p><a href="http://localhost:8080/pergunta1" class="button-link">1: Qual Cidade com Maior Valor de Venda de Produtos da Categoria 'Office Supplies'?</a></p>
        <p><a href="http://localhost:8080/pergunta2" class="button-link">2: Qual o Total de Vendas Por Data do Pedido?</a></p>
        <p><a href="http://localhost:8080/pergunta3" class="button-link">3: Qual o Total de Vendas por Estado?</a></p>
        <p><a href="http://localhost:8080/pergunta4" class="button-link">4: Quais São as 10 Cidades com Maior Total de Vendas?</a></p>
        <p><a href="http://localhost:8080/pergunta5" class="button-link">5: Qual Segmento Teve o Maior Total de Vendas?</a></p>
        <p><a href="http://localhost:8080/pergunta6" class="button-link">6: Qual o Total de Vendas Por Segmento e Por Ano?</a></p>
        <p><a href="http://localhost:8080/pergunta7" class="button-link">7: Os gestores da empresa estão considerando conceder diferentes faixas de descontos e gostariam de fazer uma simulação com base na regra: Se o Valor_Venda for maior que 1000 recebe 15% de desconto, e Se o Valor_Venda for menor que 1000 recebe 10% de desconto. Quantas Vendas Receberiam 15% de Desconto?</a></p>
        <p><a href="http://localhost:8080/pergunta8" class="button-link">8: Considere Que a Empresa Decida Conceder o Desconto de 15% do Item Anterior. Qual seria a Média do Valor de Venda Antes e Depois do Desconto?</a></p>
        <p><a href="http://localhost:8080/pergunta9" class="button-link">9: Qual a Média de Vendas Por Segmento, Por Ano e Por Mês?</a></p>
        <p><a href="http://localhost:8080/pergunta10" class="button-link">10: Qual o Total de Vendas Por Categoria das Top 12 SubCategorias?</a></p>
    </body>
    </html>
    """
    return render_template_string(textoinicial)


# ==> QUESTÃO 1 <==
@app.route("/pergunta1", methods=["GET"])
def question1():
    data_check = check_data_loaded()
    if data_check:
        return data_check

    df_p1 = df[df['Categoria'] == 'Office Supplies']
    df_p1_total = df_p1.groupby("Cidade")["Valor_Venda"].sum()
    cidade_maior_venda = df_p1_total.idxmax()
    df_p1_sorted = df_p1_total.sort_values(ascending=False).to_dict()

    texto_1 = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Pergunta 1</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">  
    </head>
    <body>
        <div class="link-container">
            <a href="http://localhost:8080/">Sumário</a>
            <div class="right-links">
                <a class="inactive">Anterior</a>
                <a href="http://localhost:8080/pergunta2">Próximo</a>
            </div>
        </div>
        <h2>Pergunta de Negócio 1</h2>
        <h2>Qual Cidade com Maior Valor de Venda de Produtos da Categoria 'Office Supplies'?</h2>
        <h3>Resposta: {{ cidade_maior_venda }}</h3>
        <p>Para conferir o resultado, segue a lista do maior para o menor valor de venda:</p>
        <table>
            <thead>
                <tr>
                    <th>Cidade</th>
                    <th>Total de Vendas (R$)</th>
                </tr>
            </thead>
            <tbody>
                {% for cidade, valor in df_p1_sorted.items() %}
                <tr>
                    <td>{{ cidade }}</td>
                    <td>R$ {{ '{:,.2f}'.format(valor).replace(',', 'X').replace('.', ',').replace('X', '.') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """

    return render_template_string(texto_1, cidade_maior_venda=cidade_maior_venda, df_p1_sorted=df_p1_sorted)



# ==> QUESTÃO 2 <==

@app.route("/pergunta2", methods=["GET"])
def question2():

    # Agrupando e somando o valor das vendas por data
    df['Data_Pedido'] = pd.to_datetime(df['Data_Pedido'], errors='coerce')
    df_p2 = df.groupby("Data_Pedido")["Valor_Venda"].sum()
    df_p2_sorted = df_p2.sort_index()

    # Remover entradas com data NaT
    df_p2_sorted = df_p2_sorted[~df_p2_sorted.index.isna()]

    # Gerando o gráfico e convertendo para base64
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.lineplot(x=df_p2_sorted.index,
                 y=df_p2_sorted.values,
                 ax=ax,
                 marker='o',
                 color='b')
    ax.set_title('Total de Vendas Por Data do Pedido', fontsize=14)
    ax.set_xlabel("Data do Pedido", fontsize=12)
    ax.set_ylabel("Total do Valor de Venda (R$)", fontsize=12)
    plt.rcParams['font.size'] = 8

    # Ajustar os rótulos do eixo x
    num_labels = len(df_p2_sorted)
    step = max(1, num_labels // 10)
    plt.xticks(ticks=range(0, num_labels, step), 
               labels=[date.strftime('%d/%m/%Y') for date in df_p2_sorted.index[::step]],
               rotation=45)

    # Convertendo o gráfico para uma imagem em base64
    img = io.BytesIO()
    plt.tight_layout()
    plt.savefig(img, format='png', transparent=True)
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    # Template HTML para exibir o gráfico e os dados
    texto_2 = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Pergunta 2</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">  
    </head>
    <body>
        <div class="link-container">
            <a href="http://localhost:8080/">Sumário</a>
            <div class="right-links">
                <a href="http://localhost:8080/pergunta1">Anterior</a>
                <a href="http://localhost:8080/pergunta3">Próximo</a>
            </div>
        </div>
        <h2>Pergunta de Negócio 2</h2>
        <h2>Qual o Total de Vendas Por Data do Pedido?</h2>
        <p>O gráfico abaixo mostra o total de vendas por data do pedido.</p>
        <img src="data:image/png;base64,{{ graph_url }}" alt="Gráfico de Total de Vendas por Data do Pedido">
        <p>Para conferir o resultado, segue a lista dos valores de venda, por data do pedido:</p>
        <table>
            <thead>
                <tr>
                    <th>Data do Pedido</th>
                    <th>Total de Vendas (R$)</th>
                </tr>
            </thead>
            <tbody>
                {% for data, valor in df_p2_sorted.items() %}
                <tr>
                    <td>{{ data.strftime('%d/%m/%Y') }}</td>
                    <td>R$ {{ '{:,.2f}'.format(valor).replace(',', 'X').replace('.', ',').replace('X', '.') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    return render_template_string(texto_2, df_p2_sorted=df_p2_sorted, graph_url=graph_url)



# ==> QUESTÃO 3 <==

@app.route("/pergunta3", methods=["GET"])
def question3():

    # Agrupando e somando o valor das vendas por estado
    df_p3 = df.groupby("Estado")["Valor_Venda"].sum().reset_index()
    df_p3_sorted = df_p3.sort_values(by="Valor_Venda", ascending=False)

    # Gerando o gráfico e convertendo para base64
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.barplot(x=df_p3_sorted['Estado'],
                y=df_p3_sorted['Valor_Venda'],
                palette="husl",
                ax=ax)
    ax.set_title('Total de Vendas Por Estado', fontsize=14)
    ax.set_xlabel("Estado", fontsize=12)
    ax.set_ylabel("Total do Valor de Venda (R$)", fontsize=12)
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.rcParams['font.size'] = 8

    # Convertendo o gráfico para uma imagem em base64
    img = io.BytesIO()
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.savefig(img, format='png', transparent=True)
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    # Template HTML para exibir o gráfico e os dados
    texto_3 = """
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Pergunta 3</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">  
    </head>
    <body>
        <div class="link-container">
            <a href="http://localhost:8080/">Sumário</a>
            <div class="right-links">
                <a href="http://localhost:8080/pergunta2">Anterior</a>
                <a href="http://localhost:8080/pergunta4">Próximo</a>
            </div>
        </div>
        <h2>Pergunta de Negócio 3</h2>
        <h2>Qual o Total de Vendas por Estado?</h2>
        <p>O gráfico abaixo mostra o total de vendas por estado.</p>
        <img src="data:image/png;base64,{{ graph_url }}" alt="Gráfico de Total de Vendas por Estado">
        <p>Para conferir o resultado, segue a lista do maior para o menor valor de venda, por data do pedido:</p>
        <table>
            <thead>
                <tr>
                    <th>Estado</th>
                    <th>Total de Vendas (R$)</th>
                </tr>
            </thead>
            <tbody>
                {% for row in df_p3_sorted.itertuples() %}
                <tr>
                    <td>{{ row.Estado }}</td>
                    <td>R$ {{ '{:,.2f}'.format(row.Valor_Venda).replace(',', 'X').replace('.', ',').replace('X', '.') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </body>
    </html>
    """
    return render_template_string(texto_3, df_p3_sorted=df_p3_sorted, graph_url=graph_url)







if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)