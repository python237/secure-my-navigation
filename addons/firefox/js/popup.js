// --
// Variables
// --
var pageType = z("#browserContent").attr("data-pos");
var target = "http://localhost:4700/";


// --
// Operations
// --

if (pageType === "home") {
	browser.tabs.query({
		currentWindow: true,
		active: true
	}).then(function(tabs) {
		for (let tab of tabs) {
			/** 
			 * Envoie d'une requete au content_script 'app.js' pour récupérer 
			 * le nom de domaine du site sur lequel se trouve l'utilisateur.
			*/
			browser.tabs.sendMessage(tab.id, {
				action: "getHost"
			}, function(response) {
				if (response && response.host)
					z("#homeSource").inner(response.host);
			});
		}
	});
}
else if (pageType === "search") {
	z("#searchButton2").click(function() {
		/**
		 * Envoie au serveur du nom de domaine signalée par l'utilisateur.
		*/
		var text = z("#searchInput").attr("value");

		if (text && text.length > 0)  {
			const xhttp = new XMLHttpRequest();

			xhttp.onload = function() {
				var response = JSON.parse(this.responseText);

				z("#searchButton2").removeCSS("display");
				z("#buttonLoader")._addCSS("display", "none", true);
				z("#searchInput").removeAttr("disabled");

				if (response.decision === "add") {
					z("#browserContentResultSource").inner(response.source);
					z("#browserContentResult").removeCSS("display");
					z("#browserContentError")._addCSS("display", "none", true);
				}
				else if (response.decision === "invalid") {
					z("#browserContentError").removeCSS("display");
					z("#browserContentResult")._addCSS("display", "none", true);
				}

				setTimeout(function() {
					z("#browserContentResult")._addCSS("display", "none", true);
					z("#browserContentError")._addCSS("display", "none", true);
				}, 10000);
			}
			xhttp.open("GET", target + "signalment?host_source=" + window.encodeURIComponent(text), true);
			xhttp.send();

			z("#searchButton2")._addCSS("display", "none", true);
			z("#searchInput").attr("value", "").attr("disabled", "true");
			z("#buttonLoader").removeCSS("display");
			z("#browserContentResult")._addCSS("display", "none", true);
			z("#browserContentError")._addCSS("display", "none", true);
		}
	});
}