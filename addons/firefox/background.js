// --
// Variables
// --

var target = "http://localhost:4700/";  // Addresse du serveur 'SecureMyNavigation'
var target2 = "localhost:4700";         // Domaine exempt d'analyse de sécurité


// --
// Fonctions
// --

/**
 * Vérifie si l'adresse URL sur laquelle l'utilisateur souhaite accéder est sûr.
 * @param {String} url : il s'agit de l'adresse url dans la barre d'adresse du navigateur utilisateur.
 * @returns La réponse du serveur
 */
function verify(url) {
    const xhttp = new XMLHttpRequest();
    var response = undefined;

    xhttp.onload = function() {
        response = JSON.parse(this.responseText);
    }
    xhttp.open("GET", target + "verify?host_source=" + window.encodeURIComponent(url), false);
    xhttp.send();

    return response;
}

/**
 * Bloque ou autorise l'accès à une adresse URL. (en se basant sur la réponse du serveur)
 * @param {JSON} requestDetails : les détails de la ressource auxquels l'utilisateur souhaite accéder.
 * @returns 
 */
function redirect(requestDetails) {
    if (requestDetails.url.indexOf(target2) < 0) {
        var response = verify(requestDetails.url);

        if (response.decision === "block")
            // Il s'agit d'un site jugé malveillant par le serveur, alors on bloque l'accès à la ressource.
            return {
                redirectUrl: target + "blocked/" + response.source
            };
    }
}


// --
// Écoute des requetes de l'utilisateur.
// --

browser.webRequest.onBeforeRequest.addListener(
    redirect,
    {
        urls:["<all_urls>"], 
        types: ["main_frame"]
    },
    ["blocking"]  // Permission de bloquer la requette
);