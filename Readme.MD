# 💸 API de Gestión de Gastos Personales

Esta API permite a los usuarios registrar, consultar, modificar y eliminar sus gastos e ingresos personales. También ofrece reportes y resúmenes financieros por período y categoría.

---

## 📦 Tecnologías utilizadas

- **Python** + **FastAPI**
- **PostgreSQL** (o SQLite en local)
- **SQLAlchemy** + **Alembic**
- **JWT** para autenticación
- **Docker** + `docker-compose`
- **Pytest** para testing
- **Pydantic** para validación de datos
- **bcrypt** para hashing de contraseñas
- *(Opcional)*: Celery + Redis para tareas asíncronas

---

## ⚙️ Requerimientos funcionales

### 🔐 Autenticación y usuarios

- `POST /auth/register`: Registro de usuario
- `POST /auth/login`: Login y obtención de JWT
- `POST /auth/refresh`: Renovar token
- `GET /users/me`: Obtener información del usuario actual

> 🛡️ Requiere protección de rutas mediante JWT

---

### 💰 Gestión de transacciones

- `GET /transactions`: Listar transacciones con filtros, orden y paginación
- `GET /transactions/{id}`: Detalle de una transacción
- `POST /transactions`: Crear transacción
- `PUT /transactions/{id}`: Modificar transacción
- `DELETE /transactions/{id}`: Eliminar transacción (soft delete)

**Campos esperados:**
```json
{
  "concept": "Alquiler",
  "amount": 50000,
  "type": "expense", // o "income"
  "category": "Vivienda",
  "date": "2025-06-01"
}
```

---

### 📊 Resúmenes y reportes

- `GET /summary/monthly`: Totales mensuales por tipo y balance general
- `GET /summary/yearly`: Evolución mes a mes
- `GET /summary/category-breakdown?month=2025-06`: Totales por categoría
- *(Opcional)*: `/summary/forecast` con predicciones simuladas

---

### 📁 Importación / exportación

- `POST /transactions/upload`: Subida de archivo CSV (validación y carga masiva)
- `GET /transactions/export`: Exportar datos en CSV o Excel
- `GET /transactions/history`: Ver historial de cargas/exportaciones

---

### ⚙️ Utilidades y administración

- `GET /categories`: Lista de categorías disponibles
- `GET /audit-log`: Auditoría del sistema (accesible solo por admin)
- `GET /health`: Endpoint de chequeo del estado del sistema

---

## 🧱 Estructura de proyecto sugerida

```
gastos_api/
├── app/
│   ├── main.py
│   ├── models/
│   ├── routers/
│   ├── services/
│   ├── schemas/
│   ├── core/
│   └── db/
├── tests/
├── alembic/
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🧪 Tests

- Autenticación (login, registro, tokens)
- CRUD de transacciones
- Validaciones y errores esperados
- Filtros, paginación, exportación
- Protección de rutas (autorización)

---

## 🚀 Para ejecutar el proyecto

```bash
# Clonar repositorio
git clone https://github.com/usuario/api-gastos.git
cd api-gastos

# Crear y configurar .env
cp .env.example .env

# Iniciar con Docker
docker-compose up --build

# Acceder a la documentación interactiva
http://localhost:8000/docs
```

---

## 📌 Pendientes / mejoras futuras

- Soporte de transacciones recurrentes
- Notificaciones por email (resumen mensual)
- Gráficos e integración frontend
- Multiusuario con roles (`admin`, `viewer`, etc.)
- Exportación a PDF y Excel

---

## 👨‍💻 Autor

Desarrollado por Matías Mazparrote  
📧 [TuEmail@dominio.com]  
🔗 [LinkedIn](https://www.linkedin.com/)

---