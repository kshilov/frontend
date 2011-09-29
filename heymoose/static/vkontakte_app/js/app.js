//additional properties for jQuery object
$(document).ready(function(){
   //align element in the middle of the screen
   $.fn.alignCenter = function() {
      //get margin left
      var marginLeft =  - $(this).width()/2 + 'px';
      //get margin top
      var marginTop =  - $(this).height()/2 + 'px';
      //return updated element
      return $(this).css({'margin-left':marginLeft, 'margin-top':marginTop});
   };
   $.fn.togglePopup = function(){
     //detect whether popup is visible or not
     if($('#popup').hasClass('hidden'))
     {
       //hidden - then display
       //when IE - fade immediately
       if($.browser.msie)
       {
         $('#opaco').height($(document).height()).toggleClass('hidden')
                    .click(function(){$(this).togglePopup();});
       }
       else
       //in all the rest browsers - fade slowly
       {
         $('#opaco').height($(document).height()).toggleClass('hidden').fadeTo('slow', 0.7)
                    .click(function(){$(this).togglePopup();});
       }
       $('#popup')
         .html($(this).html())
         .alignCenter()
         .toggleClass('hidden');
     }
     else
     {
       //visible - then hide
       $('#opaco').toggleClass('hidden').removeAttr('style').unbind('click');
       $('#popup').toggleClass('hidden');
     }
   };
});

//VK.init(function() {
	load_offers();
//});

function load_offers(){
	var app_id = $('#happ_app_id').attr('value');
	var sig = $('#happ_sig').attr('value');
	var data = "app_id=" + app_id + "&sig=" + sig;
	$.ajax({
		type: "POST",		
		//url: "http://heymoose.com:8080/get_offers",
		url: "http://127.0.0.1:5000/get_offers",
		data : data,
		context: document.body,
		success: function(msg){
			$('#offer_list').append(msg);
			// Add user_id to template
			$('.user_id').each(function(){
				$(this).attr('value', $('#happ_user_id').attr('value'));
			})

		},
		error: function(){ 
			$('#offer_list').append("Извините, нет доступных предложений. Попробуйте позже");
		}
	});	
}

