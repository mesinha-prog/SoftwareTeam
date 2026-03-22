import 'dotenv/config';
import express from 'express';
import cors from 'cors';
import { createServer } from 'net';
import path from 'path';
import { fileURLToPath } from 'url';
import roastRouter from './routes/roast.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function isPortAvailable(port) {
  return new Promise((resolve) => {
    const server = createServer();
    server.once('error', () => resolve(false));
    server.once('listening', () => { server.close(); resolve(true); });
    server.listen(port);
  });
}

async function findAvailablePort(start) {
  let port = start;
  while (!(await isPortAvailable(port))) {
    port++;
  }
  return port;
}

const app = express();
app.use(cors());
app.use(express.json());

app.use('/api/roast', roastRouter);

// Serve React build in production
const distPath = path.join(__dirname, '../frontend/dist');
app.use(express.static(distPath));
app.get('/{*path}', (req, res) => {
  res.sendFile(path.join(distPath, 'index.html'));
});

const startPort = parseInt(process.env.PORT ?? '3001', 10);
const port = await findAvailablePort(startPort);

app.listen(port, () => {
  console.log(`Startup Roaster backend running on http://localhost:${port}`);
});
