// --
// Écoute des demandes envoyer par le fichier 'popup.js'
// --

browser.runtime.onMessage.addListener(function(request, sender, sendResponse) {
	if (request.action == "getHost")
		// Renvoie le nom de domaine du site sur lequel se trouve l'utilisateur
		sendResponse({ 
			host: window.location.host 
		});
	else sendResponse({}); // N'envoie rien 
});