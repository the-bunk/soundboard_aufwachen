var file = document.getElementById("file");
file.onchange = function(){
    if(file.files.length > 0)
    {
      document.getElementById('filename').innerHTML =file.files[0].name;
    }
};


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


function toggleSoundToBoard(sound_id){
    var e = document.getElementById('sound_'+sound_id)
    if (e.classList.contains('is-danger')){
        e.classList.remove('is-danger')
        e.classList.add('is-success')
    }
    else{
        e.classList.remove('is-success')
        e.classList.add('is-danger')
    }
}


function getSoundsToBoard(){
    var sound_list = [];
    var x = document.getElementById("sounds_to_board");
    var y = x.getElementsByTagName("a");
    for (let item of y) {
        if (item.classList.contains('is-success')){
            sound_list.push(item.getAttribute('data-id'));
        }
    }
    return sound_list;
}


function submitBoard(){
    var name = document.getElementById('tb_name');
    var sounds = getSoundsToBoard();
    alert(sounds);
    

    //TODO jetzt noch dieses doofe xhtml-request zeug
}


