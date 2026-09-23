# LGi Motors — Sistema de Gestión para Agencia de Autos

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688)
![React](https://img.shields.io/badge/React-19-61DAFB)

Sistema de gestión para **LGi Motors**, una agencia de compra-venta de vehículos en Venado Tuerto, Santa Fe. Incluye un catálogo público y un panel de administración para vehículos, clientes, ventas y la documentación de cada operación.

**Sitio en producción:** [lgimotors.com](https://lgimotors.com)
**Documentación de la API:** [car-dealership-api-7k16.onrender.com/docs](https://car-dealership-api-7k16.onrender.com/docs)
**Repo del frontend:** [car-dealership-frontend](https://github.com/FacuFuentes704/car-dealership-frontend)

<!-- TODO: agregar capturas del catálogo público y del panel de admin -->

---

## Contexto del proyecto

Antes de este proyecto, la agencia gestionaba el stock y los clientes a mano, sin catálogo online ni ningún registro centralizado de ventas. Armé un sitio público con el catálogo filtrable y un panel de administración completo — vehículos, clientes, ventas y el boleto de compra-venta oficial — que la agencia usa hoy para operar, con datos y clientes reales.

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
- Responsive

### Panel de administración (protegido con JWT)

- Dashboard con estadísticas de vehículos y clientes
- Vehículos: alta/baja/edición, carga de múltiples fotos con foto principal, patente, precio de permuta y precio de contado (privado), número de motor/chasis, equipamiento, planilla de stock imprimible (solo vehículos activos y disponibles)
- Clientes: alta/baja/edición, domicilio/documento (para el boleto), historial de compras
- Intereses: relación entre clientes y vehículos, gestionable desde ambos lados
- Ventas: registro con desglose de pago (reserva, entrega, saldo financiado, cuotas), búsqueda y filtro por rango de fechas; al cerrarse, marca el vehículo como vendido y limpia sus intereses automáticamente
- Boleto de compra-venta: documento imprimible con el formato legal real que usa la agencia en papel, con modo edición/solo-lectura y datos autocompletados desde vehículo, cliente y venta
- Configuración de la agencia: datos fijos de la empresa usados en el boleto

---

## Decisiones técnicas

Algunas decisiones y problemas reales que aparecieron construyendo esto, no solo al escribir el código sino al ponerlo en uso real:

- **Separar `price` de `price_cash`**: el modelo de `Vehicle` original solo tenía un precio. La agencia necesitaba manejar precio de permuta y precio de contado por separado — tanto en el panel como distinguidos en la planilla impresa. No lo había contemplado al armar los modelos iniciales, así que agregué `price_cash` como campo nuevo en vez de forzar un mismo campo a cumplir dos funciones distintas.

- **Un campo JSON para el equipamiento (`features`)**: en vez de una columna booleana por cada característica del vehículo (aire acondicionado, ABS, airbags, etc.), usé una sola columna JSON. Agregar una característica nueva a la lista no requiere ninguna migración de base de datos, solo un cambio en el frontend.

- **Dónde guardar los datos del boleto**: motor y chasis del vehículo, domicilio y documento del cliente, son datos que recién se conocen al cerrar una venta, no al cargar el vehículo o el cliente. En vez de una tabla aparte ligada solo a esa venta, decidí que se guarden directamente en el vehículo y el cliente reales — así, si el mismo cliente vuelve a comprar, esos datos ya están cargados.

- **Rate limiting que no funcionaba en producción**: configuré `slowapi` para limitar los intentos de login por IP; en local funcionaba, en producción no bloqueaba nada. Render enruta el tráfico por su propia infraestructura, así que cada pedido le llegaba a mi backend desde una IP interna distinta de Render, no la del cliente real — nunca se acumulaban los intentos de la misma persona. Lo resolví leyendo la IP real desde el header `X-Forwarded-For`.

- **Services levantando `HTTPException` directamente**: en este proyecto, los services (no solo los routers) levantan excepciones HTTP cuando algo no existe o una regla de negocio falla. Es una práctica común en FastAPI, aunque técnicamente implica que la capa de datos conoce HTTP — una separación más estricta dejaría esa decisión únicamente en el router. Lo mantuve así por simplicidad, siendo consciente del trade-off.

---

## Arquitectura

**Backend** — capas separadas por responsabilidad:

```
Router → Service → Model (SQLAlchemy) → PostgreSQL
              ↓
          Schema (Pydantic) → Response
```

Cada recurso (`vehicles`, `clients`, `sales`, `users`, `company_settings`) sigue el mismo patrón: el router recibe la petición y delega, el service contiene la lógica de negocio, y los schemas de Pydantic validan entrada y salida por separado (`Create` / `Update` / `Response`), sin exponer el modelo de base de datos directamente.

**Frontend** — SPA de React organizada por dominio (`admin/Vehiculos`, `admin/Clientes`, `admin/Ventas`, `admin/Boleto`), con layouts separados para el sitio público y el panel privado.

---

## Stack técnico

**Backend**
- Python 3.11 + FastAPI
- SQLAlchemy + Alembic (migraciones versionadas)
- PostgreSQL
- JWT (`python-jose`) + hashing de contraseñas con `bcrypt`
- `slowapi` para rate limiting
- Cloudinary para almacenamiento de imágenes
- `pytest` — 31 tests automatizados
- Docker + despliegue en Render

**Frontend**
- React 19 + Vite
- React Router v7
- `fetch` nativo
- Despliegue en Vercel, dominio propio vía Namecheap

---

## Seguridad

- Contraseñas hasheadas con `bcrypt`, nunca almacenadas ni devueltas en texto plano
- Tokens JWT con expiración
- Rate limiting en el login (5 intentos por minuto por IP)
- CORS restringido al dominio de producción
- Sanitización de campos de texto libre antes de persistir
- Validación de variables de entorno al arrancar la aplicación
- Baja lógica (`is_active`) en vehículos y clientes en vez de borrado físico

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

```bash
python -m alembic upgrade head
python -m uvicorn main:app --reload
```

API disponible en `http://localhost:8000`, documentación en `http://localhost:8000/docs`.

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
