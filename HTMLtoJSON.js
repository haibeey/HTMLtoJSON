//function to retrieve all child nodes of an element
function elementNodes(element){
	
	if(element.nodeType==document.ELEMENT_NODE){
		var main={name:element.tagName,
				textContent:element.textContent,
				attributes:element.hasAttributes()?element.attributes:{},
				children:[]
		};
		for(var i=0;i<element.childNodes.length;i++){
			main.children.push(elementNodes(element.childNodes[i]));
		}
		return main;
	}else if(element.nodeType==document.TEXT_NODE){
		return element.textContent;
	}else{
		return element.textContent;
	}
}

function HTMLtoJSON(element){
	return JSON.stringify(elementNodes(element));
}

//console.log(HTMLtoJSON(document.getElementsByTagName("html")[0]));

