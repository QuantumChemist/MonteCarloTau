import { app, BrowserWindow } from 'electron';
import * as path from 'path';

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true
    }
  });
  // Load renderer from src during development. In production you may copy files to dist/renderer.
  const devIndex = path.join(__dirname, '..', 'src', 'renderer', 'index.html');
  const prodIndex = path.join(__dirname, '..', 'renderer', 'index.html');
  const indexToLoad = require('fs').existsSync(devIndex) ? devIndex : prodIndex;
  win.loadFile(indexToLoad);
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
