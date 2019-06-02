var code;
var callables;
var id;

// Setup editor
function setupEditor() {
	var editor = ace.edit('editor');
	editor.setTheme('ace/theme/textmate');
	editor.session.setMode('ace/mode/python');
	editor.resize();
	editor.getSession().on("change", function () { code = editor.getSession().getValue() });
	editor.getSession().setUseSoftTabs(false);
	editor.setValue("def test():\n\treturn('hello world')");
}

// Upload code
function upload(id) {
	this.id = id;
	const Http = new XMLHttpRequest();
 	Http.open("POST", '/remote-processor/upload/' + id);
 	Http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
 	Http.send("code=" + encodeURIComponent(code));
 	Http.onreadystatechange=function(){
		if (this.readyState == 4) {
			callables = JSON.parse(this.responseText);
			loadTests();
		}
	}
}

function loadTests() {
	testsContainer = document.getElementById("tests-container");
	var result = "<div class='columns'>";
	for (var callable in callables){
	  result += "<div class='column'><div class='box'>";
	  result += "<h1 class='title is-4'>" + callable + "</h1>";
	  for (i=0; i<callables[callable].length; i++) {
		  result += "<div class='columns'><div class='column is-4'> " + callables[callable][i] + " </div><div class='column is-8'> <input id='" + callable + "-" + callables[callable][i] + "' class='input' type='text' placeholder='Type an expression...'> </div></div>";
	  }
	  result += "<a class='button' style='width:100%;' onclick='test(" + id + ",\"" + callable + "\")'>Test</a>"
	  result += "</div></div>";
	}
	result += "</div>";
	testsContainer.innerHTML = result;
}

function test(id, myFunction) {
	var data = {};
	for (i=0; i<callables[myFunction].length; i++) {
		data[callables[myFunction][i]] = document.getElementById(myFunction + "-" + callables[myFunction][i]).value;
	}
	console.log(data);
	const Http = new XMLHttpRequest();
 	Http.open("POST", '/remote-processor/test/' + id + '/' + myFunction);
 	Http.setRequestHeader("Content-Type", "application/json");
 	Http.send(JSON.stringify(data));
 	Http.onreadystatechange=function(){
		if (this.readyState == 4) {
			console.log(this.responseText);
		}
	}
}
