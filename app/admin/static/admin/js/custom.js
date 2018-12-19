function getRequest() {
  req = new XMLHttpRequest()
  if (window.XMLHttpRequest) {
    req = new XMLHttpRequest()
  } else if (window.ActiveXObject) {
    req = new ActiveXObject("Microsoft.XMLHTTP")
  }
  return req
}

function loadDiv(target) {
  if (req.readyState == 4) {
    if (req.status == 200) {
      if (target == "redirect") {
        window.location.href = req.responseText
      } else if (target != "null") {
        document.getElementById(target).innerHTML = req.responseText
      }
    }
  }
}

function toggleSoundToBoard(sound_id) {
  var e = document.getElementById("sound_" + sound_id)
  if (e.classList.contains("is-danger")) {
    e.classList.remove("is-danger")
    e.classList.add("is-success")
  } else {
    e.classList.remove("is-success")
    e.classList.add("is-danger")
  }
}

function getSoundsToBoard() {
  var sound_list = []
  var x = document.getElementById("sounds_to_board")
  var y = x.getElementsByTagName("a")
  for (let item of y) {
    if (item.classList.contains("is-success")) {
      sound_list.push(item.getAttribute("data-id"))
    }
  }
  return sound_list
}

function submitBoard(board_id) {
  var name = document.getElementById("tb_name").value
  var sounds = getSoundsToBoard()

  var target = "redirect"
  var route = "/admin/board/submit"
  var sendData = JSON.stringify({
      board_id: board_id,
    name: name,
    sounds: sounds,
  })

  var req = getRequest()
  if (req != undefined) {
    req.onreadystatechange = function() {
      loadDiv(target)
    }
    req.open("POST", route, true)
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    req.send(sendData)
    return
  }
}

var file = document.getElementById("file")
file.onchange = function() {
  if (file.files.length > 0) {
    document.getElementById("filename").innerHTML = file.files[0].name
  }
}

function submitSound() {
  document.getElementById("bt_submit").className =
    "button is-pulled-right is-info is-loading"
  var name = document.getElementById("tb_name").value
  var description = document.getElementById("tb_description").value
  var soundfile = document.getElementById("soundfile")

  // if (!isStr(name)) {
  //     alert("error: name");
  //     return;
  // }
  // if (!isStr(description)) {
  //     alert("error: description");
  //     return;
  // }

  var formData = new FormData()
  formData.append("name", name)
  formData.append("description", description)
  formData.append("soundfile", soundfile.files[0])

  var route = "/admin/sound/submit"

  var target = "main_content"
  // KRÜCKE
  var request = new XMLHttpRequest()
  request.open("POST", route)
  request.ontimeout = function() {
    window.location.href = "/admin/sounds"
  }
  request.onload = function() {
    if (request.readyState === 4) {
      if (request.status === 200) {
        window.location.href = "/admin/sounds"
      }
    }
  }
  request.timeout = 10000
  request.send(formData)
}

// SORT TABLE - aus dem internet
function sortTable(tablename, col, button, desc) {
  desc = typeof desc !== "undefined" ? desc : false
  var func =
    "sortTable('" +
    tablename +
    "', " +
    col +
    ", '" +
    button +
    "', " +
    !desc +
    "); return false;"
  document.getElementById(button).setAttribute("onClick", func)
  var table, rows, switching, i, x, y, shouldSwitch
  table = document.getElementById(tablename)
  switching = true
  /*Make a loop that will continue until
	 no switching has been done:*/
  while (switching) {
    // start by saying: no switching is done:
    switching = false
    rows = table.getElementsByTagName("tr")
    /*Loop through all table rows (except the
		 first, which contains table headers):*/
    for (i = 1; i < rows.length - 1; i++) {
      // start by saying there should be no switching:
      shouldSwitch = false
      /*Get the two elements you want to compare,
			 one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("td")[col]
      y = rows[i + 1].getElementsByTagName("td")[col]
      if (desc) {
        // check if the two rows should switch place:
        if (
          x.innerHTML.replace(/(<([^>]+)>)/gi, "").toLowerCase() <
          y.innerHTML.replace(/(<([^>]+)>)/gi, "").toLowerCase()
        ) {
          // if so, mark as a switch and break the loop:
          shouldSwitch = true
          break
        }
      } else {
        // check if the two rows should switch place:
        if (
          x.innerHTML.replace(/(<([^>]+)>)/gi, "").toLowerCase() >
          y.innerHTML.replace(/(<([^>]+)>)/gi, "").toLowerCase()
        ) {
          // if so, mark as a switch and break the loop:
          shouldSwitch = true
          break
        }
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
			 and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i])
      switching = true
    }
  }
}

function toggleSoundEnabled(sound_id) {
  var target = "tgS_" + sound_id
  var route = "/admin/sounds/enabled"
  var sendData = JSON.stringify({
    sound_id: sound_id,
  })

  var req = getRequest()
  if (req != undefined) {
    req.onreadystatechange = function() {
      loadDiv(target)
    }
    req.open("POST", route, true)
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    req.send(sendData)
    return
  }
}

function deleteSound(sound_id) {
  if (userConfirmation("Sound löschen?")) {
  var target = "redirect"
  var route = "/admin/sound/delete/" + sound_id

  var req = getRequest()
  if (req != undefined) {
    req.onreadystatechange = function() {
      loadDiv(target)
    }
    req.open("GET", route, true)
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
    req.send()
    return
  }
}
}

function userConfirmation(text) {
  var r = confirm(text)
  return r
}

function deleteBoard(board_id) {
  if (userConfirmation("Board löschen?")) {
    var target = "redirect"
    var route = "/admin/board/delete/" + board_id

    var req = getRequest()
    if (req != undefined) {
      req.onreadystatechange = function() {
        loadDiv(target)
      }
      req.open("GET", route, true)
      req.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
      req.send()
      return
    }
  }
}
