/**
 * Licensed under the Apache License, Version 2.0 (the "License"); you may
 * not use this file except in compliance with the License. You may obtain
 * a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations
 * under the License.
 */

/**
 * This file contains all of the web and hybrid functions for interacting with 
 * the basic chat bot output.
 * Leveraged from: https://github.com/sharpstef/watson-bot-starter
 */
"use strict";



// variables for chat and stored context specific events



var watson = 'Bot';

/**
 * @summary Display Chat Bubble.
 *  *
 * Formats the chat bubble element based on if the message is from the user or from Bot.
 *
 * @function displayMessage
 * @function displayButtonImage
 * @function displayproductpage
 * @function displayaccordion
 * 
 * @param {String} text - Text to be displayed in chat box.
 * @param {String} user - Denotes if the message is from Bot or the user. 
 * @return null
 */

function displayMessage(text, user) {

console.log('display message::',text,' user ::',user);
    if (text && text != "") {



        var chat = document.getElementById('chatBox');
        var bubble = document.createElement('div');

        // Set chat bubble color and position based on the user parameter
        if (user === watson) {

            bubble.className = 'bot_message';  // Bot text formatting
            bubble.innerHTML = "<div class='bot'>" + text + "</div>";


        } else {
            bubble.className = 'user_message';  // User text formatting
            bubble.innerHTML = "<div class='user'>" + text + "</div>";
        }

        chat.appendChild(bubble);
        chat.scrollTop = chat.scrollHeight;  // Move chat down to the last message displayed
        //document.getElementById('chatMessage').focus();
    }

    return null;
}

function displayButtonImage(url) {
    console.log('display button image::',url);

    if(url){
        
        //var acc=document.getElementsByClassName("accordion");
        //url for image
        //var butt=document.createElement('button')


        var image=document.createElement("img");
        image.src = url;
        var im=image.src;
        var n=/pict/;
        
        if (n.test(im)){

            var image=document.createElement("img");
            image.src = url;

            image.className = 'button';


        } 
        
               

        
       //url for product page
        var purl=document.createElement("a");	
        //var purltext=document.createTextNode("Add to cart");
        var image=document.createElement("img");
        image.src = url;
        var q=/rover/;
        var am=/product/
        
        if (q.test(im)){

              var image=document.createElement("a");
              image.src = '#';
  
  
          }

        if (am.test(im)){


            var image=document.createElement("a");
            image.src = '#';


        }

        purl.href=url;
        var ix=purl.href;
        var m=/rover/;
        
        if (m.test(ix)){
            var purl=document.createElement("a");
            purl.href=url;
            purl.target="_blank";
            purl.innerHTML="BUY NOW";

        }

        
        //purl.href.match=rover.ebay.com;
        //window.location.host="rover.ebay.com"
        

        

        //this logic works for post go live...
        //var add2cart=document.createElement("a");
        //add2cart.innerHTML="Add to Cart";
        //add2cart.href="/my-link/";
        // till here...


        
        
                       				
              
        document.body.appendChild(image);
        document.body.appendChild(purl);
        	
        //document.body.appendChild(image1);		
        //document.body.appendChild(add2cart); 
        
        //we need to activate this for add 2 cart
       
                

        var chat=document.getElementById('chatBox');
        //chat.innerHTML=image.src;
        chat.appendChild(image);
        chat.appendChild(purl);	
       	
        //chat.appendChild(image1);
       // chat.appendChild(add2cart); 
        
        //we need to activate this for add 2 cart
        

        chat.scrollTop=chat.scrollHeight;			
        				
        	       
        }
     
    return null;

}

//amazon
function displayamazonimage(url){

    console.log('displayamazonimage::',url);

    if (url){

        //amazon pics pending
        // code for image as button
        var image=document.createElement("img");
        image.src = url;
        var im1=image.src;
        var n=/pict/;
        
        if (n.test(im1)){

            var image=document.createElement("img");
            image.src = url;

            image.className = 'button';
            //image.className = 'accordion';

        }
        //amazon

              

        var apurl=document.createElement("a");
        var image=document.createElement("img");
        

        //code for product page as next page
        apurl.href=url;
        var ap=apurl.href;
        var pa=/product/;
        
        if (pa.test(ap)){

            var apurl=document.createElement("a");
            apurl.href=url;
            apurl.target="_blank";
            apurl.innerHTML="BUY NOW";
            
        }

        
        
        document.body.appendChild(apurl);
//document.body.appendChild(acc);
        var chat=document.getElementById('chatBox');
        //chatbox class is the link between this method and loginhtml jqery as that is the id where changes are desired
        chat.appendChild(apurl);
      //  chat.appendChild(acc);
        chat.scrollTop=chat.scrollHeight;
    }
    return null;
} 

//function displayaccordion(text){

  //  if (text='AAccordion'){


    //}
//}

//var acc = document.getElementsByClassName("accordion");
  //  var i;
    
    //for (i = 0; i < acc.length; i++) {
      //acc[i].addEventListener("click", function() {
        //this.classList.toggle("active");
        //var panel = this.nextElementSibling;
        //if (panel.style.display === "block") {
          //panel.style.display = "none";
      //  } else {
        //  panel.style.display = "block";
        //}
      //});
    //}





