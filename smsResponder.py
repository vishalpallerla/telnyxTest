import telnyx
from flask import Flask, request, Response
from urllib.parse import urlunsplit

app = Flask(__name__)
app.config.from_pyfile('config_file.cfg')

#Read the incoming sms message and respond based on the content
@app.route('/inbound', methods=['POST'])
def inbound_message():
    body = request.json
    #Generate URL for outbound method defined later to confirm delivery receipt
    delivery_reporting_url = urlunsplit((
        request.scheme,
        request.host,
        "/outbound",
        "", ""))
    incoming_msg = body['data']['payload']['text']
    incoming_msg = " ".join(incoming_msg.split()).lower()
    user_number = body['data']['payload']['from']['phone_number']
    telnyx_number = body['data']['payload']['to'][0]['phone_number']
    telnyx.api_key = app.config['API_KEY']
    is_responded = False
    if incoming_msg == 'pizza':
        response = "Chicago pizza is the best"
        is_responded = True
    if incoming_msg == 'ice cream':
        response = "I prefer gelato"
        is_responded = True
    if not is_responded:
        response = "Please send either the word ‘pizza’ or ‘ice cream’ for a different response"
    try:
        telnyx_response = telnyx.Message.create(
            from_=telnyx_number,
            to=user_number,
            text=response,
            webhook_url=delivery_reporting_url,
            use_profile_webhooks=False
        )
        print(f"Sent message with id: {telnyx_response.id}")
    except Exception as e:
        print("You came to a forbidden area. Check the error below to find out how you can go back:")
        print(e)
    return Response(status=200)

#Delivery report Confirmation
@app.route("/outbound", methods=["POST"])
def outbound_message():
    body = request.json
    message_id = body["data"]["payload"]["id"]
    print(f"Received Delivery Reporting(DLR) message with id: {message_id}")
    return Response(status=200)


if __name__ == "__main__":
    app.run(port=5000)    #Using port 5000 locally to run our web application
