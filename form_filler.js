window.onload = function(){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
    if(xmlhttp.status==200 && xmlhttp.readyState==4){    
        var words = xmlhttp.responseText.split('$');
        j=1
        for (i = 1; i<10; i+=2){
            document.getElementById('A'.concat(j)).value=(words[i]);
            document.getElementById('Q'.concat(j)).value=(1);
            j+=1
        }
    }
    }
    xmlhttp.open("GET","https://raw.githubusercontent.com/Miyamura80/CambridgeHackathon2020/master/Shopping_List_b.txt",true);
    xmlhttp.send();

  
    var button = document.getElementById('clickButton');
    setTimeout(function(){button.form.submit();}, 500);
    }