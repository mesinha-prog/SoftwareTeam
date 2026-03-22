import { v4 as uuidv4 } from 'uuid';

const store = new Map();

export function save(result) {
  const id = uuidv4();
  store.set(id, { id, ...result });
  return id;
}

export function get(id) {
  return store.get(id) ?? null;
}
