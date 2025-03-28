
# CETEC Auto-Asistencia

Este es el back-end del CETEC Auto-Asistencia construido en Python utilizando el framework web FastAPI. Está diseñado para el uso de los alumnos de la Facultad de Ingeniería de la Universidad de Buenos Aires. Este documento detalla las instrucciones para su configuración, ejecución y uso.

<div align="center">
  <img src="https://user-images.githubusercontent.com/75450615/228704389-a2bcdf3e-d4d6-4236-b1c6-57fd9e545625.png#gh-dark-mode-only" width="50%" align="center">
</div>

### Requisitos previos

Antes de ejecutar este back-end, asegúrese de tener instalado lo siguiente:

- Python 3.7+ (se recomienda utilizar la última versión estable de Python)
- Pip (administrador de paquetes de Python)

## Configuración del entorno

1. **Crea un entorno virtual**

```bash
python3 -m venv .venv
```

2. **Activa el entorno virtual**

En Ubuntu:

```bash
source .venv/bin/activate
```

En Windows:

```bash
.venv\Scripts\activate
```

3. **Instala las dependencias**

```bash
pip install -r requirements.txt
```

4. **Configura las variables de entorno**

Crea un archivo `.env` en el directorio raíz del proyecto y define las siguientes variables:

```env
MONGODB_KEY=<tu_clave_de_mongodb>
FRONTEND_URL=<url_del_frontend>
```

5. **Ejecuta el servidor**

```bash
uvicorn main:app --reload
```

## Endpoints disponibles

### Documentación interactiva

FastAPI genera automáticamente una documentación interactiva en `http://127.0.0.1:8000/docs`. Aquí puedes explorar y probar los endpoints disponibles.

```http
GET /docs
```

### Endpoints principales

#### (POST) `/student`

Registra un nuevo estudiante en la base de datos.

- **Body**:
  ```json
  {
    "email": "correo@ejemplo.com",
    "image": "base64_string"
  }
  ```

#### (GET) `/professor`

Obtiene la lista de todos los profesores registrados.

#### (POST) `/professor`

Registra un nuevo profesor en la base de datos.

- **Body**:
  ```json
  {
    "email": "correo@ejemplo.com"
  }
  ```

#### (GET) `/exam`

Obtiene una lista de exámenes. Puedes filtrar los resultados utilizando el parámetro `filter`.

- **Query Params**:
  - `filter` (opcional): `true` o `false`.

#### (POST) `/exam`

Crea un nuevo examen.

- **Body**:
  ```json
  {
    "name": "Examen Final",
    "start": "2025-03-27 10:00",
    "length": 120,
    "margin": 15
  }
  ```

#### (PUT) `/exam`

Actualiza un examen existente.

- **Body**:
  ```json
  {
    "code": "codigo_del_examen",
    "name": "Examen Actualizado",
    "start": "2025-03-27 12:00",
    "length": 90,
    "margin": 10
  }
  ```

#### (GET) `/attendance`

Obtiene la lista de asistencias para un examen específico.

- **Query Params**:
  - `code`: Código del examen.

#### (POST) `/attendance`

Registra la asistencia de un estudiante a un examen.

- **Body**:
  ```json
  {
    "code": "codigo_del_examen",
    "latitude": -34.617639,
    "longitude": -58.368056,
    "accuracy": 50,
    "image": "base64_string"
  }
  ```

#### (POST) `/face_validation`

Valida la imagen facial de un estudiante.

- **Body**:
  ```json
  {
    "image": "base64_string"
  }
  ```

---

## Dependencias

Las dependencias del proyecto están listadas en el archivo `requirements.txt`:

```plaintext
fastapi==0.111.1
pydantic==2.8.2
pymongo==3.13.0
uvicorn==0.20.0
python-decouple==3.8
dnspython==2.3.0
deepface==0.0.92
tf-keras==2.16.0
haversine==2.8.1
```

Instálalas ejecutando:

```bash
pip install -r requirements.txt
```

---

## Notas adicionales

- **Validación de ubicación**: Actualmente, la validación de ubicación está deshabilitada para facilitar el desarrollo. Puedes habilitarla modificando la función `validate_location` en `main.py`.
- **Validación facial**: La validación facial también está deshabilitada temporalmente debido a problemas de infraestructura. Puedes habilitarla modificando la función `validate_face`.

---

## Contacto

Para consultas o soporte, puedes contactarte con el desarrollador a través de [mcollazo@fi.uba.ar](mailto:mcollazo@fi.uba.ar).

![Footer](https://user-images.githubusercontent.com/75450615/175360883-72efe4c4-1f14-4b11-9a7c-55937563cffa.png)
