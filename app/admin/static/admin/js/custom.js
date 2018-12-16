var file = document.getElementById("file");
file.onchange = function(){
    if(file.files.length > 0)
    {
      document.getElementById('filename').innerHTML =file.files[0].name;
    }
};

function addItem() {
    document.getElementById("bt_submit").className = "button is-pulled-right is-info is-loading";
    var name = document.getElementById("tb_name").value;
    var description = document.getElementById("tb_description").value;
    var soundfile = document.getElementById("soundfile");

    // check data
    if (!isStr(name)) {
        alert("error: name");
        return;
    }
    if (!isStr(description)) {
        alert("error: description");
        return;
    }

    var formData = new FormData();
    formData.append("name", name);
    formData.append("description", description);
    formData.append("soundfile", soundfile.files[0]);

    var route = "/admin/sound/submit";



    //TODO
    var target = "main_content";
    // KRÜCKE
    var request = new XMLHttpRequest();
    request.open("POST", route);
    request.ontimeout = function() {
        window.location.href = subdir_kochbuch + "/create_item";
    };
    request.onload = function() {
        if (request.readyState === 4) {
            if (request.status === 200) {
                window.location.href = subdir_kochbuch + "/create_item";
            }
        }
    };
    request.timeout = 10000;
    request.send(formData);
}
