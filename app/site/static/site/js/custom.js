function playAudio(audio_id) {
  document.getElementById("sound_" + audio_id).onclick = function() {
    pauseAudio(audio_id);
      return false;
  };
  document.getElementById("icon_sound_" + audio_id).className = "fas fa-pause";
  var x = document.getElementById(audio_id);
  x.play();
  clickedSound(audio_id);
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
      return false;
  }
  document.getElementById("icon_sound_" + audio_id).className = "fas fa-play"
  var x = document.getElementById(audio_id)
  x.pause()
}

function stopAudio(audio_id) {
  document.getElementById("sound_" + audio_id).onclick = function() {
    playAudio(audio_id)
      return false;
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

