var vertx = require('vertx');

vertx.createHttpServer().requestHandler(function(req) {
  req.response.sendFile('index.html');
}).listen(8080)
