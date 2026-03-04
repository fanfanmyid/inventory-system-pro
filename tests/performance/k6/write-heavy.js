import http from 'k6/http';
import { check, sleep } from 'k6';
import { API_BASE_URL } from './config.js';
import { authHeaders, loginAndGetToken } from './helpers.js';

export const options = {
  scenarios: {
    write_flow: {
      executor: 'per-vu-iterations',
      vus: 3,
      iterations: 5,
      maxDuration: '2m',
    },
  },
  thresholds: {
    http_req_failed: ['rate<0.05'],
    http_req_duration: ['p(95)<2000'],
  },
};

function uniqueSuffix() {
  return `${Date.now()}-${__VU}-${__ITER}`;
}

export default function () {
  const token = loginAndGetToken();
  if (!token) return;

  const headers = authHeaders(token);
  const suffix = uniqueSuffix();

  const productPayload = JSON.stringify({
    sku: `K6-${suffix}`,
    name: `k6-item-${suffix}`,
    description: 'k6 write-heavy scenario product',
    price: 25000,
    stock: 25,
  });

  const createProductRes = http.post(`${API_BASE_URL}/products/`, productPayload, headers);
  check(createProductRes, {
    'create product status 200': (r) => r.status === 200,
    'create product has id': (r) => !!r.json('id'),
  });

  if (createProductRes.status !== 200) {
    return;
  }

  const productId = createProductRes.json('id');

  const txPayload = JSON.stringify({
    product_id: productId,
    transaction_type: 'OUT',
    quantity: 1,
    reference: `k6-${suffix}`,
  });

  const txRes = http.post(`${API_BASE_URL}/transactions/`, txPayload, headers);
  check(txRes, {
    'create transaction status 200': (r) => r.status === 200,
  });

  const salePayload = JSON.stringify({
    invoice_number: `INV-K6-${suffix}`,
    total_price: 25000,
    items: [
      {
        product_id: productId,
        quantity: 1,
        unit_price: 25000,
      },
    ],
  });

  const saleRes = http.post(`${API_BASE_URL}/sales/`, salePayload, headers);
  check(saleRes, {
    'create sale status 200': (r) => r.status === 200,
  });

  sleep(1);
}
