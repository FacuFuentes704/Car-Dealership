from app.models.sale import PaymentMethod

def test_ver_venta_sin_token(client, venta_creada):
    response = client.get("/sales/")
    assert response.status_code == 401

def test_post_venta_sin_token(client, vehiculo_creado, usuario_de_prueba, cliente_creado):
    response = client.post("/sales/", json={
        "vehicle_id": vehiculo_creado.id,
        "client_id": cliente_creado.id,
        "sale_price": 2221,
        "payment_method": "cash"
    })
    assert response.status_code == 401

def test_post_venta_con_token(client, token_usuario, vehiculo_creado, usuario_de_prueba, cliente_creado):
    response = client.post("/sales/", json={
        "vehicle_id": vehiculo_creado.id,
        "client_id": cliente_creado.id,
        "sale_price": 2221,
        "payment_method": "cash"
    },
    headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert response.status_code == 200

def test_venta_no_disponible(client, vehiculo_no_disponible, token_usuario, cliente_creado):
    response = client.post("/sales/", json={
        "vehicle_id": vehiculo_no_disponible.id,
        "client_id": cliente_creado.id,
        "sale_price": 2221,
        "payment_method": "cash"
    },
    headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Vehiculo no disponible"

def test_venta_sold(client, token_usuario, vehiculo_creado, usuario_de_prueba, cliente_creado):
    response = client.post("/sales/", json={
        "vehicle_id": vehiculo_creado.id,
        "client_id": cliente_creado.id,
        "sale_price": 2221,
        "payment_method": "cash"
    },
    headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert response.status_code == 200

    response2 = client.get(f"/vehicles/{vehiculo_creado.id}/")
    assert response2.status_code == 200
    assert response2.json()["status"] == "sold"

def test_venta_vehiculo_inactivo(client, vehiculo_inactivo, cliente_creado, token_usuario):
    response = client.post("/sales/", json={
        "vehicle_id": vehiculo_inactivo.id,
        "client_id": cliente_creado.id,
        "sale_price": 2221,
        "payment_method": "cash"
    },
    headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Vehiculo inactivo"