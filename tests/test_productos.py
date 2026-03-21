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
    assert data["precio"] == "15000.00"

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

def test_crear_producto_con_categoria_inexistente(client, admin_token):
    response = client.post("/productos/", json={
        "nombre": "Monitor",
        "precio": 3200.0,
        "categoria_id": 999
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 404
    assert "Categoría no encontrada" == response.json()["detail"]

def test_crear_producto_con_precio_invalido(client, admin_token):
    response = client.post("/productos/", json={
        "nombre": "Monitor",
        "precio": -50
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 422
    assert response.json()["error_code"] == "validation_error"

def test_soft_delete_oculta_producto_en_listado_por_defecto(client, admin_token):
    product = client.post("/productos/", json={
        "nombre": "Router",
        "precio": 1200.0,
        "stock": 4
    }, headers={"Authorization": f"Bearer {admin_token}"})
    producto_id = product.json()["id"]

    delete_response = client.delete(
        f"/productos/{producto_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert delete_response.status_code == 204

    list_response = client.get(
        "/productos/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert list_response.status_code == 200
    assert list_response.json() == []

    list_all_response = client.get(
        "/productos/?solo_activos=false",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert list_all_response.status_code == 200
    assert len(list_all_response.json()) == 1
    assert list_all_response.json()[0]["activo"] is False

def test_alertas_stock_retorna_solo_productos_activos(client, admin_token):
    low_stock_product = client.post("/productos/", json={
        "nombre": "Webcam",
        "precio": 900.0,
        "stock": 1,
        "stock_minimo": 2
    }, headers={"Authorization": f"Bearer {admin_token}"})
    inactive_product = client.post("/productos/", json={
        "nombre": "Micrófono",
        "precio": 1500.0,
        "stock": 1,
        "stock_minimo": 3
    }, headers={"Authorization": f"Bearer {admin_token}"})

    client.delete(
        f"/productos/{inactive_product.json()['id']}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.get(
        "/inventario/alertas",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == low_stock_product.json()["id"]
    assert data[0]["alerta"] == "stock bajo"

def test_movimiento_con_cantidad_invalida(client, admin_token):
    product = client.post("/productos/", json={
        "nombre": "SSD",
        "precio": 1800.0,
        "stock": 5
    }, headers={"Authorization": f"Bearer {admin_token}"})
    producto_id = product.json()["id"]

    response = client.post("/inventario/movimiento", json={
        "producto_id": producto_id,
        "tipo": "entrada",
        "cantidad": 0
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 422

def test_movimiento_sobre_producto_inactivo(client, admin_token):
    product = client.post("/productos/", json={
        "nombre": "Hub USB",
        "precio": 450.0,
        "stock": 5
    }, headers={"Authorization": f"Bearer {admin_token}"})
    producto_id = product.json()["id"]

    client.delete(
        f"/productos/{producto_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )

    response = client.post("/inventario/movimiento", json={
        "producto_id": producto_id,
        "tipo": "entrada",
        "cantidad": 2
    }, headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 409
    assert response.json()["detail"] == "El producto está inactivo"
