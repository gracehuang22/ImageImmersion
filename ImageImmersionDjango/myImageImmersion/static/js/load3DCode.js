function loadCodeProj(txtFile) {
	var xmlhttp, filetxt;
	if(window.XMLHttpRequest) {
		xmlhttp = new XMLHttpRequest();
	}
	else {
		xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
	}
	xmlhttp.onreadystatechange=function() {
		if(xmlhttp.readyState == 4 && xmlhttp.status == 200){
			filetxt = xmlhttp.responseText;
			var lines = filetxt.split("\n");
			$.each(lines, function(i, v) {
				imgDesc = v.split("; ");
				$(".imageGallery").append('<div class = "codeEntry ' + imgDesc[1] +
				'"><div class = "box ' + imgDesc[1] +
				'">' +
				'<a href = "' + imgDesc[4] + '">' +
				'<img class = "' + imgDesc[0] + '" src = "' +
				imgDesc[2] + '">' + "\n" +
				'</a>' +
				'<div class = "descriptionTitle">' +
				imgDesc[3] + '</div>' + '</div>' +
				'<div class = "codeTitle"><h1>' +
				imgDesc[3] +
				'</h1><div class = "codeDescription"><p>' +
				imgDesc[5] + '</p></div>' + '<div class = "codeLangs"><p>' +
				imgDesc[6] + '</p></div>' +
				'</div>');
			});
		}
		hover();
	}
	xmlhttp.open("GET", txtFile, true);
	xmlhttp.send();
}
