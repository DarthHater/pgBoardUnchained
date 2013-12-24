var settings = require('./local');
var bbcode = require('./bbcode');
var jsoncereal = require('json-serialize');
var http = require('http');
var server = http.createServer().listen(settings.node.port);
var io = require('socket.io').listen(server);
var cookie_reader = require('cookie');
var querystring = require('querystring');

 
var redis = require('socket.io/node_modules/redis');
var sub = redis.createClient(settings.redis.port, settings.redis.host);
sub.auth(settings.redis.password);

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
    sub.on('message', function(channel, message){
        var encodeMe = jsoncereal.deserialize(message);
        encodeMe.comment = bbcode.render(encodeMe.comment);
        socket.send(JSON.stringify(encodeMe));
    });
    
    //Client is sending message through socket.io
    socket.on('send_message', function (message, thread) {
        values = querystring.stringify({
            comment: message,
            sessionid: socket.handshake.sessionID,
            thread: thread,
        });
        
        var options = {
            host: settings.django.host,
            port: settings.django.port,
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