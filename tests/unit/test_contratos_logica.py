import pytest
from app.contratos_logica import calcular_valor_contrato, validar_contraparte

@pytest.mark.parametrize('hitos, esperado', [
    ([500000], 500000),
    ([150000, 350000], 500000),
    ([100.50, 200.25, 50.25], 351.0),
])
def test_calcular_valor_contrato(hitos, esperado):
    assert calcular_valor_contrato(hitos) == esperado

def test_contrato_sin_hitos():
    with pytest.raises(ValueError):
        calcular_valor_contrato([])

@pytest.mark.parametrize('hitos_invalidos', [
    [0],
    [100000, -50000],
])
def test_hito_monto_invalido(hitos_invalidos):
    with pytest.raises(ValueError):
        calcular_valor_contrato(hitos_invalidos)

def test_validar_contraparte_exitoso():
    assert validar_contraparte('danna@correo.com', 'Cliente@Empresa.co') is True

@pytest.mark.parametrize('correo_malo', ['sinarroba.com', 'usuario@sindominio', ''])
def test_correo_contraparte_invalido(correo_malo):
    with pytest.raises(ValueError):
        validar_contraparte('danna@correo.com', correo_malo)

def test_rechaza_contrato_consigo_mismo():
    with pytest.raises(ValueError):
        validar_contraparte('danna@correo.com', '  DANNA@correo.com ')
