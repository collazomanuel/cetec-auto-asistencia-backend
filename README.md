
# CETEC Auto-Asistencia

Este es el back-end del CETEC Auto-Asistencia construido en Python utilizando el framework web FastAPI y diseñado para el uso de los alumnos de la Facultad de Ingeniería de la Universidad de Buenos Aires. En esta sección se detallan instrucciones para su ejecución local.

<div align="center">
  <img src="https://user-images.githubusercontent.com/75450615/228704389-a2bcdf3e-d4d6-4236-b1c6-57fd9e545625.png#gh-dark-mode-only" width="50%" align="center">
</div>

### Requisitos previos

Antes de ejecutar este back-end, asegúrese de tener instalado lo siguiente:

- Python 3.7+ (se recomienda utilizar la última versión estable de Python)
- Pip (administrador de paquetes de Python)

### Configuración del entorno

1. Crea un entorno virtual

```bash
python3 -m venv .venv
```

2. Activa el entorno virtual

```bash
source .venv/bin/activate
```

3. Instala las dependencias

```bash
pip install -r requirements.txt
```

4. Ejecuta el servidor

```bash
uvicorn main:app --host 0.0.0.0
```

(5). Desactiva el entorno virtual

```bash
deactivate
```

### Dependencias

Las dependencias del proyecto se encuentran enlistadas en el archivo _"requirements.txt"_ ubicando en el directorio _"backend"_ junto al archivo _"main.py"_.

### Uso

En esta sección se incluye información relevante al uso correcto de esta API.

#### Documentación de FastAPI

FastAPI proporciona una documentación interactiva generada automáticamente en _http://0.0.0.0:8000/docs_. Esta documentación describe todos los endpoints disponibles, los parámetros requeridos y opcionales, y los ejemplos de solicitud y respuesta.

```http
GET /docs
```

#### Student (Servicio)

Este servicio recibe los datos de un alumno y los carga en la base de datos. Para utilizarlo se debe efectuar una _POST request_ de la siguiente forma:

```http
POST http://0.0.0.0:8000/student

```

En el _body_ de la _request_ se debe especificar la siguiente información:

- image: Imagen del alumno en el formato de _base64_
- email: Correo electrónico del alumno
- latitude: Coordenada de longitud
- longitude: Coordenada de latitud

#### Student (Servicio)

Este servicio recibe la solicitud de asistencia de un alumno y valida los datos a partir de los datos que hay en la base de datos. Para utilizarlo se debe efectuar una _PUT request_ de la siguiente forma:

```http
PUT http://0.0.0.0:8000/student

```

En el _body_ de la _request_ se debe especificar la siguiente información:

- image: Imagen del alumno en el formato de _base64_
- email: Correo electrónico del alumno
- latitude: Coordenada de longitud
- longitude: Coordenada de latitud

![Footer](https://user-images.githubusercontent.com/75450615/175360883-72efe4c4-1f14-4b11-9a7c-55937563cffa.png)
