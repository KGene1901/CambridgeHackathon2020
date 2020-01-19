// function duplication() {
//     for (k=3; k<20; k++){var elmnt = document.getElementById("A3");
//     var cln = elmnt.cloneNode(true);
//     document.body.appendChild(cln);}
// }


window.onload = function(){
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
    if(xmlhttp.status==200 && xmlhttp.readyState==4){    
        var words = xmlhttp.responseText.split('$');
        console.log(words)
        j=1
        for (i = 1; i<10; i+=4){
            document.getElementById('A'.concat(j)).value=(words[i]);
            document.getElementById('Q'.concat(j)).value=(1);
            j+=1
        }
    }
    }
    xmlhttp.open("GET","https://raw.githubusercontent.com/Miyamura80/CambridgeHackathon2020/master/Adding_Cart/Shopping_List.txt",true);
    xmlhttp.send();

    // var button_2 = document.getElementById('dup');
    // button_2.duplication()
    // setTimeout(button_2.duplication(), 10000);
    var button = document.getElementById('clickButton');
    //setTimeout(function(){button.form.submit();}, 200);
    }