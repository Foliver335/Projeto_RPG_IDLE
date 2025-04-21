FROM python:3.10-slim
WORKDIR /app

# Instala o pacote Python e dependências via setup.py
COPY setup.py requirements.txt ./
RUN pip install --no-cache-dir .

# Copia o restante do código
COPY . /app

# Executa a aplicação
CMD ["cronicas"]