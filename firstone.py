import os
credential_path = "F:\dk.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
import dialogflow_v2 as dialogflow
import uuid
from flask import Flask, render_template, request, jsonify, make_response
import json
app = Flask(__name__)
def detect_intent_texts(text, session):
	
	session_client = dialogflow.SessionsClient()
	text_input = dialogflow.types.TextInput(
		text=text, language_code='en-US')

	query_input = dialogflow.types.QueryInput(text=text_input)

	response = session_client.detect_intent(
		session=session, query_input=query_input)
	
	print("Response")
	print(response)
	fulfillmentlen = len(response.query_result.fulfillment_messages)
	if fulfillmentlen > 1:
		next_input = response.query_result.fulfillment_messages[1].text.text[0]
	else:
		next_input = "<input id='input' type='text' class='form-control input-sm chat_input' placeholder='Write your message here...' autocomplete='off' autofocus/><span class='input-group-btn'><button class='btn btn-primary btn-sm' id='send' value='Send'>Send</button></span><script>$('#input').keypress(function(event) {if (event.which == 13) {event.preventDefault();send();}});$('#send').click(function(event){event.preventDefault();send();});</script>"
	return jsonify({'next_input': next_input, 'message':response.query_result.fulfillment_text, 'session_variable': session})
	

def cb():
	return "Okay, i will get you chatbot!!"		
		

@app.route("/")
def hello():
	return "Hello World!"

@app.route("/mywebhook", methods=['POST','GET'])
def mywebhook():
	req = request.get_json(silent=True, force=True)
	print("Request:")
	#print(json.dumps(req, indent=4))
	print(req.get("queryResult"))

	#res = makeWebhookResult(req)
	#res= {
	#    "speech": "Yayyy!! Your user ID is " + req.get("result").get("parameters").get("any"),
	#    "displayText": "Yayyy!! Your user ID is " + req.get("result").get("parameters").get("any")
	#}
	if (req.get("queryResult").get("action") == 'input.welcome'):
		res={			
			"fulfillmentText": "Hello... I am your TestChatBot!",
		    "fulfillmentMessages":[
				{
					"text":{
						"text": [
							"Hi, Hello....."
						]
					}	
				},
				{
					"text":{
						"text": [
							"Please type in your CASID <input id='cas_id' type='text' class='form-control input-sm chat_input' placeholder='Your CAS ID here...' autocomplete='off' autofocus/><span class='input-group-btn'><button class='btn btn-primary btn-sm' id='send_casid' value='Send'>Send</button></span><script> $('#send_casid').click(function(){var text='My CAS ID is '+$('#cas_id').val(); send_text(text);});</script>"
						]
					}	
				}
			],
			"source":"mywebhook",
		}
	else:
		res={
			"fulfillmentText": "Hai.. "+req.get("queryResult").get("parameters").get("any")+". Let me check what I can do for you...",
		    "fulfillmentMessages":[
				{
					"text":{
						"text": [
							"Hi, Hello....."
						]
					}	
				},
				{
					"text":{
						"text": [
							"<input id='input' type='text' class='form-control input-sm chat_input' placeholder='Write your message here...' autocomplete='off' autofocus/><span class='input-group-btn'><button class='btn btn-primary btn-sm' id='send' value='Send'>Send</button></span><script>$('#input').keypress(function(event) {if (event.which == 13) {event.preventDefault();send();	}}); $('#send').click(function(event) {event.preventDefault();send();});</script>"
						]
					}	
				}
			],
			"source":"mywebhook",
		}
	res = json.dumps(res, indent=4)
	r = make_response(res)
	print(res)
	r.headers['Content-Type'] = 'application/json'
	return r
	
	
@app.route("/chatbot")
def chatbot():
	return render_template('index2.html')

@app.route("/chatbot1", methods=['POST','GET'])
def chatbot1():
	if request.method == 'POST':
		print ("post request")
		return jsonify(answer = 'abc')

@app.route("/chatbot2", methods=['POST','GET'])
def chatbot2():
	#print ("post request")
	textinput = request.args.get('querry')
	#print (textinput)
	session_var = request.args.get('session_var')
	#print (session_var)
	#return jsonify(message = detect_intent_texts(textinput,session_var))
	return detect_intent_texts(textinput,session_var)

@app.route("/initiateChat", methods=['POST','GET'])
def initChat():
	session_client = dialogflow.SessionsClient()
	session = session_client.session_path('chatbot-test1-fb4c6', uuid.uuid4())
	return detect_intent_texts('Hi',session)
