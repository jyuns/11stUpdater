let winston = require('winston')
require('winston-daily-rotate-file')

var transport = new (winston.transports.DailyRotateFile)({
    filename: './application.log',
    maxsize: 1024,
  });
  
  var logger = winston.createLogger({
    transports: [
      transport
    ]
  });
  
  
  module.exports = logger