import http from 'k6/http';
import { check } from 'k6';
import { API_BASE_URL, K6_USERNAME, K6_PASSWORD } from './config.js';

export function loginAndGetToken() {
  const payload = {
    username: K6_USERNAME,
    password: K6_PASSWORD,
  };

  const response = http.post(
    `${API_BASE_URL}/auth/login`,
    payload,
    {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    }
  );

  check(response, {
    'login status is 200': (r) => r.status === 200,
    'login has access token': (r) => !!r.json('access_token'),
  });

  if (response.status !== 200) {
    return null;
  }

  return response.json('access_token');
}

export function authHeaders(token) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
      Accept: 'application/json',
    },
  };
}
