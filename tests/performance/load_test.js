import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '5s', target: 3 },  // Sube a 3 usuarios virtuales
    { duration: '10s', target: 5 }, // Mantiene 5 usuarios simultáneos
    { duration: '5s', target: 0 },  // Baja gradualmente a 0
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // El 95% de peticiones debe responder en menos de 500 ms
    http_req_failed: ['rate<0.01'],   // Menos del 1% de fallos permitidos
  },
};

export default function () {
  const url = 'http://127.0.0.1:5001/contratos';
  const payload = JSON.stringify({
    titulo: `Contrato Carga VU-${__VU}`,
    creador: 'danna@correo.com',
    contraparte: 'cliente@empresa.co',
    hitos: [
      { titulo: 'Fase 1', monto: 250000 },
      { titulo: 'Fase 2', monto: 500000 },
    ],
  });

  const params = {
    headers: { 'Content-Type': 'application/json' },
  };

  // 1. Crear contrato bajo concurrencia
  const resPost = http.post(url, payload, params);
  check(resPost, {
    'POST estado 201': (r) => r.status === 201,
  });

  // 2. Consultar el contrato recién creado
  if (resPost.status === 201) {
    const id = resPost.json('id');
    const resGet = http.get(`${url}/${id}`);
    check(resGet, {
      'GET estado 200': (r) => r.status === 200,
    });
  }

  sleep(0.5);
}
