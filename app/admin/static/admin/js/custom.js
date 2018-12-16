var subdir_custom = "";


// POPUP
function hideElements(elems) {
	for (var i in elems) {
		e = elems[i];
		if (document.getElementById(e) != null) {
			document.getElementById(e).style.display = 'none';
		}
	}
}
function showElements(elems) {
	for (var i in elems) {
		e = elems[i];
		if (document.getElementById(e) != null) {
			document.getElementById(e).style.display = 'block';
		}
	}
}

// SCROLLTO
function scroll(scrollTo) {
	if (scrollTo != "") {
		document.getElementById(scrollTo).scrollIntoView();
		document.cookie = "scroll-to=; path=/;";
	}
}

function setLanguage(lang) {
	var target = "redirect";
	var route = subdir_custom + "/language/" + lang;
	var txt = window.location.pathname;
	var sendData = JSON.stringify({
		page: txt
	});
	ajaxCall(sendData, target, route);
}

// REGISTER USER
function checkEmail(register) {
	var email = document.getElementById("email").value;
	// Prüfe ob korrekte email Adresse
	var pattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
	var expr = new RegExp(pattern);
	var res = expr.test(email);
	if (!res) {
		document.getElementById("help_email").innerHTML = "keine gültige Email Adresse";
		document.getElementById("icon_email_check").innerHTML = "<i class='fas fa-exclamation-triangle'></i>";
		return;
	} else {
		document.getElementById("help_email").innerHTML = "";
		document.getElementById("icon_email_check").innerHTML = "<i class='fas fa-check'></i>";
	}
	if (!register) {
		return;
	}
	// Prüfe ob email Adresse verfügbar
	var xhr = new XMLHttpRequest();
	xhr.open("GET", "/username_is_available/" + email, true);
	xhr.onload = function(e) {
		if (xhr.readyState === 4) {
			if (xhr.status === 200) {
				if (xhr.responseText == "1") {
					document.getElementById("help_email").innerHTML = "";
					document.getElementById("icon_email_check").innerHTML = "<i class='fas fa-check'></i>";
				} else {
					document.getElementById("help_email").innerHTML = "Email Adresse bereits registriert";
					document.getElementById("icon_email_check").innerHTML = "<i class='fas fa-exclamation-triangle'></i>";
				}
			}
		}
	};
	xhr.send(null);
}
function checkPassword(field = 'password') {
	var len = document.getElementById(field).value.length;
	if (len > 5) {
		document.getElementById("help_" + field).innerHTML = "";
		document.getElementById("icon_" + field + "_check").innerHTML = "<i class='fas fa-check'></i>";
	} else {
		document.getElementById("help_" + field).innerHTML = "Passwort zu kurz";
		document.getElementById("icon_" + field + "_check").innerHTML = "<i class='fas fa-exclamation-triangle'></i>";
	}
}
function checkPasswordConfirm(field = 'password') {
	var pass = document.getElementById(field).value;
	var pass_confirm = document.getElementById("password_confirm").value;
	if (pass === pass_confirm) {
		document.getElementById("help_" + field).innerHTML = "";
	} else {
		document.getElementById("help_confirm_" + field).innerHTML = "Passwörter stimmen nicht überein";
		document.getElementById("icon_confirm_" + field + "_check").innerHTML = "<i class='fas fa-exclamation-triangle'></i>";
	}
}




// MODUL AJAX
function getRequest() {
	req = new XMLHttpRequest();
	if (window.XMLHttpRequest) {
		req = new XMLHttpRequest();
	} else if (window.ActiveXObject) {
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	return req;
}
// AJAX-JSON CALL
function ajaxCallJSON(route, sendData = null) {
	var req = getRequest();
	if (req != undefined) {
		req.onreadystatechange = function() {handleResponseJSON(10000);};
		// req.onreadystatechange = function() {func;};
		if (!sendData) {
			req.open("GET", route, true);
		} else {
			req.open("POST", route, true);
		}
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		req.send(sendData);
	}
}
function handleResponseJSON(timer = null, func) {
	if (req.readyState === 4) {
		if (req.status === 200) {
			var myjson = JSON.parse(req.responseText);
			window[func](myjson);
		}
		if (timer){
			setTimeout(timerFunc, timer, "args");
		}
	}
}
// AJAX CALL
function ajaxCall(sendData, target, route, success_func = null) {
	var req = getRequest();
	if (req != undefined) {
		req.onreadystatechange = function() {
			handleResponse(target, success_func);
		};
		if (!sendData) {
			req.open("GET", route, true);
		} else {
			req.open("POST", route, true);
		}
		if (typeof(sendData) === "string") {
			req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		} else {
			req.setRequestHeader('Content-Type', 'multipart/form-data');
		}
		req.send(sendData);
		return;
	}
}
function handleResponse(target, func = null) {
	if (req.readyState === 4) {
		var ret;
		if (req.status === 200) {
			if (target === "redirect") {
				window.location.href = req.responseText;
			} else {
				document.getElementById(target).innerHTML = req.responseText;
				if (func != null) {
					ret = eval(func);
				} // ist das ok so?, Nein eval is bad, mit window machen
			}
		} else {
			document.getElementById(target).innerHTML = req.responseText;
			if (func != null) {
				ret = eval(func);
			} // ist das ok so?
		}
	}
}



// ADMIN
function addUser() {
	var name = document.getElementById("admin_add_user_name").value;
	var email = document.getElementById("admin_add_user_email").value;
	// Eingaben prüfen: name
	if (!isStr(name)) {
		alert("error: name");
		return;
	}
	if (!isEmail(email)) {
		alert("error: email");
		return;
	}
	var sendData = JSON.stringify({
		name: name,
		email: email
	});
	var route = subdir_custom + "/admin/users/adduser/";
	var target = "main_content";
	document.getElementById("btAddUser").className = "button is-pulled-right is-info is-loading";
	ajaxCall(sendData, target, route);
}

function addRole() {
	var name = document.getElementById("admin_add_role_name").value;
	var description = document.getElementById("admin_add_role_description").value;
	// Eingaben prüfen: name
	if (!isStr(name)) {
		alert("error: name");
		return;
	}
	if (!isStr(description)) {
		alert("error: name");
		return;
	}
	var sendData = JSON.stringify({
		name: name,
		description: description
	});
	var route = subdir_custom + "/admin/users/addrole/";
	var target = "main_content";
	document.getElementById("btAddRole").className = "button is-pulled-right is-info is-loading";
	ajaxCall(sendData, target, route);
}

function editUserInRole(set, user, role) {
	function changeClass(target, set, user, role) {
		if (req.readyState === 4) {
			if (req.status === 200) {
				var link = "editUserInRole('" + set + "','" + user + "','" + role + "',); return false;";
				document.getElementById(target).className = req.responseText;
				document.getElementById(target).setAttribute('onclick', link);
			} else {
				alert("error: editUserInRole()");
			}
		}
	}
	var target = "u2r_" + role + "_" + user;
	document.getElementById(target).className += " is-loading ";
	var route = subdir_custom + "/admin/users/user2role";
	var sendData = JSON.stringify({
		val: set,
		user: user,
		role: role
	});
	if (set === 1) {
		set = 0;
	} else {
		set = 1;
	}
	req = new XMLHttpRequest();
	if (window.XMLHttpRequest) {
		req = new XMLHttpRequest();
	} else if (window.ActiveXObject) {
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	if (req != undefined) {
		req.onreadystatechange = function() {
			changeClass(target, set, user, role);
		};
		req.open("POST", route, true);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		req.send(sendData);
	}
}

function deleteUser(id, name) {
	if (!confirm("Soll der Benutzer " + name + " wirklich gelöscht werden?")) {
		return;
	}
	var route = subdir_custom + "/admin/users/remove_user/" + id;
	document.cookie = "scroll-to=scroll2user; path=/;";
	window.location.href = route;
}

function deleteRole(id, name) {
	if (!confirm("Soll die Rolle " + name + " wirklich gelöscht werden?")) {
		return;
	}
	var route = subdir_custom + "/admin/users/remove_role/" + name;
	document.cookie = "scroll-to=scroll2role; path=/;";
	window.location.href = route;
}

function toggleActive(userid) {
	function changeLink(target) {
		if (req.readyState === 4) {
			if (req.status === 200) {
				document.getElementById(target).innerHTML = req.responseText;
			} else {
				alert("error: editUserInRole()");
			}
		}
	}
	var target = "tgU_" + userid;
	var route = subdir_custom + "/admin/users/deactivate/" + userid;
	req = new XMLHttpRequest();
	if (window.XMLHttpRequest) {
		req = new XMLHttpRequest();
	} else if (window.ActiveXObject) {
		req = new ActiveXObject("Microsoft.XMLHTTP");
	}
	if (req != undefined) {
		req.onreadystatechange = function() {
			changeLink(target);
		};
		req.open("GET", route, true);
		req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
		req.send();
	}
}

function removeRole(role, rolename) {
	if (!confirm("Soll die Rolle " + rolename + " wirklich gelöscht werden?")) {
		return;
	}
	var route = "{{config.SUBDIR}}/admin/remove_role/" + role;
	document.cookie = "scroll-to=scroll2role; path=/;";
	window.location.href = route;
}

// SORT TABLE - aus dem internet
function sortTable(tablename, col, button, desc) {
	desc = (typeof desc !== 'undefined') ? desc : false;
	var func = "sortTable('" + tablename + "', " + col + ", '" + button + "', " + !desc + "); return false;";
	document.getElementById(button).setAttribute("onClick", func);
	var table, rows, switching, i, x, y, shouldSwitch;
	table = document.getElementById(tablename);
	switching = true;
	/*Make a loop that will continue until
	 no switching has been done:*/
	while (switching) {
		// start by saying: no switching is done:
		switching = false;
		rows = table.getElementsByTagName("tr");
		/*Loop through all table rows (except the
		 first, which contains table headers):*/
		for (i = 1; i < (rows.length - 1); i++) {
			// start by saying there should be no switching:
			shouldSwitch = false;
			/*Get the two elements you want to compare,
			 one from current row and one from the next:*/
			x = rows[i].getElementsByTagName("td")[col];
			y = rows[i + 1].getElementsByTagName("td")[col];
			if (desc) {
				// check if the two rows should switch place:
				if (x.innerHTML.replace(/(<([^>]+)>)/ig, "").toLowerCase() < y.innerHTML.replace(/(<([^>]+)>)/ig, "").toLowerCase()) {
					// if so, mark as a switch and break the loop:
					shouldSwitch = true;
					break;
				}
			} else {
				// check if the two rows should switch place:
				if (x.innerHTML.replace(/(<([^>]+)>)/ig, "").toLowerCase() > y.innerHTML.replace(/(<([^>]+)>)/ig, "").toLowerCase()) {
					// if so, mark as a switch and break the loop:
					shouldSwitch = true;
					break;
				}
			}
		}
		if (shouldSwitch) {
			/*If a switch has been marked, make the switch
			 and mark that a switch has been done:*/
			rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
			switching = true;
		}
	}
}

function isFloat(str) {
	return true;
}

function isInt(str) {
	return true;
}

function isStr(str) {
	return true;
}

function isEmail(email) {
	return true;
}
