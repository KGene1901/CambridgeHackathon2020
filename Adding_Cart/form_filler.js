window.onload = function(){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
    if(xmlhttp.status==200 && xmlhttp.readyState==4){    
        var words = xmlhttp.responseText.split('$');
        for (i = 1; i<5; i+=3){
            document.getElementById('A'.concat(i)).value=(words[i]);
            document.getElementById('Q'.concat(i)).value=(1);
        }
    }
    }
    xmlhttp.open("GET","https://raw.githubusercontent.com/Miyamura80/CambridgeHackathon2020/master/Shopping_List.txt",true);
    xmlhttp.send();
    
    var button = document.getElementById('clickButton');
    setTimeout(function(){button.form.submit();}, 300);
    }