import os
import pymysql
credential_path = "F:\dk.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
import dialogflow_v2 as dialogflow
import uuid
from flask import Flask, render_template, request, jsonify, make_response
import json
app = Flask(__name__)
def detect_intent_texts(text, session, cas_id):

	session_client = dialogflow.SessionsClient()
	text_input = dialogflow.types.TextInput(
		text=text, language_code='en-US')

	query_input = dialogflow.types.QueryInput(text=text_input)

	response = session_client.detect_intent(
		session=session, query_input=query_input)

	print("Response")
	print(response)
	fulfillmentlen = len(response.query_result.fulfillment_messages)
	cas_id = response.query_result.fulfillment_messages[0].text.text[0]
	if fulfillmentlen > 1:
		next_input = response.query_result.fulfillment_messages[1].text.text[0]
	else:
		next_input = "<input id='input' type='text' class='form-control input-sm chat_input' placeholder='Write your message here...' autocomplete='off' autofocus/><span class='input-group-btn'><button class='btn btn-primary btn-sm' id='send' value='Send'>Send</button></span><script>$('#input').keypress(function(event) {if (event.which == 13) {event.preventDefault();send();}});$('#send').click(function(event){event.preventDefault();send();});</script>"
	return jsonify({'next_input': next_input, 'message':response.query_result.fulfillment_text, 'session_variable': session, 'cas_id':cas_id})


def cb():
	return "Okay, i will get you chatbot!!"


@app.route("/")
def hello():
	return "Hello World!"

@app.route("/mywebhook", methods=['POST','GET'])
def mywebhook():
	req = request.get_json(silent=True, force=True)
	print("WebhookCalled")
	print("Action:"+req.get("queryResult").get("action"))
	#print(json.dumps(req, indent=4))
	#print(req.get("queryResult"))
	#res = makeWebhookResult(req)
	#res= {
	#    "speech": "Yayyy!! Your user ID is " + req.get("result").get("parameters").get("any"),
	#    "displayText": "Yayyy!! Your user ID is " + req.get("result").get("parameters").get("any")
	#}
	if (req.get("queryResult").get("action") == 'input.welcome'):
		res={
			"fulfillmentText": "Hello... I am your TestChatBot!!!",
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
	elif (req.get("queryResult").get("action") == 'user_id_intent'):        
		cas_id = req.get("queryResult").get("parameters").get("any").rstrip()
		print("CAS_ID ="+cas_id)
		conn = pymysql.connect("dkundapura.mysql.pythonanywhere-services.com", "dkundapura", "liaison@123", "dkundapura$harman")
		cursor = conn.cursor()
		query_string = "select cas_id, firstname, lastname from Users where cas_id = '"+cas_id+"';"
		print(query_string)
		cursor.execute(query_string)
		row = cursor.fetchone()
		conn.close()
		cas_id = ''
		if(row):
			cas_id = row[0]
			res={
				"fulfillmentText": "Hai "+row[2]+", "+row[1]+". Do you want to check your application status?",
				"fulfillmentMessages":[
					{
						"text":{
							"text": [
								cas_id
							]
						}
					},
					{
						"text":{
							"text": [
								"<input id='input' type='text' class='form-control input-sm chat_input' placeholder='Write your message here...' autocomplete='off' autofocus/><span class='input-group-btn'><button class='btn btn-primary btn-sm' id='send' value='Send'>Send</button></span><script>$('#input').keypress(function(event) {if (event.which == 13) {event.preventDefault();send();	}}); $('#send').click(function(event) {event.preventDefault();send();});</script>"
							]
						}
					},
					
				],
				"source":"mywebhook",
			}
		else:
			res={
				"fulfillmentText": "I couldn't find that CAS ID. Please try again. GIve me your 11 digit CAS ID....",
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
								"Your 11 digit CASID:<input id='cas_id' type='text' class='form-control input-sm chat_input' placeholder='Your CAS ID here...' autocomplete='off' autofocus/><span class='input-group-btn'><button class='btn btn-primary btn-sm' id='send_casid' value='Send'>Send</button></span><script> $('#send_casid').click(function(){var text='My CAS ID is '+$('#cas_id').val(); send_text(text);});</script>"
							]
						}
					}
				],
				"source":"mywebhook",
			}
	elif (req.get("queryResult").get("action") == 'application_status_yes'):
		print("CASID:")
		cas_id = req.get("queryResult").get("outputContexts")[1].get("parameters").get("any")
		print(cas_id)
		user_id = cas_id[6:11]
		print("User ID:"+user_id)
		conn = pymysql.connect("dkundapura.mysql.pythonanywhere-services.com", "dkundapura", "liaison@123", "dkundapura$harman")
		cursor = conn.cursor()
		query_string = "select user_id, application_status, complete  from ApplicantStatus where user_id = '"+user_id+"';"
		print(query_string)
		cursor.execute(query_string)
		row = cursor.fetchone()
		conn.close()
		if(row):
			user_id = row[0]
			applicant_status = row[1]
			completion_status = row[2]
			if(applicant_status == '1'):
				if(completion_status == '1'):
					status_message = 'Your Applicantion is complete. No further acton required from your side. Thank you...'
				else:
					status_message = 'Your Applicantion is submitted and yet to be completed.'
			else:
				status_message = 'You have not submitted your application yet. '
			res={
				"fulfillmentText": status_message,
				"fulfillmentMessages":[
					{
						"text":{
							"text": [
								cas_id
							]
						}
					},
					{
						"text":{
							"text": [
								"<input id='input' type='text' class='form-control input-sm chat_input' placeholder='Write your message here...' autocomplete='off' autofocus/><span class='input-group-btn'><button class='btn btn-primary btn-sm' id='send' value='Send'>Send</button></span><script>$('#input').keypress(function(event) {if (event.which == 13) {event.preventDefault();send();	}}); $('#send').click(function(event) {event.preventDefault();send();});</script>"
							]
						}
					},
					
				],
				"source":"mywebhook",
			}
		else:
			status_message = 'You have not submitted your application yet. '
			res={
				"fulfillmentText": status_message,
				"fulfillmentMessages":[
					{
						"text":{
							"text": [
								cas_id
							]
						}
					},
					{
						"text":{
							"text": [
								"<input id='input' type='text' class='form-control input-sm chat_input' placeholder='Write your message here...' autocomplete='off' autofocus/><span class='input-group-btn'><button class='btn btn-primary btn-sm' id='send' value='Send'>Send</button></span><script>$('#input').keypress(function(event) {if (event.which == 13) {event.preventDefault();send();	}}); $('#send').click(function(event) {event.preventDefault();send();});</script>"
							]
						}
					},
					
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
	r.headers['Content-Type'] = 'application/json'
	print(r)
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
	print ("post request")
	textinput = request.args.get('querry')
	print (textinput)
	session_var = request.args.get('session_var')
	print (session_var)
	cas_id = request.args.get('cas_id')
	#return jsonify(message = detect_intent_texts(textinput,session_var))
	return detect_intent_texts(textinput,session_var, cas_id)

@app.route("/initiateChat", methods=['POST','GET'])
def initChat():
	session_client = dialogflow.SessionsClient()
	session = session_client.session_path('chatbot-test1-fb4c6', uuid.uuid4())
	return detect_intent_texts('Hi',session, 'cas_id')
