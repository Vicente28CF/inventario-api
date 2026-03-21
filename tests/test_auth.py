def test_registro_exitoso(client):
    response = client.post("/auth/registro", json={
        "nombre": "Vicente",
        "email": "vicente@test.com",
        "password": "123456"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "vicente@test.com"
    assert data["rol"] == "viewer"

def test_registro_email_duplicado(client):
    client.post("/auth/registro", json={
        "nombre": "Vicente",
        "email": "vicente@test.com",
        "password": "123456"
    })
    response = client.post("/auth/registro", json={
        "nombre": "Vicente",
        "email": "vicente@test.com",
        "password": "123456"
    })
    assert response.status_code == 400
    assert "ya está registrado" in response.json()["detail"]
    assert response.json()["error_code"] == "http_error"

def test_login_exitoso(client):
    client.post("/auth/registro", json={
        "nombre": "Vicente",
        "email": "vicente@test.com",
        "password": "123456"
    })
    response = client.post("/auth/login", data={
        "username": "vicente@test.com",
        "password": "123456"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_credenciales_incorrectas(client):
    response = client.post("/auth/login", data={
        "username": "noexiste@test.com",
        "password": "wrong"
    })
    assert response.status_code == 401
    assert response.json()["error_code"] == "http_error"

def test_me_autenticado(client, usuario_token):
    response = client.get("/auth/me", headers={
        "Authorization": f"Bearer {usuario_token}"
    })
    assert response.status_code == 200
    assert response.json()["email"] == "vicente@test.com"

def test_me_sin_token(client):
    response = client.get("/auth/me")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"
