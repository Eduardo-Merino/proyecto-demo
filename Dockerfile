# Utilizamos una imagen base de continuumio/miniconda para usar conda como manejador de entornos
FROM continuumio/miniconda3:latest

# Copiamos el archivo environment.yml al contenedor
COPY environment.yml .

# Instalamos las dependencias desde el archivo environment.yml
RUN conda env create -f environment.yml

# Activamos el entorno
SHELL ["conda", "run", "-n", "demo", "/bin/bash", "-c"]

# Copiamos todo el contenido del proyecto al contenedor
RUN mkdir /app
WORKDIR /app/
COPY ./app /app

# Establecemos el entorno como base para ejecutar los comandos
ENV PATH /opt/conda/envs/demo/bin:$PATH

# Exponemos el puerto 8000 para que la API esté disponible en este puerto
EXPOSE 8000

# Comando para correr la aplicación usando el entorno conda
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"]