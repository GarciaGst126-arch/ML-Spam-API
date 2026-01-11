# ML-Spam-API

# Email Spam Detection API

API de detección de spam en correos electrónicos usando Machine Learning con Regresión Logística y SVM.

## Modelos Implementados

1. **Regresión Logística**: Modelo lineal rápido e interpretable para clasificación de texto
2. **SVM (Support Vector Machine)**: Clasificador no lineal con kernel RBF para patrones complejos

Ambos modelos usan **TF-IDF** (Term Frequency-Inverse Document Frequency) para vectorizar el texto.

## Instalación Local

```bash
cd scripts/backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o: venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Iniciar servidor
python manage.py runserver
```

## API Endpoints

### POST /api/detect/
Detecta si un correo es spam o ham (legítimo).

**Request Body:**
```json
{
  "email": "sender@example.com",
  "content": "Congratulations! You've won $1,000,000!",
  "model_type": "logistic"
}
```

**Response:**
```json
{
  "prediction": "spam",
  "is_spam": true,
  "probability": 0.95,
  "confidence": 95.0,
  "class_probabilities": {
    "spam": 0.95,
    "ham": 0.05
  },
  "model_used": "logistic"
}
```

### GET /api/detect/
Retorna información sobre la API y campos requeridos.

### GET /api/logs/
Retorna el historial de detecciones.

### POST /api/train/
Re-entrena los modelos ML con los datos de ejemplo.

### GET /api/health/
Health check del servicio.

## Despliegue en Railway

1. **Subir código a GitHub**

2. **Crear proyecto en Railway:**
   - Ir a [railway.app](https://railway.app)
   - New Project → Deploy from GitHub repo
   - Seleccionar el repositorio

3. **Configurar variables de entorno:**
   ```
   DJANGO_SECRET_KEY=genera-una-clave-secreta-aqui
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   ```

4. **Configurar el servicio:**
   - Root Directory: `scripts/backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

5. Railway detectará el Procfile y desplegará automáticamente.

## Despliegue en Render

1. **Crear cuenta en [render.com](https://render.com)**

2. **Nuevo Web Service:**
   - Conectar repositorio GitHub
   - Runtime: Python 3
   - Root Directory: `scripts/backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn config.wsgi:application`

3. **Variables de entorno:**
   ```
   DJANGO_SECRET_KEY=genera-una-clave-secreta-aqui
   DEBUG=False
   PYTHON_VERSION=3.11.6
   ```

4. Render construirá e iniciará el servicio automáticamente.

## Tecnologías

- Django 4.2
- Django REST Framework
- scikit-learn (Logistic Regression, SVM, TF-IDF)
- gunicorn
- whitenoise

## Ejemplos de Uso

**Spam:**
```bash
curl -X POST http://localhost:8000/api/detect/ \
  -H "Content-Type: application/json" \
  -d '{"email": "winner@lottery.com", "content": "You won $1M! Click here!", "model_type": "svm"}'
```

**Ham (legítimo):**
```bash
curl -X POST http://localhost:8000/api/detect/ \
  -H "Content-Type: application/json" \
  -d '{"email": "john@company.com", "content": "Meeting tomorrow at 3pm", "model_type": "logistic"}'
