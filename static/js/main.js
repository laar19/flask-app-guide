/*------------------------------------*/
// Resalta las opciones del menú
var url = window.location.pathname;
url = url.split("/");
element = document.getElementById(url[1]);
element.classList.add("active");

/*------------------------------------*/
// Valida los formularios
document.getElementById("username").addEventListener("blur", function() {

    if(document.getElementById("username").value.match(/[ºª!|@"#·~$½%¬&{/[(=?¿`^+*}´¨çÇ,;:·"]/)) {
        alert("Sólo letras y números por favor");
        document.getElementById("username").value = "";
    };

});