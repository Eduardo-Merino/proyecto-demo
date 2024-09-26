# Usa una imagen oficial de Python 3.12
FROM python:3.12-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias environment.yml al contenedor
COPY enviroment.yml /app/enviroment.yml

# Instala conda y crea el entorno desde el archivo environment.yml
RUN apt-get update && apt-get install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    bash miniconda.sh -b -p /opt/conda && \
    rm miniconda.sh && \
    /opt/conda/bin/conda env create -f /app/enviroment.yml && \
    /opt/conda/bin/conda clean -afy

# Activa el entorno creado
SHELL ["/bin/bash", "-c"]
RUN echo "source activate demo" > ~/.bashrc
ENV PATH /opt/conda/envs/demo/bin:$PATH

# Copia el contenido del proyecto a la imagen del contenedor
COPY . /app

# Exponer el puerto 8000 para FastAPI
EXPOSE 8000

# Comando para correr la aplicación usando Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]