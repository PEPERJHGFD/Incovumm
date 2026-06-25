# Admin Panel Simulado

Este proyecto es un panel administrativo simulado con apariencia de Django Admin, construido con Flask y Bootstrap y organizado con una arquitectura MVC limpia.

## Estructura

- `app.py`: punto de entrada de Flask.
- `config.py`: configuración de aplicación, usuario y rutas.
- `controllers/`: controladores que interactúan con los servicios.
- `models/`: definiciones de datos y persistencia simulada.
- `services/`: lógica de negocio y acceso a datos.
- `templates/`: vistas HTML con Bootstrap.
- `data/`: datos persistidos en JSON.
- `static/`: recursos estáticos adicionales.

## Ejecutar

```bash
cd admin_panel
pip install -r requirements.txt
python app.py
```

Luego abre `http://127.0.0.1:8501` en tu navegador.
