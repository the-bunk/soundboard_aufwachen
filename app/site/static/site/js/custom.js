function playAudio(audio_id) {
  document.getElementById("sound_" + audio_id).onclick = function() {
    pauseAudio(audio_id)
    return false
  }
  document.getElementById("icon_sound_" + audio_id).className = "fas fa-pause"
  var x = document.getElementById(audio_id)
  x.play()
  clickedSound(audio_id)
}

function clickedSound(audio_id) {
  var route = "/clicked/" + audio_id
  req = new XMLHttpRequest()
  // req.open("GET", route, false)
  req.open("GET", route, true)
  req.send()
}

function pauseAudio(audio_id) {
  document.getElementById("sound_" + audio_id).onclick = function() {
    playAudio(audio_id)
    return false
  }
  document.getElementById("icon_sound_" + audio_id).className = "fas fa-play"
  var x = document.getElementById(audio_id)
  x.pause()
}

function stopAudio(audio_id) {
  document.getElementById("sound_" + audio_id).onclick = function() {
    playAudio(audio_id)
    return false
  }
  document.getElementById("icon_sound_" + audio_id).className = "fas fa-play"
  var x = document.getElementById(audio_id)
  x.load()
}

function toggleModal() {
  var e = document.getElementById("modal")
  if (e.classList.contains("is-active")) {
    e.classList.remove("is-active")
  } else {
    e.classList.add("is-active")
  }
}

function submitSoundspende() {
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

  var route = "/soundspende/submit"

  var target = "main_content"
  // KRÜCKE
  var request = new XMLHttpRequest()
  request.open("POST", route)
  request.ontimeout = function() {
    window.location.href = "/"
  }
  request.onload = function() {
    if (request.readyState === 4) {
      if (request.status === 200) {
        window.location.href = "/"
      }
    }
  }
  request.timeout = 10000
  request.send(formData)
}

function hide_sounds() {
  nameDivs = document.getElementsByClassName("soundcard")
  for (var j = 0, divsLen = nameDivs.length; j < divsLen; j++) {
    nameDivs[j].style.display = "none"
  }
}

function display_sounds() {
  nameDivs = document.getElementsByClassName("soundcard")
  for (var j = 0, divsLen = nameDivs.length; j < divsLen; j++) {
    nameDivs[j].style.display = "block"
  }
}

function filter_sounds() {
  document.getElementById("div_search").classList.add("is_loading")
  var str_needle = tb_search.value
  if (str_needle == "") {
   display_sounds()
  } else {
    hide_sounds()
    var o_edit = document.getElementById("tb_search")
    str_needle = str_needle.toUpperCase()
    var searchStrings = str_needle.split(/\W/)

    for (var i = 0, len = searchStrings.length; i < len; i++) {
      var currentSearch = searchStrings[i].toUpperCase()
      if (currentSearch !== "") {
        nameDivs = document.getElementsByClassName("soundcard")
        for (var j = 0, divsLen = nameDivs.length; j < divsLen; j++) {
          if (
            nameDivs[j].textContent.toUpperCase().indexOf(currentSearch) !== -1
          ) {
            nameDivs[j].style.display = "block"
          }
        }
      }
    }
  }

  document.getElementById("div_search").classList.remove("is_loading")
}
