import { app, BrowserWindow, session } from 'electron';
import { existsSync } from 'node:fs';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

app.commandLine.appendSwitch('autoplay-policy', 'no-user-gesture-required');

function createWindow() {
  const win = new BrowserWindow({
    width: 1280,
    height: 820,
    minWidth: 980,
    minHeight: 640,
    backgroundColor: '#050B12',
    title: 'JARVIS',
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true
    }
  });

  const devUrl = process.env.JARVIS_DESKTOP_DEV_URL ?? 'http://127.0.0.1:5173';
  const distIndex = join(__dirname, '..', 'dist', 'index.html');

  if (process.env.JARVIS_DESKTOP_MODE === 'dev' || !existsSync(distIndex)) {
    void win.loadURL(devUrl);
  } else {
    void win.loadFile(distIndex);
  }
}

app.whenReady().then(() => {
  session.defaultSession.setPermissionRequestHandler((_webContents, permission, callback) => {
    callback(permission === 'media' || permission === 'microphone');
  });

  createWindow();
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
