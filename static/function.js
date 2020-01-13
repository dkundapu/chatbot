		var chat_start_flag = 0;
		var session_var;
		var cas_id  = 'cas_id';
		$(document).ready(function() {
			$("#input").keypress(function(event) {
				if (event.which == 13) {
					event.preventDefault();
					send();					
				}
			});
			$("#send").click(function(event) {
				event.preventDefault();
				send();		
			});
		});
		function setInput(text) {
			$("#input").val(text);
			send();
		}
		function send_hi() {
			$("#chat_container").append("<div class='lds-waiting'><div></div><div></div><div></div></div>");
			$.getJSON('/initiateChat',{
				querry: 'hi',
			}, function (data){
				session_var = data.session_variable;
				chat_start_flag = 1;
				setResponseText(data.message);
				$(".input-group").html('');
				$(".input-group").html(data.next_input);
				$('.lds-waiting').remove();
			});
			
		}
		function send_bg(text) {
			$("#chat_container").append("<div class='lds-waiting'><div></div><div></div><div></div></div>");
			$.getJSON('/chatbot2',{
				querry: text,
				session_var: session_var
			}, function (data){
				session_var = data.session_variable;
				chat_start_flag = 1;
				setResponseText(data.message);
				$(".input-group").html('');
				$(".input-group").html(data.next_input);
				$('.lds-waiting').remove();
			});
			
		}
		function send() {
			var text = $("#input").val();
			if (text == ""){
				return;
			}
			var d = new Date();
			var n = d.toLocaleTimeString();
			var my_text = '<li><div id="me">' + text + '</div></li>';
			var my_text = `<div class="row msg_container base_sent">
								<div class="col-md-10 col-xs-10"><div class="messages msg_sent">  
                                <p> ` + text + `</p>
                                <time datetime="2009-11-13T20:00">`+n+`</time>
                            </div>
                        </div>
                    </div>`;			
			
			$("#chat_container").append(my_text);
			$('#chat_container').animate({scrollTop: $('#chat_container').prop("scrollHeight")}, 250);
			$("#chat_container").append("<div class='lds-waiting'><div></div><div></div><div></div></div>");
			$.getJSON('/chatbot2',{
				querry: text,
				session_var: session_var,
				cas_id: cas_id
			}, function (data){
				console.log(data);
				cas_id = data.cas_id;
				setResponseText(data.message);
				$(".input-group").html('');
				$('.input-group').html(data.next_input);
				$('.lds-waiting').remove();
			});	
			$("#input").val('');
		}
		
		function send_more(text){
			send_bg(text);
			$('.next_input').parent().parent().parent().remove();
		}

		function send_text(text) {
			if (text == ""){
				return;
			}
			var d = new Date();
			var n = d.toLocaleTimeString();
			var my_text = '<li><div id="me">' + text + '</div></li>';
			var my_text = `<div class="row msg_container base_sent">
								<div class="col-md-10 col-xs-10"><div class="messages msg_sent">  
                                <p> ` + text + `</p>
                                <time datetime="2009-11-13T20:00">`+n+`</time>
                            </div>
                        </div>
                    </div>`;			
			
			$("#chat_container").append(my_text);
			$('#chat_container').animate({scrollTop: $('#chat_container').prop("scrollHeight")}, 250);
			$("#chat_container").append("<div class='lds-waiting'><div></div><div></div><div></div></div>");
			
			$.getJSON('/chatbot2',{
				querry: text,
				session_var: session_var,
				cas_id: cas_id
			}, function (data){
				console.log(data);
				setResponseText(data.message);
				$(".input-group").html('');
				$(".input-group").html(data.next_input);
				$('.lds-waiting').remove();
			});	
			/*$('.input-group').val('');*/
			$("#input").val('');
		}
		function setResponseText(val) {
			var d = new Date();
			var n = d.toLocaleTimeString();
			var bot_text = `<div class="row msg_container base_receive bounceInRight">
								<div class="col-md-10 col-xs-10"><div class="messages msg_receive">  
                                <p> ` + val + `</p>
                                <time datetime="2009-11-13T20:00">`+n+`</time>
                            </div>
                        </div>
                    </div>`;
			$("#chat_container").append(bot_text);
			$('#chat_container').animate({scrollTop: $('#chat_container').prop("scrollHeight")}, 250);
		}
	