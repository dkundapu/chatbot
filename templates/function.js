		var chat_start_flag = 0;
		var accessToken = "7d46ebd96d2d40baa4b8e21992cbfc24";
		var baseUrl = "https://api.api.ai/v1/";
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
			$("#rec").click(function(event) {
				switchRecognition();
			});
		});
		var recognition;
		function startRecognition() {	
			recognition = new webkitSpeechRecognition();
			recognition.onstart = function(event) {
				updateRec();
			};
			recognition.onresult = function(event) {
				var text = "";
			    for (var i = event.resultIndex; i < event.results.length; ++i) {
			    	text += event.results[i][0].transcript;
			    }
			    setInput(text);
				stopRecognition();
			};
			recognition.onend = function() {
				stopRecognition();
			};
			recognition.lang = "en-US";
			recognition.start();
		}
	
		function stopRecognition() {
			if (recognition) {
				recognition.stop();
				recognition = null;
			}
			updateRec();
		}
		function switchRecognition() {
			if (recognition) {
				stopRecognition();
			} else {
				startRecognition();
			}
		}
		function setInput(text) {
			$("#input").val(text);
			send();
		}
		function updateRec() {
			$("#rec").text(recognition ? "Stop" : "Speak");
		}
		function send_hi() {
			var text = 'show_list_1';
			$.ajax({
				type: "POST",
				url: baseUrl + "query?v=20150910",
				contentType: "application/json; charset=utf-8",
				dataType: "json",
				headers: {
					"Authorization": "Bearer " + accessToken
				},
				data: JSON.stringify({ query: text, lang: "en", sessionId: "somerandomthing" }),
				success: function(data) {
					var abc = JSON.stringify(data, undefined, 2);
					setResponse(abc);
					setResponseText(data.result.fulfillment.speech);
					chat_start_flag = 1;
				},
				error: function() {
					setResponse("Internal Server Error");
				}
			});
			
		}
		function send_bg() {
			var text = 'show_list_1';
			$.ajax({
				type: "POST",
				url: baseUrl + "query?v=20150910",
				contentType: "application/json; charset=utf-8",
				dataType: "json",
				headers: {
					"Authorization": "Bearer " + accessToken
				},
				data: JSON.stringify({ query: text, lang: "en", sessionId: "somerandomthing" }),
				success: function(data) {
					var abc = JSON.stringify(data, undefined, 2);
					setResponse(abc);
					setResponseText(data.result.fulfillment.speech);
					chat_start_flag = 1;
				},
				error: function() {
					setResponse("Internal Server Error");
				}
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
			$.ajax({
				type: "POST",
				url: baseUrl + "query?v=20150910",
				contentType: "application/json; charset=utf-8",
				dataType: "json",
				headers: {
					"Authorization": "Bearer " + accessToken
				},
				data: JSON.stringify({ query: text, lang: "en", sessionId: "somerandomthing" }),
				success: function(data) {
					var abc = JSON.stringify(data, undefined, 2);
					setResponse(abc);
					setResponseText(data.result.fulfillment.speech);
				},
				error: function() {
					setResponse("Internal Server Error");
				}
			});
			//setResponse("Loading...");
			//setResponseText("Loading...");
			$("#input").val('');
		}
		function setResponse(val) {
			//$("#response").text(val);
		}
		function setResponseText(val) {
			//$("#response_text").text(val);
			var d = new Date();
			var n = d.toLocaleTimeString();
			var bot_text = `<div class="row msg_container base_receive">
								<div class="col-md-10 col-xs-10"><div class="messages msg_receive">  
                                <p> ` + val + `</p>
                                <time datetime="2009-11-13T20:00">`+n+`</time>
                            </div>
                        </div>
                    </div>`;
			$("#chat_container").append(bot_text);
			$('#chat_container').animate({scrollTop: $('#chat_container').prop("scrollHeight")}, 250);
		}
	