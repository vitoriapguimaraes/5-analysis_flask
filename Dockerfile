# Utilizar imagem base Python
FROM python:3.10.11

# Definir o diretório de trabalho
WORKDIR /app

# Copiar arquivos necessários
COPY requirements.txt requirements.txt
COPY 4-analysis_with_flask.py 4-analysis_with_flask.py
COPY 4-analysis/4-dados/ 4-analysis/4-dados/
COPY static/css/style.css static/css/style.css

# Instalar as dependências
RUN pip install -r requirements.txt
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-roboto \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Expor a porta do Flask
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "4-analysis_with_flask.py"]