
var socket = new io.Socket();

$(document).ready(function() {
	
	$('.cell').bind('input',onInput);
   //$('.cell').keypress(onCellKeypress);
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
	cell.value = cell.value.replace($(cell).data('oldVal'),'');
	cell.value = cell.value[0].toUpperCase();
	
	$(cell).data('oldVal',cell.value);
}

function onInput(event) {
	updateInput(this);
	
	var next  = nextCell(this);
	
	//chrome refocuses on the input if we call it before returning
	setTimeout(function() { next.focus() }, 0);
}

function onChange(event) {
	this.value=this.value.toUpperCase();
	
	var cell = $(this).parent();
	var row =  $(this).parent().parent();
	var change = new Change	(getX(this),getY(this),this.value);
	socket.send(JSON.stringify(change));
	$.print(JSON.stringify(change));
}

