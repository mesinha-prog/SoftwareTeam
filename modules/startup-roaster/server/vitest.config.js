import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    include: [
      '../test/component/resultStore.test.js',
      '../test/integration/api.test.js',
    ],
  },
});
