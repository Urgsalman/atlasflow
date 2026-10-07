import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  vus: 50,          // Simule 50 utilisateurs virtuels en parallèle
  duration: '30s',  // Le test dure 30 secondes
};

export default function () {
  // On attaque l'endpoint de documentation Swagger (ou /api/orders) pour tester la latence web
  const res = http.get('http://host.docker.internal:8000/docs');
  
  // On vérifie que le service répond 200 OK et met moins de 500ms
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  sleep(1);
}