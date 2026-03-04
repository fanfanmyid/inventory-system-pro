import http from 'k6/http';
import { check, sleep } from 'k6';
import { API_BASE_URL } from './config.js';
import { authHeaders, loginAndGetToken } from './helpers.js';

export const options = {
  scenarios: {
    constant_load: {
      executor: 'ramping-vus',
      stages: [
        { duration: '30s', target: 5 },
        { duration: '1m', target: 15 },
        { duration: '30s', target: 0 },
      ],
      gracefulRampDown: '10s',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.02'],
    http_req_duration: ['p(95)<1500', 'p(99)<2500'],
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

  const headers = authHeaders(token);

  const responses = http.batch([
    ['GET', `${API_BASE_URL}/products/?limit=20`, null, headers],
    ['GET', `${API_BASE_URL}/transactions/?page=1&size=10`, null, headers],
    ['GET', `${API_BASE_URL}/sales/?page=1&size=10`, null, headers],
  ]);

  check(responses[0], { 'products status 200': (r) => r.status === 200 });
  check(responses[1], { 'transactions status 200': (r) => r.status === 200 });
  check(responses[2], { 'sales status 200': (r) => r.status === 200 });

  sleep(1);
}
