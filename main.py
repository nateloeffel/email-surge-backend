from flask import Flask, request, jsonify
from time import sleep
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from linkedin_scraper import actions
from person import Person
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
load_dotenv()

testdata = {
    "about": "I spend my time balancing my left brain with my right. I think my greatest strength lies in balancing my aptitude for creativity with my technical skills to create products users love. I started out as a software engineer, made an abrupt shift to product management, and have slowly drifted back to somewhere in the middle where I try to bridge the gap between the two domains.\n\nI am passionate about why people do what they do, and believe in making data-driven decisions to create products that solve real problems. I think Steve Jobs had it right when he said we should \"make products we are proud to sell and recommend to our family and friends.\" Today, I am fortunate to be leading an incredible team at The Ashley Group where we do just that for our clients every single day.\n…see more",
    "accomplishments": [],
    "company": "The Ashley Group · Full-time",
    "contacts": [],
    "educations": [
        {
            "degree": "Bachelor’s Degree, Marketing",
            "description": "Secondary coursework in Computer Science",
            "from_date": None,
            "institution_name": "The Ohio State University",
            "linkedin_url": "https://www.linkedin.com/company/3173/",
            "to_date": None
        },
        {
            "degree": "Nanodegree, React",
            "description": "Declarative user interfaces for the web with React, and for iOS and Android with React Native. State management in applications with Redux.",
            "from_date": None,
            "institution_name": "Udacity",
            "linkedin_url": "https://www.linkedin.com/company/2475568/",
            "to_date": None
        },
        {
            "degree": "UX Research & Strategy",
            "description": "4 week course on UX research to learn the in’s and out’s of user centered design and how to create key components of any customer research process.",
            "from_date": None,
            "institution_name": "Designlab",
            "linkedin_url": "https://www.linkedin.com/company/89842/",
            "to_date": None
        },
        {
            "degree": "High School Diploma",
            "description": "",
            "from_date": None,
            "institution_name": "St. Xavier High School",
            "linkedin_url": "https://www.linkedin.com/company/376683/",
            "to_date": None
        }
    ],
    "email": None,
    "experiences": [
        {
            "description": "• Lead cross-functional teams of software engineers, product designers and project managers to build top-tier digital experiences for our clients\n• Work with discipline leads to set new approaches for leveraging existing technology, drive automation and pilot experiments to improve processes, and promote solutions at scale across teams\n• Work with clients to understand critical business objectives and translate them into actionable, measurable plans\n\nTechnologies used:\n- TypeScript, React/React Native, Node.js, Ruby on Rails, SQL, AWS, GCP",
            "duration": "3 yrs 9 mos",
            "from_date": "May 2020",
            "institution_name": "The Ashley Group · Full-time",
            "linkedin_url": "https://www.linkedin.com/company/64942566/",
            "location": "Cincinnati, Ohio, United States",
            "position_title": "Founder",
            "to_date": "Present"
        },
        {
            "description": "• Introduced agile processes for translating marketing requirements into technical roadmaps at Fortune 100 companies\n• Simultaneously managed multiple lines of business for web applications, voice applications and email campaigns\n• Utilized real-time analytics to deliver insights against project KPIs and keep project stakeholders informed\n\nTechnologies used:\n- React, Angular, JavaScript, ES6, Ruby, SASS",
            "duration": "1 yr 1 mo",
            "from_date": "May 2019",
            "institution_name": "BAREFOOT · Full-time",
            "linkedin_url": "https://www.linkedin.com/company/14605/",
            "location": "Cincinnati, Ohio · On-site",
            "position_title": "Product Manager",
            "to_date": "May 2020"
        },
        {
            "description": "• Rebuilt a legacy Flex application with an Angular 8 frontend and Java Spring backend\n• Optimized workflow by introducing Git Flow, pull request guidelines and code linters\n• Distribute application to multiple teams for daily use and document/debug issues\n\nTechnologies used:\n– Angular 8, TypeScript, SASS, HTML, Jenkins",
            "duration": "1 yr 1 mo",
            "from_date": "Apr 2019",
            "institution_name": "Keeneland Association · Contract",
            "linkedin_url": "https://www.linkedin.com/company/699291/",
            "location": "Columbus, Ohio, United States · Remote",
            "position_title": "Software Engineer",
            "to_date": "Apr 2020"
        },
        {
            "description": "• Rebuilt a vanilla JavaScript application with Ionic 4 for iOS and Android\n• Migrated and integrated existing backend services on Firebase Cloud Functions\n• Scoped, planned and documented entire project from beginning to end\n\nTechnologies used:\n– Ionic 4, Firebase Realtime Database ",
            "duration": "3 mos",
            "from_date": "Jan 2019",
            "institution_name": "Poplin · Contract",
            "linkedin_url": "https://www.linkedin.com/company/14842687/",
            "location": "Columbus, Ohio Area · Remote",
            "position_title": "Software Engineer",
            "to_date": "Mar 2019"
        },
        {
            "description": "• Directly managed internal workflow for new agile, web-development projects\n• Created two Angular progressive web applications and integrated Angular Material library\n• Traveled to a client conference to help launch recently completed project\n\nTechnologies used:\n– Angular 7, SASS, Node.js, Firebase Authentication, DynamoDB",
            "duration": "9 mos",
            "from_date": "Apr 2018",
            "institution_name": "Robins & Morton · Contract",
            "linkedin_url": "https://www.linkedin.com/company/65030/",
            "location": "Columbus, Ohio · Remote",
            "position_title": "Software Engineer",
            "to_date": "Dec 2018"
        },
        {
            "description": "• Full-stack web development with modern frameworks such as React and Angular\n• Integrate third-party API’s like Google Cloud Natural Language and Stripe\n• Follow strict agile development standards and document all work through Jira\n\nTechnologies used:\n– Angular, SASS, Node.js, Firebase Authentication, DynamoDB, PostgresSQL",
            "duration": "1 yr 10 mos",
            "from_date": "Aug 2015",
            "institution_name": "Upwork · Contract",
            "linkedin_url": "https://www.linkedin.com/company/4827017/",
            "location": "Columbus, Ohio · Remote",
            "position_title": "Software Engineer",
            "to_date": "May 2017"
        }
    ],
    "interests": [],
    "job_title": "Founder",
    "linkedin_url": "https://www.linkedin.com/in/michaelashley",
    "location": "Fail",
    "name": "Michael Ashley"
}

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

email = os.getenv('LINKEDIN_EMAIL')
password = os.getenv('LINKEDIN_PASSWORD')
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--load-extension={0}".format("./capsolver_extension"))

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


@app.route('/scrape', methods=['POST'])
def scrape():
    data = request.get_json()
    try:
        url = data['profileUrl']
    except:
        response = jsonify({'error': 'No profile URL provided'})
        response.status_code = 400
        return response
    if url == "testdata":
        sleep(5)
        print("Test Data")
        return jsonify(testdata)
    if url == "" or url is None:
        print("400")
        response = jsonify({"Error": "No profile URL provided"})
        response.status_code = 400
        return response
    driver = webdriver.Chrome(options=chrome_options)
    actions.login(driver, email, password)
    person = Person(linkedin_url=url, driver=driver)
    response = person.serialize_person()
    print(response)
    return jsonify(response)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(debug=True, host="0.0.0.0", port=port)
