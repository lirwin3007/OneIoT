var code;

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
	const Http = new XMLHttpRequest();
 	Http.open("POST", '/remote-processor/upload/' + id);
 	Http.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
 	Http.send("code=" + encodeURIComponent(code));
 	Http.onreadystatechange=function(){
		if (this.readyState == 4) {
			if (this.responseText == "true"){
				state.step = 2;
			} else {
				alert("Failed. Please try again")
			}
		}
	}
}
