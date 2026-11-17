import pytest
from app.api import create_app

@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / 'test_contratos.db'))
    return app.test_client()

def crear_contrato_valido(client):
    return client.post('/contratos', json={
        'titulo': 'Desarrollo Web',
        'creador': 'danna@correo.com',
        'contraparte': 'cliente@empresa.co',
        'hitos': [
            {'titulo': 'Diseño UI', 'monto': 300000},
            {'titulo': 'Backend API', 'monto': 700000}
        ]
    })

def test_crear_y_consultar_contrato_atomico(client):
    res = crear_contrato_valido(client)
    assert res.status_code == 201
    data = res.get_json()
    assert data['valor'] == 1000000
    cid = data['id']

    res_get = client.get(f'/contratos/{cid}')
    assert res_get.status_code == 200
    detalle = res_get.get_json()
    assert len(detalle['hitos']) == 2
    assert detalle['custodia']['estado'] == 'En Custodia'
    assert detalle['custodia']['monto'] == 1000000

def test_contrato_inexistente_devuelve_404(client):
    assert client.get('/contratos/999').status_code == 404

def test_rechaza_datos_incompletos(client):
    res = client.post('/contratos', json={'titulo': 'Sin hitos'})
    assert res.status_code == 400

def test_rechaza_mismo_usuario_en_api(client):
    res = client.post('/contratos', json={
        'titulo': 'Contrato Inválido',
        'creador': 'danna@correo.com',
        'contraparte': 'danna@correo.com',
        'hitos': [{'titulo': 'Hito 1', 'monto': 100000}]
    })
    assert res.status_code == 400
