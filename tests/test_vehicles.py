def test_crear_vehiculo_con_token(client, token_usuario):
    response = client.post("/vehicles/", json={
        "fuel_type": "gasoline",
        "transmission": "manual",
        "status": "available",
        "color": "negro",
        "brand": "Toyota", 
        "model": "Corolla", 
        "year": 2026, 
        "plate": "AI 111 111", 
        "km": 1000, 
        "price": 40000000, 
        "description": "descripcion de prueba", 
        "condition": "used", 
        "is_active": True
    },
    headers= {"Authorization": f"Bearer {token_usuario}"}
    )
    assert response.status_code == 200

def test_crear_vehiculo_sin_token(client):
    response = client.post("/vehicles/", json={
        "fuel_type": "gasoline",
        "transmission": "manual",
        "status": "available",
        "color": "negro",
        "brand": "Toyota", 
        "model": "Corolla", 
        "year": 2026, 
        "plate": "AI 111 111", 
        "km": 1000, 
        "price": 40000000, 
        "description": "descripcion de prueba", 
        "condition": "used", 
        "is_active": True
    })
    assert response.status_code == 401

def test_update_vehiculo_sin_token(client, vehiculo_creado):
    response = client.patch(f"/vehicles/{vehiculo_creado.id}", json={
        "brand": "prueba"
    })
    assert response.status_code == 401

def test_delete_vehiculo_sin_token(client, vehiculo_creado):
    response = client.delete(f"/vehicles/{vehiculo_creado.id}")
    assert response.status_code == 401

def test_catalogo_publico(client):
    response = client.get("/vehicles/")
    assert response.status_code == 200
    vehiculos = response.json()
    for vehiculo in vehiculos:
        assert "interested_clients" not in vehiculo

def test_catalogo_activos(client, vehiculo_creado, vehiculo_inactivo):
    response = client.get("/vehicles/")
    assert response.status_code == 200
    vehiculos = response.json()
    marcas = [v["brand"] for v in vehiculos]

    assert "Toyota" in marcas
    assert "Ford" not in  marcas

def test_admin_ve_inactivos(client, vehiculo_creado, vehiculo_inactivo, token_usuario):
    response = client.get("/vehicles/admin",
                          headers= {"Authorization": f"Bearer {token_usuario}"})
    assert response.status_code == 200
    vehiculos = response.json()
    marcas = [vehiculo["brand"] for vehiculo in vehiculos]

    assert "Toyota" in marcas
    assert "Ford" in marcas



def _vehiculo_payload(**extra):
    base = {
        "fuel_type": "gasoline",
        "transmission": "manual",
        "status": "available",
        "color": "negro",
        "brand": "Toyota",
        "model": "Corolla",
        "year": 2026,
        "plate": "AI 111 111",
        "description": "descripcion de prueba",
        "condition": "used",
    }
    base.update(extra)
    return base

def test_crear_vehiculo_km_oculto_se_guarda_interno(client, token_usuario):
    headers = {"Authorization": f"Bearer {token_usuario}"}
    response = client.post("/vehicles/", json=_vehiculo_payload(km=None, km_internal=45000), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["km"] is None
    assert data["km_internal"] == 45000

def test_crear_vehiculo_solo_km_completa_km_interno(client, token_usuario):
    headers = {"Authorization": f"Bearer {token_usuario}"}
    response = client.post("/vehicles/", json=_vehiculo_payload(km=1000), headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["km"] == 1000
    assert data["km_internal"] == 1000

def test_actualizar_ocultar_km_conserva_interno(client, token_usuario, vehiculo_creado):
    headers = {"Authorization": f"Bearer {token_usuario}"}
    response = client.patch(f"/vehicles/{vehiculo_creado.id}",
                            json={"km": None, "km_internal": 1000}, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["km"] is None
    assert data["km_internal"] == 1000

def test_actualizar_solo_km_sincroniza_interno(client, token_usuario, vehiculo_creado):
    headers = {"Authorization": f"Bearer {token_usuario}"}
    response = client.patch(f"/vehicles/{vehiculo_creado.id}", json={"km": 2500}, headers=headers)
    assert response.status_code == 200
    assert response.json()["km_internal"] == 2500

def test_catalogo_publico_no_expone_km_interno(client, token_usuario):
    headers = {"Authorization": f"Bearer {token_usuario}"}
    creado = client.post("/vehicles/", json=_vehiculo_payload(km=None, km_internal=45000), headers=headers).json()

    listado = client.get("/vehicles/").json()
    assert all("km_internal" not in v for v in listado)
    detalle = client.get(f"/vehicles/{creado['id']}").json()
    assert "km_internal" not in detalle
    assert detalle["km"] is None

def test_admin_ve_km_interno(client, token_usuario):
    headers = {"Authorization": f"Bearer {token_usuario}"}
    creado = client.post("/vehicles/", json=_vehiculo_payload(km=None, km_internal=45000), headers=headers).json()
    detalle = client.get(f"/vehicles/{creado['id']}/admin", headers=headers).json()
    assert detalle["km_internal"] == 45000


def test_vehiculo_sin_publicar_no_aparece_en_catalogo_publico(client, token_usuario):
    headers = {"Authorization": f"Bearer {token_usuario}"}
    creado = client.post("/vehicles/", json=_vehiculo_payload(status="unpublished"), headers=headers)
    assert creado.status_code == 200
    assert creado.json()["status"] == "unpublished"
    vehiculo_id = creado.json()["id"]

    # Ni sin filtro de status ni pidiendolo explicitamente
    assert vehiculo_id not in [v["id"] for v in client.get("/vehicles/").json()]
    assert vehiculo_id not in [v["id"] for v in client.get("/vehicles/?status=unpublished").json()]
    # Ni por link directo
    assert client.get(f"/vehicles/{vehiculo_id}").status_code == 404

def test_vehiculo_sin_publicar_aparece_en_admin(client, token_usuario):
    headers = {"Authorization": f"Bearer {token_usuario}"}
    vehiculo_id = client.post("/vehicles/", json=_vehiculo_payload(status="unpublished"), headers=headers).json()["id"]

    ids = [v["id"] for v in client.get("/vehicles/admin?status=unpublished", headers=headers).json()]
    assert vehiculo_id in ids
    assert client.get(f"/vehicles/{vehiculo_id}/admin", headers=headers).status_code == 200

def test_publicar_vehiculo_lo_muestra_en_catalogo(client, token_usuario):
    headers = {"Authorization": f"Bearer {token_usuario}"}
    vehiculo_id = client.post("/vehicles/", json=_vehiculo_payload(status="unpublished"), headers=headers).json()["id"]
    client.patch(f"/vehicles/{vehiculo_id}", json={"status": "available"}, headers=headers)
    assert vehiculo_id in [v["id"] for v in client.get("/vehicles/").json()]
