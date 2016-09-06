var http = require('http');
var connect = require('connect'); // package <connect> need to be installed



// 404 response
function send404Response(response){
	response.writeHead(404, {"Context-Type: "text/plain"});
	response.write("Error 404: page not found!");
	response.end();
}

// Handle a user request
function onRequest(request, response){
	if (request.method == 'GET' && request.url == '/'){
		response.writeHead(200, {"Context-Type: "text/html"});
		fs.createReadStrem("./index.html").pipe(response);
	}else{
		send404Response(response);
	}
	

}

http.createServer(onRequest).listen(8080);
console.log("Server is now running ...")

/*
var LED = {
	state =  // 1--> LED on, 0--> Led off 
	brightness =  //brightness of led, 0 if it is turned off
	time = // how long the led in this state
	SwitchTime =  // how much time left to switch led state
} 

function Offled(){
	;
}

function Adjust(){
	;
}
*/
