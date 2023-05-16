from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# process the csv file

df = pd.read_csv("LiCONiC Data 001.csv")
df['Size_Info'] = df['Product Model'].map(lambda x: x.split('-')[0])
df['Size'] = "unknown Size"
for i, row in df.iterrows():
    row['Size'] = int("".join(filter(str.isdigit, row['Size_Info'])))
 
df['Info'] = df['Product Model'].map(lambda x: x.split('-')[1])
df['Climate'] = "unknown climate"
df['Placement'] = "unknown placement"
df['Temp Low'] = "1000"
df['Temp High'] = "1000"
df['Humidity Low'] = "1000"
df['Humidity High'] = "1000"

for i, row in df.iterrows():
    if("IC" in row['Info']):
        row['Climate'] = "IC"
        row['Temp Low'] = 33
        row['Temp High'] = 50
        row['Humidity Low'] = 0
        row['Humidity High'] = 95
    elif("HC" in row['Info']):
        row['Climate'] = "HC"
        row['Temp Low'] = 4
        row['Temp High'] = 25
        row['Humidity Low'] = 0
        row['Humidity High'] = 90
    elif("DC2" in row['Info']):
        row['Climate'] = "DC2"
        row['Temp Low'] = 4
        row['Temp High'] = 25
        row['Humidity Low'] = 4
        row['Humidity High'] = 50
    elif("HR" in row['Info']):
        row['Climate'] = "HR"
        row['Temp Low'] = 4
        row['Temp High'] = 50
        row['Humidity Low'] = 90
        row['Humidity High'] = 95
    elif("DR2" in row['Info']):
        row['Climate'] = "DR2"
        row['Temp Low'] = 4
        row['Temp High'] = 50
        row['Humidity Low'] = 2
        row['Humidity High'] = 50
    elif("AR" in row['Info']):
        row['Climate'] = "AR"
        row['Temp Low'] = 4
        row['Temp High'] = 50
        row['Humidity Low'] = 2
        row['Humidity High'] = 50
    elif("DF" in row['Info']):
        row['Climate'] = "DF"
        row['Temp Low'] = -20
        row['Temp High'] = 0
        row['Humidity Low'] = 10
        row['Humidity High'] = 95
    elif("NC" in row['Info']): 
        # no climate, use the range of room temperature
        row['Climate'] = "NC"
        row['Temp Low'] = -10
        row['Temp High'] = 40
        row['Humidity Low'] = 0
        row['Humidity High'] = 100

for i, row in df.iterrows():
    if("MISA" in row['Info']):
        row['Placement'] = "MISA"
    elif("MIBT" in row['Info']):
        row['Placement'] = "MIBT"
    elif("SA" in row['Info']):
        row['Placement'] = "SA"
    elif("BT" in row['Info']):
        row['Placement'] = "BT"
    elif("IT" in row['Info']):
        row['Placement'] = "IT"

df['Temp Low'] = df['Temp Low'].astype(int)
df['Temp High'] = df['Temp High'].astype(int)
df['Humidity Low'] = df['Humidity Low'].astype(int)
df['Humidity High'] = df['Humidity High'].astype(int)

# main function of choosing the appropriate models

def choose(number, temp_low, temp_high, humd_low, humd_high, place):
    selected = []
    for i, row in df.iterrows():
        p = place # First filtered by the Placement 
        if(p==row['Placement']): # Then look at the size, and climate
            if(number<=row['Size'] and 
               temp_low>=row['Temp Low'] and 
               temp_high<=row['Temp High'] and 
               humd_low>=row['Humidity Low'] and humd_high<=row['Humidity High']):
                machine = row['Product Model'] + " - " + row['Code']
                selected.append(machine)
    return selected

# endpoints

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    number = 1000
    place = "not selected"
    if request.method == 'POST':
        number = request.form.get('number', type=int)
        temp_low = request.form.get('temp_low', type=int)
        temp_high = request.form.get('temp_high', type=int)
        humd_low = request.form.get('humd_low', type=int)
        humd_high = request.form.get('humd_high', type=int)
        place = request.form.get('place', type=str)

        machine_list = choose(number, temp_low, temp_high, humd_low, humd_high, place)

    return render_template("result.html", machines = machine_list)


