def calcular_valor_contrato(hitos):
    if not hitos:
        raise ValueError('El contrato debe tener al menos un hito')
    total = 0
    for monto in hitos:
        if monto <= 0:
            raise ValueError('El monto de cada hito debe ser mayor a cero')
        total += monto
    return round(total, 2)

def validar_contraparte(correo_creador, correo_contraparte):
    creador = correo_creador.strip().lower()
    contraparte = correo_contraparte.strip().lower()
    if '@' not in contraparte or '.' not in contraparte:
        raise ValueError('El correo de la contraparte no es válido')
    if creador == contraparte:
        raise ValueError('No puedes crear un contrato contigo mismo')
    return True
