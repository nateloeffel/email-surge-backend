from flask import Flask, request, jsonify
from time import sleep
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()


api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)


def generate_response(data):
    company_name = data['companyName']
    target_name = data['targetName']
    target_type = data['targetType']
    sender_name = data['senderName']
    sender_service = data['senderService']

    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You are an email copywriter, skilled in creating cold emails that will generate leads and responses. You will be given multiple different details in this format: \n Sender's Company Name, this is the name of the company or agency that the sender is working for.\n Sender Service, this is the service that the sender wants to provide to the target user.\n Sender Name, This is the name of the person who will be sending the email. Use this for the closing.\n Target Name, this will be the name of the person or company that the email is going to. Whether it is the name or the company will be determined by the target type.\n Target Type, this will be whether the target is a company or an individual. \n\n\n Based on this information you will craft an email that generates leads for the given service, using the details provided. The email should not be long at all and needs to be to the point. Short and sweet. No more than 4 paragraphs."},
            {"role": "user", "content": f"Write an email that will generate leads. Here are your details. \n Sender Company's Name: {company_name}\nSender Service: {sender_service}\n Sender Name: {sender_name}\n Target Name: {target_name}\nTarget Type {target_type}"}
        ]
    )

    return completion.choices[0].message.content



    

app = Flask(__name__)
CORS(app)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({ 'message': "hello" })

@app.route('/create', methods=['POST'])
def create():
    print("create")
    data = request.json
    email = generate_response(data)
    return jsonify({ 'message': email })



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, port=port)
