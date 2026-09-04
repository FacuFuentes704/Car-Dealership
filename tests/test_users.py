def test_login_exitoso(client, usuario_de_prueba):
    response = client.post("/auth/login", json={
        "email": "test@test.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()