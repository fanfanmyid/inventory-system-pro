import http from 'k6/http';
import { check, sleep } from 'k6';
import { API_BASE_URL } from './config.js';
import { authHeaders, loginAndGetToken } from './helpers.js';

export const options = {
  vus: 1,
  iterations: 5,
  thresholds: {
    http_req_failed: ['rate<0.01'],
    http_req_duration: ['p(95)<1000'],
  },
};

export default function () {
  const token = loginAndGetToken();
  check(token, {
    'token exists': (t) => t !== null,
  });

  if (!token) {
    return;
  }

  const productsRes = http.get(`${API_BASE_URL}/products/`, authHeaders(token));
  check(productsRes, {
    'products status is 200': (r) => r.status === 200,
  });

  const txRes = http.get(`${API_BASE_URL}/transactions/?page=1&size=10`, authHeaders(token));
  check(txRes, {
    'transactions status is 200': (r) => r.status === 200,
  });

  const salesRes = http.get(`${API_BASE_URL}/sales/?page=1&size=10`, authHeaders(token));
  check(salesRes, {
    'sales status is 200': (r) => r.status === 200,
  });

  sleep(1);
}
