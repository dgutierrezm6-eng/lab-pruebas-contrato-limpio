# language: es
Característica: Gestión y validación de contratos en Contrato Limpio
  Como usuario de Contrato Limpio
  Quiero crear acuerdos con hitos definidos y validación de contraparte
  Para asegurar que los montos y participantes cumplan las reglas del sistema

  Escenario: Creación exitosa de un contrato con múltiples hitos
    Dado que el creador es "danna@correo.com" y la contraparte es "cliente@empresa.co"
    Cuando registra un contrato llamado "Desarrollo Web" con hitos de 300000 y 700000
    Entonces el valor total calculado debe ser 1000000
    Y el estado de validación de la contraparte debe ser exitoso

  Escenario: Rechazo de un contrato consigo mismo
    Dado que el creador es "danna@correo.com" y la contraparte es "danna@correo.com"
    Cuando intenta validar las partes del contrato
    Entonces el sistema debe rechazar la operación con el error "No puedes crear un contrato contigo mismo"
