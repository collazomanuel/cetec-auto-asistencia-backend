
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

En Ubuntu:

```bash
source .venv/bin/activate
```

En Windows:

```bash
.venv\Scripts\activate
```

3. Instala las dependencias

```bash
pip install -r requirements.txt
```

4. Ejecuta el servidor

```bash
uvicorn main:app
```

### Dependencias

Las dependencias del proyecto se encuentran enlistadas en el archivo _"requirements.txt"_ ubicando en el directorio _"backend"_ junto al archivo _"main.py"_.

### Uso

En esta sección se incluye información relevante al uso correcto de esta API.

#### Documentación de FastAPI

FastAPI proporciona una documentación interactiva generada automáticamente en _http://127.0.0.1:8000/docs_. Esta documentación describe todos los endpoints disponibles, los parámetros requeridos y opcionales, y los ejemplos de solicitud y respuesta.

```http
GET /docs
```
#### (GET) Exam

Este servicio devuelve una lista de todos los examenes válidos al momento de efectuar la solicitud. Para utilizarlo se debe efectuar una _GET request_ de la siguiente forma:

```http
GET http://127.0.0.1:8000/exam

```

#### (POST) Exam

Este servicio recibe los datos de un examen y los carga en la base de datos. Para utilizarlo, se debe efectuar una _POST request_ de la siguiente forma:

```http
POST http://127.0.0.1:8000/exam

```

En el _body_ de la _request_ se debe especificar la siguiente información:

- code: Código del examen
- name: Nombre del examen
- start: Tiempo de comienzo del examen
- length: Duración del examen en minutos
- margin: Márgen de validez de asistencia en minutos

#### (POST) Student

Este servicio recibe los datos de un alumno y los carga en la base de datos. Para utilizarlo, se debe efectuar una _POST request_ de la siguiente forma:

```http
POST http://127.0.0.1:8000/student

```

En el _body_ de la _request_ se debe especificar la siguiente información:

- email: Correo electrónico del alumno
- image: Imagen del alumno en el formato de _base64_

#### (POST) Attendance

Este servicio recibe la solicitud de asistencia a un examen de un alumno y valida los parámetros a partir de los datos que existen en la base de datos. Para utilizarlo, se debe efectuar una _POST request_ de la siguiente forma:

```http
POST http://127.0.0.1:8000/attendance

```

En el _body_ de la _request_ se debe especificar la siguiente información:

- code: Código del examen
- email: Correo electrónico del alumno
- latitude: Coordenada de longitud
- longitude: Coordenada de latitud
- image: Imagen del alumno en formato _base64_

![Footer](https://user-images.githubusercontent.com/75450615/175360883-72efe4c4-1f14-4b11-9a7c-55937563cffa.png)
