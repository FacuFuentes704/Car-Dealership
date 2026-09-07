def test_get_client_sin_token(client, cliente_creado):
    response = client.get("/clients/")
    assert response.status_code == 401

def test_delete_client(client, token_usuario, cliente_creado):
    response = client.delete(f"/clients/{cliente_creado.id}",
                             headers= {"Authorization": f"Bearer {token_usuario}"})
    assert response.status_code == 204

    response2 = client.get(f"/clients/{cliente_creado.id}",
                           headers={"Authorization": f"Bearer {token_usuario}"})
    assert response2.status_code == 200
    assert response2.json()["is_active"] == False

def test_post_client_sin_token(client):
    response = client.post("/clients/", json={
        "name": "test1",
        "phone": "1234",
        "email": "test22@gmail.com"
    })
    assert response.status_code == 401

def test_update_sin_token(client, cliente_creado):
    response = client.patch(f"/clients/{cliente_creado.id}", json={
        "name": "test2",
        "phone": "4455"
    })
    assert response.status_code == 401

def test_crear_interes_con_token(client, token_usuario, cliente_creado, vehiculo_creado):
    response = client.post(
        f"/clients/{cliente_creado.id}/interests/{vehiculo_creado.id}",
        headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert response.status_code == 200

def test_delete_interes(client, client_interest, vehiculo_creado, cliente_creado, token_usuario):
    response = client.delete(f"/clients/{cliente_creado.id}/interests/{vehiculo_creado.id}",
                             headers={"Authorization": f"Bearer {token_usuario}"})
    assert response.status_code == 204

def test_get_client_interests(client, token_usuario, client_interest, cliente_creado):
    response = client.get(f"/clients/{cliente_creado.id}",
                          headers={"Authorization": f"Bearer {token_usuario}"})
    assert response.status_code == 200
    respuesta = response.json()
    assert "interests" in respuesta

def test_crear_interes_sin_token(client, cliente_creado, vehiculo_creado):
    response = client.post(f"/clients/{cliente_creado.id}/interests/{vehiculo_creado.id}")
    assert response.status_code == 401

