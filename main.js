const electron = require('electron')
const path = require('path')
const fs = require('fs')
const child_process = require('child_process')

const app = electron.app
const BrowserWindow = electron.BrowserWindow

/********************
 * Window Creation. *
 ********************/

let mainWindow = null   // Global variable to contain the main window.

/**
 * Creates the main window.
 */
const createWindow = () => {
    mainWindow = new BrowserWindow({width: 800, height: 600})
    mainWindow.loadURL(require('url').format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: "file:",
        slashes: true
    }))
    mainWindow.maximize()
    // mainWindow.webContents.openDevTools()
    mainWindow.on('closed', () => {
        mainWindow = null
    })
}

/****************************
 * Python process spawning. *
 ****************************/

// Constant variables for the Python source.
const PY_DIST_FOLDER = 'pylifedist' // Folder that contains the compiled python files.
const PY_FOLDER = 'pylife'  // Folder that contains the source python files.
const PY_MODULE = 'api' // Name of the "main" python file.

let pyProc = null // Global variable to contain the Python process.
const pyPort = 4242 // Port that the Python process will use.

/**
 * Checks if the Python files have been packaged or not.
 * @returns {Boolean} If the Python files have been packaged or not.
 */
const checkIfPackaged = () => {
    const fullPath = path.join(__dirname, PY_DIST_FOLDER)
    return fs.existsSync(fullPath)
}

/**
 * Returns the file path to the main Python file.
 * @returns {String} The file path to the main Python file.
 */
const getScriptPath = () => {
    if(!checkIfPackaged()) {
        return path.join(__dirname, PY_FOLDER, PY_MODULE + '.py')
    }
    if(process.platform === 'win32') {
        return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE + '.exe')
    }
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE)
}

/**
 * Spawns the Python child process that will handle the backend.
 */
const createPyProc = () => {
    let script = getScriptPath()

    if(checkIfPackaged()) {
        pyProc = child_process.execFile(script, [pyPort])
    } else {
        pyProc = child_process.spawn('python', [script, pyPort])
    }

    if(pyProc !== null) {
        console.log("Child process successfully spawned on port " + pyPort)
    }
}

/**
 * Kills the Python child process.
 */
const exitPyProc = () => {
    pyProc.kill()
    pyProc = null
}

/*******************
 * Event Handlers. *
 *******************/
app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (mainWindow === null) {
        createWindow()
    }
})

app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)