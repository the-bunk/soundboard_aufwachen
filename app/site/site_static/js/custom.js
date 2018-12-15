    function playAudio(audio_id) {
       document.getElementById("sound_" + audio_id).onclick = function() { pauseAudio(audio_id); } 
       document.getElementById("icon_sound_" + audio_id).className = "fas fa-pause"
        var x = document.getElementById(audio_id);
        x.play();
    }

    function pauseAudio(audio_id) {
       document.getElementById("sound_" + audio_id).onclick = function() { playAudio(audio_id); };
       document.getElementById("icon_sound_" + audio_id).className = "fas fa-play"
        var x = document.getElementById(audio_id);
        x.pause();
    }

    function stopAudio(audio_id) {
       document.getElementById("sound_" + audio_id).onclick = function() { playAudio(audio_id); };
       document.getElementById("icon_sound_" + audio_id).className = "fas fa-play"
        var x = document.getElementById(audio_id);
        x.load();
    }
