# 🚀 Guía de Deployment - Streamlit Cloud

## Pasos para desplegar tu aplicación

### 1. Preparar el repositorio en GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/tu-usuario/voice-text-agent.git
git push -u origin main
```

### 2. Crear cuenta en Streamlit Cloud

1. Ve a: https://share.streamlit.io/
2. Inicia sesión con tu cuenta de GitHub

### 3. Desplegar la aplicación

1. Click en **"New app"**
2. Selecciona tu repositorio de GitHub
3. Selecciona la rama `main`
4. Main file: `voice_text_agent.py`
5. Click **"Deploy"**

### 4. Configuración adicional

El archivo `runtime.txt` ya está incluido para especificar Python 3.11. Si necesitas cambiarlo, edita el archivo:

```
python-3.11.0
```

## ✅ Archivos necesarios

Tu proyecto ya incluye todos los archivos necesarios:
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `voice_text_agent.py` - Archivo principal de la aplicación
- ✅ `runtime.txt` - Versión de Python (3.11.0)

## ✅ Funcionalidad completa

La aplicación ahora usa **audio-recorder-streamlit** que permite grabar audio directamente desde el navegador del usuario, funcionando perfectamente en Streamlit Cloud:
- ✅ Text-to-Speech funciona perfectamente
- ✅ Speech-to-Text con grabación desde el navegador (funciona en la nube!)
- ✅ Los usuarios también pueden subir archivos de audio para transcribir

## 📚 Documentación

Para más información: https://docs.streamlit.io/streamlit-community-cloud
