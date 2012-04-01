
var socket = new io.Socket();

$(document).ready(function() {
	
	$('.cell').bind('input',onInput);
	$('.cell').keydown(onKeydown);
   //$('.cell').blur(onChange);
   
   socket.connect();
   socket.on('connect', function() {
   	//alert('Connected');
   	socket.subscribe('xword');
   });
   
   var handlers = {"change":handleChange}

   socket.on('message', function(data) {
	   //$.print("incoming");
	   //$.print(data);
   		var message = JSON.parse(data);
   		handlers[message.type].call(this,message);
   });
});

function Change(x,y,value) {
	this.type = "change";
	this.x = x;
	this.y = y;
	this.val = value
}

function handleChange(change) {
	getCell(change.x,change.y).value = change.val;
}

function getX(input) {
	return $(input).parent()[0].cellIndex;
}

function getY(input) {
	return $(input).parent().parent()[0].sectionRowIndex;
}

function getCell(x,y)
{
	return $("#crossword tr").eq(y).find('td').eq(x).find('input')[0];
}

function nextCell(input) {
	return nextCellAcross(input);
}

function prevCellAcross(input) {
	var td = $(input).parent("td");
	
	do
	{
		var td = $(td).prev("td");
		//detects the end of a row and moves down a row 
		if(td.length == 0)
		{
			td = $(input).parent("td").parent("tr").prev("tr").children("td").last();
		}	
	}
	while(td.hasClass("blackcell"));
	
	return td.children("input").first();	
}

function nextCellAcross(input) {
	var td = $(input).parent("td");
	
	do
	{
		var td = $(td).next("td");
		//detects the end of a row and moves down a row 
		if(td.length == 0)
		{
			td = $(input).parent("td").parent("tr").next("tr").children("td").first();
		}	
	}
	while(td.hasClass("blackcell"));
	
	return td.children("input").first();
}

function updateInput(cell)
{
	cell.value = cell.value.toUpperCase();
	var oldVal = $(cell).data('oldVal');
	cell.value = cell.value.replace(oldVal,'');
	
	cell.value = cell.value[0]
	
	var didChange = cell.value == oldVal;
	
	$(cell).data('oldVal',cell.value);
	
	return didChange;
}

function onInput(event) {
	var didChange = updateInput(this);
	
	if(didChange)
	{
		var change = new Change	(getX(this),getY(this),this.value);
		socket.send(JSON.stringify(change));
	}

	var next  = nextCell(this);
	
	//chrome refocuses on the input if we call it before returning
	setTimeout(function() { next.focus() }, 0);
}


function onKeydown(event) {
	switch(event.keyCode)
	{
	case 37:prevCellAcross(this).focus();break;
	case 38: /* up */ break;
	case 39:nextCellAcross(this).focus();break;
	case 40: /*down*/ break;
	}
}
