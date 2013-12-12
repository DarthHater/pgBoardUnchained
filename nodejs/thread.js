var http = require('http');
var server = http.createServer().listen(8001);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');
 
var redis = require('socket.io/node_modules/redis');
var sub = redis.createClient(6379, "127.0.0.1");
sub.auth("wut@ngr00lz");
 
//Subscribe to the Redis chat channel
sub.subscribe('thread');

io.configure(function() {
    io.set('authorization', function(data, accept) {
        if(data.headers.cookie) {
            data.cookie = cookie_reader.parse(data.headers.cookie); 
            data.sessionID = data.cookie['sessionid'];
            return accept(null, true);
        }
        return accept('Say it again cookie beyotch!', false);
    });
});

io.sockets.on('connection', function (socket) {

    //Grab message from Redis and send to client
    //sub.on('thread', function(channel, message){
    //    socket.send(message);
    //});
    
    //Client is sending message through socket.io
    socket.on('send_message', function (message) {
        values = querystring.stringify({
            comment: message,
            sessionid: socket.handshake.sessionID,
        });
        
        var options = {
            host: '127.0.0.1',
            port: 8000,
            path: '/thread_api',
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Content-Length': values.length
            }
        };
        
        //Send message to Django server
        var req = http.get(options, function(res){
            res.setEncoding('utf8');
            
            //Print out error message
            res.on('data', function(message){
                if(message != 'Everything worked :)'){
                    console.log('Message: ' + message);
                }
            });
        });
        
        req.write(values);
        req.end();
    });
});