const {app, BrowserWindow} = require('electron')
const path = require('path')

/********************
 * Window Creation. *
 ********************/
let mainWindow = null

const createWindow = () => {
    "use strict"
    mainWindow = new BrowserWindow({width: 800, height: 600})
    mainWindow.loadURL(require('url').format({
        pathname: path.join(__dirname, 'index.html'),
        protocol: "file:",
        slashes: true
    }))
}