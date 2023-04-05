import master
from flask import Flask,redirect,render_template,jsonify,request
import base64

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def home():
    return render_template('primary.html')

@app.route('/send_coordinates',methods= ['GET','POST'])
def send_coordinates():
    if request.method == 'POST':
        latitude=request.form.get('latitude')
        longitude=request.form.get('longitude')
        current_temp = master.current_temperature(latitude,longitude)
        current_weather=master.find_current_weather_status(latitude,longitude)
        min_max_temp=master.find_current_and_today_min_max_temperature(latitude,longitude)
        curr_wind_info=master.current_wind_info(latitude,longitude)
        rain_or_not=master.is_it_going_to_rain_tomorrow(latitude,longitude)
        sunrise_sunset=master.sunrise_sunset(latitude,longitude)
    return jsonify({'status':'success','curr_temp':current_temp,'temp_forcasting':temp_forcasting,'cur_weather':current_weather})

if __name__=="__main__":
    app.run(debug=True)