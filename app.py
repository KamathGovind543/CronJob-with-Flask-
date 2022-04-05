import requests
from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_mail import Mail
from flask_mail import Message
from datetime import datetime
from flask_apscheduler import APScheduler


app = Flask(__name__)
scheduler = APScheduler()
scheduler.api_enabled = True



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] =''

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = '465',
    MAIL_USE_SSL = 'True',
    MAIL_USERNAME =  'Add user gmail',
    MAIL_PASSWORD =  'add Password ',
    MAIL_DEFAULT_SENDER = 'Add Default user gamil for sending mail'
)

mail = Mail(app)

def get_weather_data(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=(add your api id here)'
    r = requests.get(url).json()
    return r

@app.route('/')
def index():
    return "Welcome to the Flask_APScheduler"

def send_mail():
    with app.app_context():

        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        weather_data = []
        
        r = get_weather_data("Hyderabad")
        

        weather = {
            'city' : "Hyderabad",
            'temparature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
            
        } 
        

        weather_data.append(weather)

        msg = Message('Weather Info ',recipients=['any mail'])
        body_msg = render_template('email.html',weather_data=weather_data , dt_string = dt_string)
        msg.html = (body_msg)
        mail.send(msg)
        

        
if __name__=="__main__":

    scheduler.add_job(id ='Scheduled task', func = send_mail, trigger = 'cron', minute = "36", hour="13" ,day="*", month = "*" ,week = "*")
    scheduler.start()
    app.run(debug=True)  

