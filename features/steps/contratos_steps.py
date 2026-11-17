from behave import given, when, then
from app.contratos_logica import calcular_valor_contrato, validar_contraparte

@given('que el creador es "{creador}" y la contraparte es "{contraparte}"')
def step_definir_partes(context, creador, contraparte):
    context.creador = creador
    context.contraparte = contraparte
    context.error = None

@when('registra un contrato llamado "{titulo}" con hitos de {m1:d} y {m2:d}')
def step_registrar_contrato(context, titulo, m1, m2):
    context.validacion = validar_contraparte(context.creador, context.contraparte)
    context.valor_total = calcular_valor_contrato([m1, m2])

@then('el valor total calculado debe ser {esperado:d}')
def step_verificar_total(context, esperado):
    assert context.valor_total == esperado

@then('el estado de validación de la contraparte debe ser exitoso')
def step_verificar_validacion(context):
    assert context.validacion is True

@when('intenta validar las partes del contrato')
def step_intentar_validar(context):
    try:
        validar_contraparte(context.creador, context.contraparte)
    except ValueError as e:
        context.error = str(e)

@then('el sistema debe rechazar la operación con el error "{mensaje_esperado}"')
def step_verificar_error(context, mensaje_esperado):
    assert context.error == mensaje_esperado
