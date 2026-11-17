from playwright.sync_api import expect

def test_flujo_crear_contrato_en_navegador(page):
    page.goto('http://127.0.0.1:5001/')
    page.fill('#titulo', 'Diseño Plataforma E2E')
    page.fill('#creador', 'danna@correo.com')
    page.fill('#contraparte', 'empresa@cliente.co')
    page.fill('#hito_titulo', 'Entrega Final')
    page.fill('#hito_monto', '850000')
    page.click('#btn-crear')

    mensaje = page.locator('#mensaje')
    expect(mensaje).to_contain_text('creado por $850000 - Estado: Activo (Fondeado)')

def test_bloquea_autocontrato_en_navegador(page):
    page.goto('http://127.0.0.1:5001/')
    page.fill('#titulo', 'Contrato Inválido')
    page.fill('#creador', 'danna@correo.com')
    page.fill('#contraparte', 'danna@correo.com')
    page.fill('#hito_titulo', 'Hito Único')
    page.fill('#hito_monto', '100000')
    page.click('#btn-crear')

    mensaje = page.locator('#mensaje')
    expect(mensaje).to_contain_text('Error: No puedes crear un contrato contigo mismo')
