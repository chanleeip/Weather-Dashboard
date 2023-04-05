import master
from flask import Flask, render_template,jsonify,request
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
        current_temp = master.current_temperature(latitude, longitude)
        graph = master.temperature_forecasting(latitude, longitude)
        temp_forcasting = base64.b64encode(graph.getvalue()).decode('utf-8')
    return jsonify({'status':'success','curr_temp':current_temp,'temp_forcasting':temp_forcasting})

if __name__=="__main__":
    app.run(debug=True)