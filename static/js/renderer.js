const zerorpc = require('zerorpc')

/******************************************
 * Communication with the Python backend. *
 ******************************************/

let client = new zerorpc.Client()
client.connect("tcp://127.0.0.1:4242")

/**
 * Check if the server has started.
 */
client.invoke("echo", "Server ready.", (error, res) => {
    if(error || res !== "Server ready.") {
        console.error(error)
    } else {
        console.log("Server is ready.")
    }
})

