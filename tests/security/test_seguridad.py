import pytest
from app.api import create_app

@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "seguridad_test.db"
    app = create_app(str(db_file))
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_resistencia_inyeccion_sql(client):
    payload_sqli = {
        "titulo": "Contrato'; DROP TABLE contratos; --",
        "creador": "atacante@correo.com",
        "contraparte": "victima@empresa.co",
        "hitos": [{"titulo": "Hito 1", "monto": 100000}]
    }
    res = client.post("/contratos", json=payload_sqli)
    assert res.status_code == 201
    cid = res.get_json()["id"]

    # Verifica que la tabla contratos sigue intacta y guardó el texto como literal seguro
    consulta = client.get(f"/contratos/{cid}")
    assert consulta.status_code == 200
    assert consulta.get_json()["titulo"] == "Contrato'; DROP TABLE contratos; --"

def test_bloquea_fraude_monto_negativo(client):
    payload_fraude = {
        "titulo": "Intento de extracción de fondos",
        "creador": "atacante@correo.com",
        "contraparte": "victima@empresa.co",
        "hitos": [{"titulo": "Hito fraudulento", "monto": -500000}]
    }
    res = client.post("/contratos", json=payload_fraude)
    assert res.status_code == 400

def test_rechaza_payload_malformado_sin_exponer_traza(client):
    res = client.post("/contratos", data="no-es-json", content_type="application/json")
    assert res.status_code == 400
    cuerpo = res.get_json()
    assert "error" in cuerpo
    assert "Traceback" not in str(cuerpo)
