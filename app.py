from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
def detect_intent_texts(text):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    #print('Session path: {}\n'.format(session))

    text_input = dialogflow.types.TextInput(
        text=text, language_code='en-US')

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    #print('=' * 20)
    #print('Query text: {}'.format(response.query_result.query_text))
    #print('Detected intent: {} (confidence: {})\n'.format(
        #response.query_result.intent.display_name,
        #response.query_result.intent_detection_confidence))
    print('Chatbot:\n\t{}'.format(
        response.query_result.fulfillment_text))

def cb():
    return "Okay, i will get you chatbot!!"		
		

@app.route("/")
def hello():
    return "Hello World!"
	
	
	
@app.route("/chatbot")
def chatbot():
    return render_template('index2.html')

@app.route("/chatbot1", methods=['POST','GET'])
def chatbot1():
    if request.method == 'POST':
        print ("post request")
        return jsonify(answer = 'abc')
