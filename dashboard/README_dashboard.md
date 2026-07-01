# Dashboard Web — MindScope

Este directorio contiene el **dashboard HTML** del proyecto `cognitive-tracker`.

## Archivos

| Archivo | Descripción |
|---------|-------------|
| `index.html` | Dashboard web estático inspirado en la referencia de diseño del usuario. No requiere build. |
| `server.py` | Servidor FastAPI que sirve el HTML y expone endpoints de API JSON. |

## Cómo usar

### Opción 1 — Abrir directo en el navegador

```bash
xdg-open dashboard/index.html   # Linux
open dashboard/index.html        # macOS
```

### Opción 2 — Servidor FastAPI (recomendado)

Sirve el HTML en `http://localhost:8000` y activa los endpoints de la API:

```bash
uvicorn dashboard.server:app --reload
```

Luego abre: [http://localhost:8000](http://localhost:8000)

### Endpoints de API disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Sirve el dashboard HTML |
| GET | `/api/sessions` | Todas las sesiones grabadas |
| GET | `/api/sessions/{type}` | Sesiones por tipo (`logic`, `memory`, `arithmetic`) |
| GET | `/api/summary` | Resumen: promedio, última nota y conteo por tipo |

## Próximos pasos

- Conectar el botón "Comenzar" de cada tarjeta a formularios reales de tests
- Leer datos reales desde `/api/sessions` con `fetch()` en JavaScript
- Agregar autenticación si el dashboard se despliega en un servidor público
