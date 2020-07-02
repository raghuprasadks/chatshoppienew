function displayaccordion(){

    var acc=document.getElementsByClassName("accordion");
    var i;

        for(i=0;i<acc.length;i++){

            acc[i].addEventListener("click",function(){
                /* Toggle between adding and removing the "active" class,
                  to highlight the button that controls the panel */
              this.classList.toggle("active");

              /*Toggle between hiding and showing the panel*/
              var panel=this.nextElementSibling;
              if(panel.style.display==="block"){
                  panel.style.display="none";

              } else {
                  panel.style.display="block";
              }
            });

            document.body.appendChild(acc);

            var chat=document.getElementById('chatbox');
            chat.appendChild(acc);

            chat.scrollTop=chat.scrollHeight;

        }
}   
