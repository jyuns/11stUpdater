let {PythonShell} =  require('python-shell');
 
const express = require('express')
const nodeApp = express()

const cors = require('cors')
const bodyParser = require('body-parser')

nodeApp.use(cors())
nodeApp.use(bodyParser.json({limit:'100mb'}))
nodeApp.use(bodyParser.urlencoded({limit:'100mb', extended:true}))

// 속도 측정하기
const getDurationInMilliseconds = (start) => {
    const NS_PER_SEC = 1e9
    const NS_TO_MS = 1e6
    const diff = process.hrtime(start)
  
    return (diff[0] * NS_PER_SEC + diff[1]) / NS_TO_MS
  }

nodeApp.use((req, res, next) => {
    console.log(`${req.method} ${req.originalUrl} [STARTED]`)
    const start = process.hrtime()
  
    res.on('finish', () => {            
        const durationInMilliseconds = getDurationInMilliseconds (start)
        console.log(`${req.method} ${req.originalUrl} [FINISHED] ${durationInMilliseconds .toLocaleString()} ms`)
    })
  
    res.on('close', () => {
        const durationInMilliseconds = getDurationInMilliseconds (start)
        console.log(`${req.method} ${req.originalUrl} [CLOSED] ${durationInMilliseconds .toLocaleString()} ms`)
    })
  
    next()
  })

nodeApp.post('/11st/login', async (req, res) => {
    let userID = req.body.userID
    let userPW = req.body.userPW

    let options = {
        mode: 'text',
        pythonPath:'/usr/bin/python',
        pythonOptions: ['-u'],
        args:[userID, userPW]
      };
    
    let shell = new PythonShell(__dirname + '/login.py', options)

    try {
        shell.on('message', function(message) {
            console.log(message)
            res.send(message)
        })
    } catch (err) {
        res.send(err)
    }
})

nodeApp.post('/11st/upload', async (req, res) => {

    let path = req.body.path
    let type = req.body.type
    let cookies = req.body.cookies

    let options = {
        mode: 'text',
        pythonPath:'/usr/bin/python',
        pythonOptions: ['-u'],
        args:[cookies, path, type]
    };
    
    let shell = new PythonShell(__dirname + '/upload.py', options)

    try {
        shell.on('message', function(message) {
            res.send(message)
        })
    } catch (err) {
        res.send(err)
    }

    res.end('success')
})

nodeApp.listen(8082, () => {
    console.log('node listen 8082 port')
})