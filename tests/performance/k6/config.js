import { SharedArray } from 'k6/data';

const API_BASE_URL = __ENV.API_BASE_URL;
const K6_USERNAME = __ENV.K6_USERNAME;
const K6_PASSWORD = __ENV.K6_PASSWORD;

if (!API_BASE_URL || !K6_USERNAME || !K6_PASSWORD) {
  throw new Error('Missing required env: API_BASE_URL, K6_USERNAME, K6_PASSWORD');
}

const PRODUCTS = new SharedArray('products_payload', () => [
  {
    sku: `K6-SKU-${Date.now()}-1`,
    name: 'K6 Product 1',
    description: 'k6 generated product payload',
    price: 10000,
    stock: 20,
  },
  {
    sku: `K6-SKU-${Date.now()}-2`,
    name: 'K6 Product 2',
    description: 'k6 generated product payload',
    price: 15000,
    stock: 15,
  },
]);

export {
  API_BASE_URL,
  K6_USERNAME,
  K6_PASSWORD,
  PRODUCTS,
};
