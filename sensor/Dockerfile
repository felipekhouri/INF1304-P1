FROM python:3.11-slim
WORKDIR /app

# Evita arquivos .pyc e garante flush de stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1

# Instala dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia código da aplicação
COPY sensor.py ./

CMD ["python", "sensor.py"]
