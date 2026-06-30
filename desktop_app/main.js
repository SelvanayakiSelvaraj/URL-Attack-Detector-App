const { app, BrowserWindow, dialog } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');
const fs = require('fs');
const os = require('os');

let mainWindow;
let javaProcess;
let pythonProcess;
let logStream;

function log(msg) {
    const timestamp = new Date().toISOString();
    const message = `[${timestamp}] ${msg}\n`;
    console.log(message);
    if (logStream) logStream.write(message);
}

log("=========================================");
log("Starting URL Attack Detector Application");

// We assume the final distribution structure will look like:
// /win-unpacked/
// │
// ├── URL Attack Detector.exe
// ├── resources/
// │   └── app/
// │       ├── main.js
// │       ├── package.json
// │       ├── backend/
// │       │   └── url-attack-detector-0.0.1-SNAPSHOT.jar
// │       └── ml_service/
// │           ├── app.py
// │           └── model/
//
// Alternatively, if running in dev via `npm start`:
// /desktop_app/
// ├── main.js
// ├── package.json
// └── (points up one level to original folders)

const isDev = !app.isPackaged;
const basePath = isDev ? path.join(__dirname, '..') : process.resourcesPath;

function createSplashWindow() {
    const debugLogPath = path.join(app.getPath('desktop'), 'app_debug_log.txt');
    logStream = fs.createWriteStream(debugLogPath, { flags: 'a' });
    log("=========================================");
    log("APPLICATION STARTING...");
    log("=========================================");
    log("Starting URL Attack Detector Application");

    const splash = new BrowserWindow({
        width: 400,
        height: 300,
        frame: false,
        alwaysOnTop: true,
        transparent: false,
        backgroundColor: '#1e293b',
        webPreferences: { nodeIntegration: true }
    });

    splash.loadURL('data:text/html;charset=utf-8,' + encodeURI(`
        <html>
        <body style="font-family: sans-serif; background-color: #1e293b; color: white; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; margin: 0;">
            <h1 style="color: #4facfe; margin-bottom: 5px;">URL Attack Detector</h1>
            <p>Starting Security Engines...</p>
            <div style="margin-top: 20px; width: 40px; height: 40px; border: 4px solid rgba(255,255,255,0.1); border-top-color: #4facfe; border-radius: 50%; animation: spin 1s linear infinite;"></div>
            <style>@keyframes spin { 100% { transform: rotate(360deg); } }</style>
        </body>
        </html>
    `));
    return splash;
}

let javaError = "";
let pythonError = "";

function startBackendServices() {
    console.log("Starting Python ML Service...");
    const mlPath = isDev ? path.join(basePath, 'ml_service') : path.join(basePath, 'ml_service');

    // NEVER use the packaged venv directly, as python will crash if the directory moved.
    // Instead, dynamically build and install the venv on-the-fly via a batch script using an explicit cmd path!
    const cmdPath = process.env.comspec || 'C:\\Windows\\System32\\cmd.exe';

    try {
        pythonProcess = spawn(cmdPath, ['/c', 'start_ml.bat'], {
            cwd: mlPath,
            detached: false,
            windowsHide: true
        });

        pythonProcess.stdout.on('data', data => log(`[PYTHON] ${data.toString()}`));
        pythonProcess.stderr.on('data', data => {
            log(`[PYTHON ERR] ${data.toString()}`);
            pythonError += data.toString();
        });
        pythonProcess.on('error', err => {
            log(`[PYTHON SPAWN ERR] ${err.message}`);
            pythonError += err.message + "\n";
        });
    } catch (e) {
        pythonError += e.message + "\n";
    }

    console.log("Starting Java Spring Boot Service...");
    const jarPath = isDev
        ? path.join(basePath, 'target', 'url-attack-detector-0.0.1-SNAPSHOT.jar')
        : path.join(basePath, 'backend', 'url-attack-detector-0.0.1-SNAPSHOT.jar');

    try {
        javaProcess = spawn(cmdPath, ['/c', 'java', '-jar', jarPath], {
            detached: false,
            windowsHide: true
        });

        javaProcess.stdout.on('data', data => log(`[JAVA] ${data.toString()}`));
        javaProcess.stderr.on('data', data => log(`[JAVA ERR] ${data.toString()}`));
        javaProcess.on('error', err => {
            log(`[JAVA SPAWN ERR] ${err.message}`);
            javaError += err.message + "\n";
        });
    } catch (e) {
        javaError += e.message + "\n";
    }
}

function waitForServer(url, timeoutMs, intervalMs, callback) {
    const start = Date.now();

    const check = () => {
        if (Date.now() - start > timeoutMs) {
            return callback(new Error("Timeout waiting for server"));
        }

        http.get(url, (res) => {
            if (res.statusCode === 200 || res.statusCode === 404 || res.statusCode === 405) {
                callback(null);
            } else {
                setTimeout(check, intervalMs);
            }
        }).on('error', () => {
            setTimeout(check, intervalMs);
        });
    };
    check();
}

app.whenReady().then(() => {
    const splash = createSplashWindow();

    startBackendServices();

    // Wait until Spring Boot UI is completely up (usually takes ~5-15s)
    waitForServer('http://localhost:8080/', 45000, 1000, (err) => {
        if (err) {
            dialog.showErrorBox("Startup Failed", "Could not start the backend security engines.\n\nPython Error: " + pythonError + "\n\nJava Error: " + javaError);
            app.quit();
            return;
        }

        // Create main app window
        mainWindow = new BrowserWindow({
            width: 1000,
            height: 700,
            title: "URL Attack Detector",
            autoHideMenuBar: true,
            webPreferences: {
                nodeIntegration: false
            }
        });

        mainWindow.webContents.session.clearCache().then(() => {
            mainWindow.loadURL('http://localhost:8080/');
        });

        mainWindow.once('ready-to-show', () => {
            splash.close();
            mainWindow.show();
        });

        mainWindow.on('closed', () => {
            mainWindow = null;
        });
    });
});

app.on('will-quit', () => {
    // Kill child processes cleanly on exit so ports 8080 and 5000 are freed
    if (javaProcess) {
        // Windows needs taskkill to forcefully kill the java tree if spawned via shell
        spawn('taskkill', ['/pid', javaProcess.pid, '/f', '/t']);
    }
    if (pythonProcess) {
        spawn('taskkill', ['/pid', pythonProcess.pid, '/f', '/t']);
    }
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
