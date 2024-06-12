# Utiliza la imagen oficial de Python como base
FROM python:3.8-slim-buster

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo requirements.txt al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias utilizando pip
RUN pip install -r requirements.txt

# Copia el resto de los archivos de tu aplicación al directorio de trabajo
COPY . .

# Expon el puerto 5000 en el contenedor
EXPOSE 5000

# Define el comando para ejecutar tu aplicación Flask
CMD ["python", "app.py"]
