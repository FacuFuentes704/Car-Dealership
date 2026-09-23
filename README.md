# LGi Motors — Sistema de Gestión para Agencia de Autos

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688)
![React](https://img.shields.io/badge/React-19-61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791)
![License](https://img.shields.io/badge/license-privado-lightgrey)

Sistema full-stack real, en producción, construido para **LGi Motors**, una agencia de compra-venta de vehículos en Venado Tuerto, Santa Fe (Argentina). Incluye un catálogo público y un panel de administración completo para gestionar vehículos, clientes, ventas y la documentación legal de cada operación.

**🔗 Sitio en producción:** [lgimotors.com](https://lgimotors.com)
**📄 Documentación de la API (Swagger):** [car-dealership-api-7k16.onrender.com/docs](https://car-dealership-api-7k16.onrender.com/docs)
**🖥️ Repo del frontend:** [car-dealership-frontend](https://github.com/FacuFuentes704/car-dealership-frontend)

<!-- TODO: agregar capturas de pantalla del catálogo público y del panel de admin -->

---

## Contexto del proyecto

LGi Motors gestionaba su stock y sus clientes de forma manual, sin ningún catálogo online ni un sistema centralizado para hacer seguimiento de ventas. Este proyecto resuelve ambos problemas: un **sitio público** donde cualquier persona puede ver el stock disponible, filtrarlo y contactar por WhatsApp, y un **panel privado** donde el personal de la agencia administra vehículos, clientes, intereses, ventas y genera el boleto de compra-venta oficial — replicando el formato de papel que la agencia ya usaba, pero con los datos autocompletados desde el sistema.

No es un proyecto de práctica aislado: es la herramienta que la agencia usa hoy, con datos y clientes reales.

---

## Funcionalidades

### Sitio público

- Catálogo de vehículos con filtros (marca, modelo, año, precio, km, combustible, transmisión, condición)
- Páginas dedicadas: 0KM, Usados, Ofertas
- Detalle de vehículo con galería de fotos, ficha técnica y equipamiento (aire, ABS, airbags, etc.)
- Botón de contacto directo por WhatsApp, con mensaje pre-armado según el vehículo
- Página de financiación
- Modo oscuro / claro
- SEO básico (meta description, Open Graph) y política de privacidad
- Totalmente responsive

### Panel de administración (protegido con JWT)

- **Dashboard** con estadísticas de vehículos y clientes
- **Vehículos**: alta/baja/edición, carga de múltiples fotos con foto principal, patente, precio de permuta y precio de contado (privado), número de motor/chasis, equipamiento, planilla de stock imprimible (solo vehículos activos y disponibles)
- **Clientes**: alta/baja/edición, domicilio/documento (para el boleto), historial de compras
- **Intereses**: relación muchos-a-muchos entre clientes y vehículos, gestionable desde ambos lados
- **Ventas**: registro con desglose de pago (reserva, entrega, saldo financiado, cuotas), búsqueda y filtro por rango de fechas; al cerrarse, marca el vehículo como vendido y limpia sus intereses automáticamente
- **Boleto de compra-venta**: documento imprimible con el formato legal real usado por la agencia, con modo edición/solo-lectura y datos autocompletados desde vehículo, cliente y venta
- **Configuración de la agencia**: datos fijos de la empresa (razón social, domicilio, CUIT) usados en el boleto

---

## Arquitectura

**Backend** — arquitectura en capas clásica:

```
Router → Service → Model (SQLAlchemy) → PostgreSQL
              ↓
          Schema (Pydantic) → Response
```

Cada recurso (`vehicles`, `clients`, `sales`, `users`, `company_settings`) sigue el mismo patrón: el router recibe la petición y delega, el service contiene la lógica de negocio, y los schemas de Pydantic validan entrada y salida por separado (`Create` / `Update` / `Response`), sin exponer nunca el modelo de base de datos directamente.

**Frontend** — SPA de React organizada por dominio (`admin/Vehiculos`, `admin/Clientes`, `admin/Ventas`, `admin/Boleto`), con capas de admin (protegidas) y público separadas mediante layouts distintos, cada uno con su propio `<Outlet />`.

---

## Stack técnico

**Backend**
- Python 3.11 + FastAPI
- SQLAlchemy + Alembic (migraciones versionadas)
- PostgreSQL
- Autenticación JWT (`python-jose`) + hashing de contraseñas con `bcrypt`
- `slowapi` para rate limiting (protección contra fuerza bruta en el login)
- Cloudinary para almacenamiento de imágenes
- `pytest` — 31 tests automatizados (auth, CRUD, reglas de negocio, rate limiting)
- Docker + despliegue en Render

**Frontend**
- React 19 + Vite
- React Router v7
- `fetch` nativo (sin librerías de estado de servidor)
- Despliegue en Vercel, dominio propio vía Namecheap

---

## Seguridad

- Contraseñas hasheadas con `bcrypt`, nunca almacenadas ni devueltas en texto plano
- Tokens JWT con expiración
- Rate limiting en el login (5 intentos por minuto por IP, detectando la IP real detrás del proxy de Render vía `X-Forwarded-For`)
- CORS restringido al dominio de producción
- Sanitización de campos de texto libre (`html.escape`) antes de persistir
- Validación de variables de entorno al arrancar la aplicación (falla rápido y con mensaje claro si falta una)
- Baja lógica (`is_active`) en vehículos y clientes en vez de borrado físico — preserva el historial

---

## Cómo correrlo localmente

### Backend

```bash
git clone https://github.com/FacuFuentes704/Car-Dealership.git
cd Car-Dealership
pip install -r requirements.txt --break-system-packages
```

Creá un archivo `.env` en la raíz con:

```
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
DB_NAME=
SECRET_KEY=
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=120
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
```

Aplicá las migraciones y levantá el servidor:

```bash
python -m alembic upgrade head
python -m uvicorn main:app --reload
```

La API queda disponible en `http://localhost:8000`, con documentación interactiva en `http://localhost:8000/docs`.

### Tests

```bash
python -m pytest -v
```

### Frontend

```bash
git clone https://github.com/FacuFuentes704/car-dealership-frontend.git
cd car-dealership-frontend
npm install
npm run dev
```

Disponible en `http://localhost:5173`.

---

## Despliegue

| Componente | Plataforma |
|---|---|
| API (backend) | Render — Web Service |
| Base de datos | Render — PostgreSQL |
| Frontend | Vercel |
| Dominio | `lgimotors.com` (Namecheap) |

El backend usa Docker con un `entrypoint.sh` que corre las migraciones de Alembic automáticamente antes de levantar `uvicorn` en cada deploy.

---

## Roadmap

- Sección de usuarios (cambio de contraseña, alta de nuevos empleados desde el panel)
- Cotizador de vehículos y simulador de financiación
- Gráficos comparativos de ventas mes a mes

---

## Autor

**Facundo Fuentes** — estudiante de la Tecnicatura en Programación, UTN Facultad Regional Venado Tuerto.
[GitHub](https://github.com/FacuFuentes704)
