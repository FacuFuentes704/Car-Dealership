def test_login_exitoso(client, usuario_de_prueba):
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_defectuoso(client):
    response = client.post("/auth/login", json={
        "email": "mal@mal.com",
        "password": "mal121"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales incorrectas"

def test_login_inactivo(client, usuario_inactivo):
    response = client.post("/auth/login", json={
        "email": "test2@test.com",
        "password": "password123"
    })
    assert response.status_code == 403
    assert response.json()["detail"] == "Usuario inactivo"

def test_contraseña_incorrecta(client, usuario_de_prueba):
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "mal123"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales incorrectas"

def test_registrar_sin_token(client):
    response = client.post("/users/register", json={
        "name": "test",
        "email": "test3@test.com",
        "password": "test123"
    })
    assert response.status_code == 401

def test_registrar_con_token(client, token_usuario):
    response = client.post("/users/register", json={
        "name": "test",
        "email": "test3@test.com",
        "password": "test123"
    },
    headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert response.status_code == 200

def test_registrar_email_duplicado(client, usuario_de_prueba, token_usuario):
    response = client.post("/users/register", json={
        "name": "Test User",
        "email": "test@test.com",
        "password": "password123"
    },
    headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email duplicado"

def test_get_perfil_sin_token(client):
    response = client.get("/users/me")
    assert response.status_code == 401

def test_delete_perfil(client, token_usuario):
    response = client.delete(
        "/users/me",
        headers={"Authorization": f"Bearer {token_usuario}"}
    )
    assert response.status_code == 204
    login_response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "password123"
    })
    assert login_response.status_code == 403