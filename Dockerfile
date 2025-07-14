FROM python:3.11-alpine3.21

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

#Agrega un usuario y grupo | para evitar permisos de root
RUN addgroup -S app \
 && adduser -S app -G app

# Copiar el archivo de dependencias (si tienes un requirements.txt)
# Si no tienes requirements.txt, puedes agregar la instalación directamente en la siguiente línea
COPY requirements.txt .

# Instalar dependencias del sistema necesarias para algunas bibliotecas
RUN apk add --no-cache --virtual .build-deps \
    gcc musl-dev libffi-dev openssl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# Copiar todo el contenido de la aplicación en el contenedor
COPY --chown=app:app . .

#Puerto de visualización
EXPOSE 8000

#Cambia el usaurio para que trabaje con el usuario que se esta creando
USER app

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]