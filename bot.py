__author__ = 'Nazeer'

from flask import Flask, render_template, request, redirect
from AI_Class_and_Object_Implementation import Email_AI
from duckling_simplified import Parse_date_duckling
from memory import memory, update_report_id

app = Flask(__name__)

ai = Email_AI()
ai.fit_classifier()


@app.route('/')
def my_form():
    return render_template('test.html')

@app.route('/clarification')
def my_clarification():
    return 'For Which Date You are Looking for?'

@app.route('/get')
def my_form_post():
    Report_ID = 0
    userText = request.args.get('msg')

    if userText.lower() == 'hi' or userText.lower() == 'hello':
        return 'Hi There.'
    if userText.lower() == 'how are you':
        return "I'm Good, Thanks for Asking"
    if userText.lower() == 'are you human':
        return "No, I am a Chat Bot, Your Personal Sales Assistant :)"
    if 'bye' in userText.lower():
        return "Bye, Thank You."
    grain, date, end_date, date_string = Parse_date_duckling(userText)

    if Report_ID == 0 and date is not None:
        try:
            id = str(memory())
            if int(id) != 0:
                update_report_id(0)
                return 'Report Id:' + id
        except:
            return 'Error'

    Report_ID, self_flag, date1, end_date1, ai_input_string, confidence = ai.user_input(userText)

    if int(confidence) < 70.0:
        return "I Can't Answer This Query."
    try:
        if date is not None:
            date = str(date).split('T')[0]
    except:
        pass
    if date is None or date == 'None':
        # return 'For Which Date You are Looking for?'
        update_report_id(Report_ID)
        return redirect('/clarification')
    # return ' Report Id: '+str(Report_ID)+' and Date: '+str(date)
    return ' Report Id: ' + str(Report_ID)


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 3000)