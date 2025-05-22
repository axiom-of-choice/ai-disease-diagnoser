# Imagen base oficial de Python
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar los archivos de la app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copy ENV files
COPY ./.env ./
COPY . .

# Exponer el puerto que usa Streamlit
EXPOSE 8501

# Comando para iniciar la app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
