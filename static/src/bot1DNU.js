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


    if(url){
        
        //var acc=document.getElementsByClassName("accordion");
        //url for image
        //var butt=document.createElement('button')


        var image=document.createElement("img");
        image.src = url;
        var im=image.src;
        var n=/pict/;
        //var q=/rover/;
        if (n.test(im)){

            var image=document.createElement("img");
            image.src = url;

            image.className = 'button';
            //image.className = 'accordion';
            //acc.image.className='accordion';


        } 
        
        //else if (q.test(im)){

          //  var image=document.createElement("img");
            //image.src = null;


        //}
        
        
        //image.src.match=pict;
        

        
       //url for product page
        var purl=document.createElement("a");	
        //var purltext=document.createTextNode("Add to cart");
        var image=document.createElement("img");
        image.src = url;
        var q=/rover/;
        if (q.test(im)){

              var image=document.createElement("a");
              image.src = '#';
  
  
          }
          
        

        purl.href=url;
        var ix=purl.href;
        var m=/rover/;
        //var ss=/product/;
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
        
        			
        //document.body.appendChild(add2cart); 
        
        //we need to activate this for add 2 cart
       
                

        var chat=document.getElementById('chatBox');
        //chat.innerHTML=image.src;
        chat.appendChild(image);
        chat.appendChild(purl);		
       
        
       // chat.appendChild(add2cart); 
        
        //we need to activate this for add 2 cart
        

        chat.scrollTop=chat.scrollHeight;			
        				
        	       
        }
     
    return null;

}






