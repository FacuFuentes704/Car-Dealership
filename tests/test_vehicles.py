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