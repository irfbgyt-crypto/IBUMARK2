document.addEventListener("keydown", function(e){

    if(e.ctrlKey){

        switch(e.key){

            case "1":
                window.location.href="/";
                break;

            case "2":
                window.location.href="/medidas";
                break;

            case "3":
                window.location.href="/rutina";
                break;

            case "4":
                window.location.href="/ejercicios";
                break;

            case "5":
                window.location.href="/progreso";
                break;

            case "6":
                window.location.href="/ayuda";
                break;

        }

    }

});