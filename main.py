from flask import Flask,render_template,request
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import pandas as pd
import os
app=Flask(__name__)
app.secret_key='Reetika'
class Coffee:
 def __init__(self):
        self.name=None
        self.location=None
        self.opentime=None
        self.closetime=None
        self.rating=None
        self.wifistrength=None
class addcoffee(FlaskForm):
 name=StringField(label="Name of Coffee Shop",validators=[DataRequired()])
 location=StringField(label="Location of Coffee Shop",validators=[DataRequired()])
 opentime=StringField(label="Opening Time of Coffee Shop",validators=[DataRequired()])
 closetime=StringField(label="Closing Time of Coffee Shop",validators=[DataRequired()])
 rating=StringField(label="Rating of Coffee Shop",validators=[DataRequired()])
 wifistrength=StringField(label="WIFI Strength of Coffee Shop",validators=[DataRequired()])
 submit=SubmitField('ADD')
bootstrap=Bootstrap5(app)
@app.route('/')
def home():
 return render_template("index.html")
@app.route('/add_coffee_shops',methods=['Get','Post']) 
def add():
 form=addcoffee()
 if request.method == 'POST':
       
    if form.validate_on_submit():
        coff=Coffee()
        coff.name=form.name.data
        coff.location=form.location.data
        coff.opentime=form.opentime.data
        coff.closetime=form.closetime.data
        coff.rating=form.rating.data
        coff.wifistrength=form.wifistrength.data
        
        file_path = 'static/coffee.csv'
        
        # Check if the file exists and is not empty
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                existing_df = pd.read_csv(file_path)
                # Check if the DataFrame has the expected columns
                if existing_df.empty:
                    existing_df = pd.DataFrame(columns=['NAME', 'LOCATION', 'OPENING_TIME', 'CLOSING_TIME', 'RATING', 'WIFI_STRENGTH'])
            except pd.errors.EmptyDataError:
                # Handle the case where the file is empty but exists
                existing_df = pd.DataFrame(columns=['NAME', 'LOCATION', 'OPENING_TIME', 'CLOSING_TIME', 'RATING', 'WIFI_STRENGTH'])
        else:
            # Create a new DataFrame with columns if file does not exist or is empty
            columns1 = ['NAME', 'LOCATION', 'OPENING_TIME', 'CLOSING_TIME', 'RATING', 'WIFI_STRENGTH']
            existing_df = pd.DataFrame(columns=columns1)
        
        # Prepare new data
        dict={'NAME':coff.name,'LOCATION':coff.location,'OPENING_TIME':coff.opentime,'CLOSING_TIME':coff.closetime,'RATING':coff.rating,'WIFI_STRENGTH':coff.wifistrength}
          
        
        # Create a DataFrame for the new row
        df = pd.DataFrame([dict])
        
        # Write the new row to the CSV file
        # Use 'mode=a' to append; write headers only if the file was initially empty
        if existing_df.empty:
            print("File is empty or newly created")
            df.to_csv(file_path, mode='w', index=False, header=True)
        else:
            print("File is not empty")
            df.to_csv(file_path, mode='a', index=False, header=False)
        
        # Render the template or redirect
        return render_template('index.html')
        # coff=coffee()
        # coff.name=form.name.data
        # coff.location=form.location.data
        # coff.opentime=form.opentime.data
        # coff.closetime=form.closetime.data
        # coff.rating=form.rating.data
        # coff.wifistrength=form.wifistrength.data
        
        # try:
        #  existing_df=pandas.read_csv('coffee.csv')
        # except FileNotFoundError:
        #   columns1=['index','NAME', 'LOCATION', 'OPENING_TIME', 'CLOSING_TIME', 'RATING', 'WIFI_STRENGTH']
        #   existing_df=pandas.DataFrame(columns=columns1)
        # max_index=existing_df.index.max() 
        # if existing_df.empty:
        #   max_index=-1
        #   dict={'index':max_index+1,'NAME':coff.name,'LOCATION':coff.location,'OPENING_TIME':coff.opentime,'CLOSING_TIME':coff.closetime,'RATING':coff.rating,'WIFI_STRENGTH':coff.wifistrength}
          
        #   print("not empty")  
        #   df=pandas.DataFrame([dict])
        #   df.to_csv('static/coffee.csv',mode='a',index=False,header=True)
        # else:
          
        #   dict={'index':max_index+1,'NAME':coff.name,'LOCATION':coff.location,'OPENING_TIME':coff.opentime,'CLOSING_TIME':coff.closetime,'RATING':coff.rating,'WIFI_STRENGTH':coff.wifistrength}
        #   print("empty")  
        #   df=pandas.DataFrame([dict])
        #   df.to_csv('static/coffee.csv',mode='a',index=False,header=False)
          
        
        # return render_template('index.html')  # Adjust based on your app's logic
    
    
 return render_template('coffee_shop_list.html',form=form)
@app.route("/seecoffee",methods=['Get'])
def seecoffee1():
        try: 
          data=pd.read_csv('static/coffee.csv')
          print("went into try")
        except FileNotFoundError and pd.errors.EmptyDataError:
         columns1=['NAME', 'LOCATION', 'OPENING_TIME', 'CLOSING_TIME', 'RATING', 'WIFI_STRENGTH'] 
         data=pd.DataFrame(columns=columns1)
        
        
        
        return render_template("show_coffee.html",data_csv=data.to_dict(orient='records'))
if __name__==('__main__'):
 app.run(debug=True)