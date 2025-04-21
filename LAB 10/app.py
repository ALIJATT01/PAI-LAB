from flask import Flask, render_template, request, jsonify
import json
import re
session_context = {
    'last_level': None
}


app = Flask(__name__)

# Load admission data
with open('admission_data.json', 'r') as file:
    data = json.load(file)

# Chatbot logic (same as above, included here for completeness)
def get_response(user_input):
    user_input = user_input.lower().strip()

    # Track level of study if mentioned
    if 'undergraduate' in user_input:
        session_context['last_level'] = 'undergraduate'
    elif 'postgraduate' in user_input:
        session_context['last_level'] = 'postgraduate'

    level = session_context.get('last_level')

    # Eligibility
    if re.search(r'eligibility|requirements', user_input):
        if level:
            return data['admission_info'][level]['eligibility']
        else:
            return "Please specify undergraduate or postgraduate eligibility."

    # Documents
    elif re.search(r'documents|document', user_input):
        if level:
            return ", ".join(data['admission_info'][level]['documents'])
        else:
            return "Please specify undergraduate or postgraduate documents."

    # Deadlines
    elif re.search(r'deadline|dates', user_input):
        if level:
            return data['admission_info'][level]['deadlines']
        else:
            return "Please specify undergraduate or postgraduate deadlines."

    # Fees
    elif re.search(r'fees|cost|tuition', user_input):
        if level:
            return data['admission_info'][level]['fees']
        else:
            return "Please specify undergraduate or postgraduate fees."

    # Programs
    elif re.search(r'programs|courses', user_input):
        if level:
            return ", ".join(data['admission_info'][level]['programs'])
        else:
            return "Please specify undergraduate or postgraduate programs."

    # Contact info
    elif re.search(r'contact|email|phone', user_input):
        return f"Email: {data['admission_info']['contact']['email']}\nPhone: {data['admission_info']['contact']['phone']}\nOffice Hours: {data['admission_info']['contact']['office_hours']}"

    # If they just type "undergraduate" or "postgraduate"
    elif user_input in ['undergraduate', 'postgraduate']:
        session_context['last_level'] = user_input
        return f"You selected {user_input.title()}. Please ask about eligibility, documents, deadlines, programs, or fees."

    else:
        return "Sorry, I didn't understand your question. Please ask about eligibility, documents, deadlines, fees, programs, or contact details."


# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chatbot messages
@app.route('/get_response', methods=['POST'])
def chatbot_response():
    user_input = request.form.get('message', '')  # Safely get the message
    print(f"User input received: {user_input}")  # Debugging
    response = get_response(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)