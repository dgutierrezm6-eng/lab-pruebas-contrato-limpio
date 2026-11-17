import sqlite3
from flask import Flask, jsonify, request
from app.contratos_logica import calcular_valor_contrato, validar_contraparte

HTML_UI = '''
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8"><title>Contrato Limpio</title></head>
<body>
  <h1>Contrato Limpio - Gestión de Acuerdos</h1>
  <form id="form-contrato">
    <input id="titulo" placeholder="Título del contrato" required />
    <input id="creador" placeholder="Correo creador" required />
    <input id="contraparte" placeholder="Correo contraparte" required />
    <input id="hito_titulo" placeholder="Nombre del hito" required />
    <input id="hito_monto" type="number" placeholder="Monto del hito" required />
    <button id="btn-crear" type="submit">Crear y Fondear Contrato</button>
  </form>
  <p id="mensaje"></p>
  <script>
    document.getElementById('form-contrato').addEventListener('submit', async (e) => {
      e.preventDefault();
      const payload = {
        titulo: document.getElementById('titulo').value,
        creador: document.getElementById('creador').value,
        contraparte: document.getElementById('contraparte').value,
        hitos: [{
          titulo: document.getElementById('hito_titulo').value,
          monto: Number(document.getElementById('hito_monto').value)
        }]
      };
      const res = await fetch('/contratos', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      const msg = document.getElementById('mensaje');
      if (res.status === 201) {
        msg.textContent = `Contrato #${data.id} creado por $${data.valor} - Estado: ${data.estado}`;
      } else {
        msg.textContent = `Error: ${data.error}`;
      }
    });
  </script>
</body>
</html>
'''

def create_app(db_path='contratos.db'):
    app = Flask(__name__)

    def db():
        con = sqlite3.connect(db_path)
        con.row_factory = sqlite3.Row
        return con

    with db() as con:
        con.execute('''
            CREATE TABLE IF NOT EXISTS contratos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                creador TEXT NOT NULL,
                contraparte TEXT NOT NULL,
                valor REAL NOT NULL,
                estado TEXT NOT NULL
            )
        ''')
        con.execute('''
            CREATE TABLE IF NOT EXISTS hitos_contrato (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contrato_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                monto REAL NOT NULL
            )
        ''')
        con.execute('''
            CREATE TABLE IF NOT EXISTS custodia_escrow (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contrato_id INTEGER NOT NULL,
                monto REAL NOT NULL,
                estado TEXT NOT NULL
            )
        ''')

    @app.get('/')
    def home():
        return HTML_UI, 200

    @app.post('/contratos')
    def crear_contrato():
        datos = request.get_json(silent=True) or {}
        titulo = datos.get('titulo')
        creador = datos.get('creador', '')
        contraparte = datos.get('contraparte', '')
        hitos = datos.get('hitos')

        if not titulo or not isinstance(hitos, list):
            return jsonify(error='Datos incompletos o inválidos'), 400

        try:
            validar_contraparte(creador, contraparte)
            montos = [h['monto'] for h in hitos]
            valor_total = calcular_valor_contrato(montos)
        except (ValueError, KeyError, TypeError) as e:
            return jsonify(error=str(e)), 400

        with db() as con:
            cur = con.execute(
                'INSERT INTO contratos (titulo, creador, contraparte, valor, estado) VALUES (?, ?, ?, ?, ?)',
                (titulo, creador.strip().lower(), contraparte.strip().lower(), valor_total, 'Activo (Fondeado)')
            )
            cid = cur.lastrowid
            for h in hitos:
                con.execute(
                    'INSERT INTO hitos_contrato (contrato_id, titulo, monto) VALUES (?, ?, ?)',
                    (cid, h['titulo'], h['monto'])
                )
            con.execute(
                'INSERT INTO custodia_escrow (contrato_id, monto, estado) VALUES (?, ?, ?)',
                (cid, valor_total, 'En Custodia')
            )

        return jsonify(id=cid, titulo=titulo, valor=valor_total, estado='Activo (Fondeado)'), 201

    @app.get('/contratos/<int:cid>')
    def obtener_contrato(cid):
        with db() as con:
            contrato = con.execute('SELECT * FROM contratos WHERE id = ?', (cid,)).fetchone()
            if contrato is None:
                return jsonify(error='Contrato no encontrado'), 404
            hitos = con.execute('SELECT titulo, monto FROM hitos_contrato WHERE contrato_id = ?', (cid,)).fetchall()
            custodia = con.execute('SELECT monto, estado FROM custodia_escrow WHERE contrato_id = ?', (cid,)).fetchone()

        return jsonify(
            id=contrato['id'],
            titulo=contrato['titulo'],
            valor=contrato['valor'],
            estado=contrato['estado'],
            hitos=[dict(h) for h in hitos],
            custodia=dict(custodia)
        ), 200

    return app

if __name__ == '__main__':
    create_app().run(port=5001)
