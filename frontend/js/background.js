
function getCookies(domain, name, callback) {
chrome.cookies.get({"url": domain, "name": name}, function(cookie) {
    if(callback) {
        callback(cookie.value);
    }
});
}

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    console.log("xexe");

    getCookies("https://music.mts.ru/", request.giveMe, function(id) {
      sendResponse({here: id});
      });
    return true;
});





chrome.browserAction.onClicked.addListener(function(tab) {
	chrome.tabs.create({
		url: "https://music.mts.ru"
	});
	//usage:
});

let haveLicense;

chrome.extension.onMessage.addListener(function(request, sender, sendResponse) {
	switch (request.action) {

		// Копировать
		case 'copy':
			let a = $('TEXTAREA');
			a.val(request.text);
			a.select();
			if (document.execCommand('copy', false, null)) {
				sendResponse({result: true});
			} else {
				sendResponse({result: false});
			}
			break;
		case 'check':
		    sendResponse({result: true});
		    break;
			getLicense();
			setTimeout(function checkSubs() {
				if(haveLicense === undefined) {
					setTimeout(checkSubs, 500);
				}
				else {
					console.log(haveLicense);
					if(haveLicense) {
						sendResponse({result: true});
					}
					else {
						sendResponse({result: false});
					}
				}
			}, 500);
			break;
	}
});




function getLicense() {
	let CWS_LICENSE_API_URL = 'https://www.googleapis.com/chromewebstore/v1.1/userlicenses/';
	xhrWithAuth('GET', CWS_LICENSE_API_URL + chrome.runtime.id, true, onLicenseFetched);
}

function onLicenseFetched(error, status, response) {
	console.log(error, status, response);
	response = JSON.parse(response);
	if (status === 200) {
		parseLicense(response);
	} else {
		console.log("Error reading license server.");
	}
}

function parseLicense(license) {
	if (license.result) {
		console.log("Fully paid & properly licensed.");
		haveLicense = true;
	}

	else {
		console.log("No license ever issued.");
		haveLicense = false;
	}
}


function xhrWithAuth(method, url, interactive, callback) {
	let retry = true;
	getToken();
	let access_token;

	function getToken() {
		console.log("Calling chrome.identity.getAuthToken", interactive);
		console.log(chrome.identity);
		chrome.identity.getAuthToken({ interactive: interactive }, function(token) {
			if (chrome.runtime.lastError) {
				callback(chrome.runtime.lastError);
				return;
			}
			console.log("chrome.identity.getAuthToken returned a token", token);
			access_token = token;
			requestStart();

		});
	}

	function requestStart() {

		let xhr = new XMLHttpRequest();

		xhr.open(method, url);
		xhr.setRequestHeader('Authorization', 'Bearer ' + access_token);
		xhr.onreadystatechange = function (oEvent) {
			if (xhr.readyState === 4) {
				if (xhr.status === 401 && retry) {
					retry = false;
					chrome.identity.removeCachedAuthToken({ 'token': access_token },
						getToken);
				} else if(xhr.status === 200){
					console.log("Authenticated XHR completed.");
					callback(null, xhr.status, xhr.response);
				}
			}else{
				console.log("Error - " + xhr.statusText);
			}
		};
		try {
			xhr.send();
		} catch(e) {
			console.log("Error in xhr - " + e);
		}

	}


}
