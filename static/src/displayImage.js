function displayImage(url) {
    if (url) {
        var purl = document.createElement("a");
        //var purltext=document.createTextNode("Add to cart");
        purl.href = url;
        //purl.href.match=rover.ebay.com;
        //window.location.host="rover.ebay.com"
        purl.target = "_blank";
        purl.innerHTML = "BUY NOW";
    }
    document.body.appendChild(image1);
    var chat = document.getElementById('chatBox');
    //var chat = iframe.contentWindow.document.getElementById('chatBox');
    chat.appendChild(image1);
    //chat.appendChild(purl);
    //chat.scrollTop = chat.scrollHeight;  // Move chat down to the last message displayed
}
return null;
