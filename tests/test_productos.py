def test_crear_producto_como_admin(client, admin_token):
    response = client.post("/productos/", json={
        "nombre": "Laptop",
        "descripcion": "Laptop gamer",
        "precio": 15000.0,
        "stock": 10,
        "stock_minimo": 3
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Laptop"
    assert data["stock"] == 10

def test_crear_producto_sin_permiso(client, usuario_token):
    response = client.post("/productos/", json={
        "nombre": "Laptop",
        "precio": 15000.0
    }, headers={"Authorization": f"Bearer {usuario_token}"})
    assert response.status_code == 403

def test_listar_productos(client, admin_token):
    client.post("/productos/", json={
        "nombre": "Laptop",
        "precio": 15000.0,
        "stock": 10
    }, headers={"Authorization": f"Bearer {admin_token}"})
    response = client.get("/productos/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_obtener_producto_no_existe(client, usuario_token):
    response = client.get("/productos/999",
        headers={"Authorization": f"Bearer {usuario_token}"}
    )
    assert response.status_code == 404

def test_crear_categoria_como_admin(client, admin_token):
    response = client.post("/productos/categorias", json={
        "nombre": "Electrónica",
        "descripcion": "Productos electrónicos"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    assert response.json()["nombre"] == "Electrónica"

def test_movimiento_entrada(client, admin_token):
    product = client.post("/productos/", json={
        "nombre": "Mouse",
        "precio": 500.0,
        "stock": 5
    }, headers={"Authorization": f"Bearer {admin_token}"})
    producto_id = product.json()["id"]

    response = client.post("/inventario/movimiento", json={
        "producto_id": producto_id,
        "tipo": "entrada",
        "cantidad": 10,
        "nota": "Restock"
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 201
    assert response.json()["cantidad"] == 10

def test_movimiento_salida_stock_insuficiente(client, admin_token):
    product = client.post("/productos/", json={
        "nombre": "Teclado",
        "precio": 800.0,
        "stock": 2
    }, headers={"Authorization": f"Bearer {admin_token}"})
    producto_id = product.json()["id"]

    response = client.post("/inventario/movimiento", json={
        "producto_id": producto_id,
        "tipo": "salida",
        "cantidad": 10
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 400
    assert "insuficiente" in response.json()["detail"]