// Setup editor
var editor = ace.edit('editor');
var textarea = document.getElementById('code-text-area');
editor.setTheme('ace/theme/monokai');
editor.session.setMode('ace/mode/python');
editor.resize();
editor.getSession().on("change", function () { textarea.value = editor.getSession().getValue() });

// Adding a new action
function addNewAction() {
	console.log("Adding action");
}

// Collapsing an action
function collapseAction(action_id) {
	var general = document.getElementById('action-' + action_id + '-general');
	var general_icon = document.getElementById('action-' + action_id + '-general-icon');
	var intent = document.getElementById('action-' + action_id + '-intent');
	var fulfillment = document.getElementById('action-' + action_id + '-fulfillment');

	intent.style.display = 'none';
	fulfillment.style.display = 'none';
	general.style.marginBottom = '-12px';
	general_icon.classList.remove('fa-chevron-up');
	general_icon.classList.add('fa-chevron-down');
}

// Expanding an action
function expandAction(action_id) {
	var general = document.getElementById('action-' + action_id + '-general');
	var general_icon = document.getElementById('action-' + action_id + '-general-icon');
	var intent = document.getElementById('action-' + action_id + '-intent');
	var fulfillment = document.getElementById('action-' + action_id + '-fulfillment');

	intent.style.display = 'block';
	fulfillment.style.display = 'block';
	general.style.marginBottom = '12px';
	general_icon.classList.remove('fa-chevron-down');
	general_icon.classList.add('fa-chevron-up');
}

// Onclick routine for expanding or collapsing an action
function expandCollapseOnClick(action_id) {
	if (document.getElementById('action-' + action_id + '-intent').style.display == 'none') {
		expandAction(action_id);
	} else {
		collapseAction(action_id);
	}
}

// Adding tags to patterns
function addTag(action_id, pattern_id, type, input_name) {
	var field = document.getElementById('action-' + action_id + '-pattern-' + pattern_id);
	if (type == 'optional') {
		field.innerHTML += "<span class='tag is-dark' style='margin-left:3px;margin-right:3px;' contentEditable='false'>Optional:" + document.getElementById(input_name).value + "</span>&nbsp";
	} else {
		var inputElement = document.getElementById(input_name);
		field.innerHTML += "<span class='tag is-info' style='margin-left:3px;margin-right:3px;' contentEditable='false'>" + inputElement.options[inputElement.selectedIndex].value + "</span>&nbsp";
	}
}

// validation
// Validating manifest
function validateManifest(display_errors) {
	var display_name = document.getElementById('field-display-name');
	var invocation_name = document.getElementById('field-invocation-name');
	var icon = document.getElementById('manifest-completed_icon');
	var icon_span = document.getElementById('manifest-completed_icon-span');
	var tasks_icon = document.getElementById('tasks-manifest-icon');

	if (display_name.value != '' && invocation_name.value) {
		icon_span.classList.add('has-text-success');
		icon_span.classList.remove('has-text-danger');
		icon.classList.add('fa-check-circle');
		icon.classList.remove('fa-times-circle');
		tasks_icon.classList.add('has-text-success');
		tasks_icon.classList.remove('has-text-danger');
		tasks_icon.classList.add('fa-check-circle');
		tasks_icon.classList.remove('fa-times-circle');
		display_name.classList.remove('is-danger');
		invocation_name.classList.remove('is-danger');
		validateTasks();
		return true;
	} else {
		if (display_name.value == '' && display_errors) {display_name.classList.add('is-danger');} else {display_name.classList.remove('is-danger');}
		if (invocation_name.value == '' && display_errors) {invocation_name.classList.add('is-danger');} else {invocation_name.classList.remove('is-danger');}
		icon_span.classList.add('has-text-danger');
		icon_span.classList.remove('has-text-success');
		icon.classList.add('fa-times-circle');
		icon.classList.remove('fa-check-circle');
		tasks_icon.classList.add('has-text-danger');
		tasks_icon.classList.remove('has-text-success');
		tasks_icon.classList.add('fa-times-circle');
		tasks_icon.classList.remove('fa-check-circle');
		validateTasks();
		return false;
	}
}

function validateTasks() {
	var tasks_icon = document.getElementById('tasks-icon');
	var manifest_icon = document.getElementById('tasks-manifest-icon');

	if (manifest_icon.classList.contains('has-text-success')) {
		tasks_icon.classList.add('has-text-success');
		tasks_icon.classList.remove('has-text-danger');
		tasks_icon.classList.add('fa-check-circle');
		tasks_icon.classList.remove('fa-times-circle');
	} else {
		tasks_icon.classList.add('has-text-danger');
		tasks_icon.classList.remove('has-text-success');
		tasks_icon.classList.add('fa-times-circle');
		tasks_icon.classList.remove('fa-check-circle');
	}
}

// Run all validation routines to start with
validateManifest(false);
