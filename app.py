from flask import Flask, render_template ,request,flash,Response
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from werkzeug.utils import secure_filename
import wget
import cv2
import os
import calendar
import time
import getpass
import platform
from compression import compression
from effects import oreo,mercury,alchemy,wacko,unstable,ore,contour,snicko,indus,spectra,molecule,lynn,download
from edit import brightness,contrast,blur,resize,denoise,rotate,sharp,downloads
import mysql.connector
app = Flask(__name__)
app.config['SECRET_KEY']='mySnapLab'

UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response





@app.route('/')
@app.route('/Home1')
def Home1():
	return render_template('Home1.html')


@app.route('/NewUser')
def NewUser():
	return render_template('NewUser.html')

@app.route('/UserLogin')
def UserLogin():
	return render_template('UserLogin.html')

@app.route("/RNewUser", methods=['GET', 'POST'])
def RNewUser():
    if request.method == 'POST':

        name1 = request.form['name']
        gender1 = request.form['gender']
        Age = request.form['age']
        email = request.form['email']
        address = request.form['address']
        pnumber = request.form['phone']
        uname = request.form['uname']
        password = request.form['psw']


        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1photodb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('" + name1 + "','" + gender1 + "','" + Age + "','" + email + "','" + pnumber + "','" + address + "','" + uname + "','" + password + "')")
        conn.commit()
        conn.close()
        # return 'file register successfully'




    return render_template('userlogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    error = None
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['password']
        session['uname'] = request.form['uname']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='1photodb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where UserName='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()

        if data is None:

            data1 = 'Username or Password is wrong'
            return render_template('goback.html', data=data1)



        else:
            conn1 = mysql.connector.connect(user='root', password='', host='localhost', database='1photodb')

            cur1 = conn1.cursor()
            cur1.execute("SELECT * FROM regtb where username='"+ session['uname'] +"' ")
            data = cur1.fetchall()
            # return 'file register successfully'
            # return render_template('order.html', data=data)


            return render_template('home.html',data=data)
@app.route('/home')
def home():
	return render_template('home.html')

############################################################################################edit page
edit_img=''
edited=''
brightness_value='0'
contrast_value='1'
sharp_value=''
resize_value=''
rotate_value=''
denoise_value=''
blur_value='0'
@app.route('/edit',methods=['GET','POST'])
def edit():
    if request.method=='POST':
       global edit_img
       global edited
       global brightness_value
       global contrast_value
       global sharp_value
       global resize_value
       global rotate_value
       global denoise_value
       global blur_value
       if request.form['button']=='Upload' and request.form['path']!='' and  request.files['local_file'].filename=='':
           path = request.form['path']
           a = path.split('/')
           previous = os.getcwd()
           edit_img=previous+'/static/images/trash/'+a[len(a)-1]
           if os.path.isfile(previous+'/static/images/trash/'+a[len(a)-1]):
              return render_template('edit.html',image_filename='../static/images/trash/'+a[len(a)-1],brightness_value=brightness_value,contrast_value=contrast_value,blur_value=blur_value,sharp_value=sharp_value,denoise_value=denoise_value,rotate_value=rotate_value,resize_value=resize_value)
           folder = previous +'/static/images/trash/'
           os.chdir(folder)
           image_filename = wget.download(path)
           os.chdir(previous)
           return render_template('edit.html',image_filename='../static/images/trash/'+image_filename,brightness_value=brightness_value,contrast_value=contrast_value,blur_value=blur_value,sharp_value=sharp_value,denoise_value=denoise_value,rotate_value=rotate_value,resize_value=resize_value)

       elif request.form['button']=='Upload' and request.form['path']=='' and  request.files['local_file'].filename!='':
            f = request.files['local_file']
            previous = os.getcwd()
            edit_img=previous+'/static/images/trash/'+f.filename
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            f.save(secure_filename(f.filename))
            os.chdir(previous)
            return render_template('edit.html',image_filename='../static/images/trash/'+f.filename,brightness_value=brightness_value,contrast_value=contrast_value,blur_value=blur_value,sharp_value=sharp_value,denoise_value=denoise_value,rotate_value=rotate_value,resize_value=resize_value)
     
       elif request.form['button']=='Apply' and edit_img!='':
            brightness_value = request.form['brightness']
            contrast_value = request.form['Contrast']
            sharp_value = request.form['type']
            resize_value = request.form['type2']
            rotate_value = request.form['type1']
            denoise_value = request.form['type3']
            blur_value = request.form['Blur']
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            if edit_img.count('jpeg')>0 or edit_img.count("jpg")>0:
                edited=folder+'edited.jpg'
            elif edit_img.count('png')>0:
                 edited=folder+'edited.png'
            os.chdir(folder)
            if brightness_value:
               brightness(edit_img,int(brightness_value))
            if contrast_value:
               contrast(edited,float(contrast_value))
            if sharp_value!='none':
               sharp(edited,sharp_value)
            if resize_value!='none':
               resize(edited,resize_value)
            if rotate_value!='none': 
               rotate(edited,rotate_value)
            if denoise_value!='none':
               denoise(edited,denoise_value)
            if blur_value:
               blur(edited,int(blur_value))      
            os.chdir(previous)           
 
            if edit_img.count('jpeg')>0 or edit_img.count("jpg")>0:
                return render_template('edit.html',image_filename='../static/images/trash/edited.jpg',brightness_value=brightness_value,contrast_value=contrast_value,blur_value=blur_value,sharp_value=sharp_value,denoise_value=denoise_value,rotate_value=rotate_value,resize_value=resize_value)
            elif edit_img.count('png')>0:
                return render_template('edit.html',image_filename='../static/images/trash/edited.png',brightness_value=brightness_value,contrast_value=contrast_value,blur_value=blur_value,sharp_value=sharp_value,denoise_value=denoise_value,rotate_value=rotate_value,resize_value=resize_value)
            else:
               flash("Oops Something went wrong !")
               return render_template('edit.html',brightness_value=brightness_value,contrast_value=contrast_value,blur_value=blur_value,sharp_value=sharp_value,denoise_value=denoise_value,rotate_value=rotate_value,resize_value=resize_value)

       elif request.form['button']=='Download' and edited!='':
            downloads(edited)
            edit_img=''
            edited=''
            brightness_value='0'
            contrast_value='1'
            sharp_value=''
            resize_value=''
            rotate_value=''
            denoise_value=''
            blur_value='0'
            flash("Successfully Downloaded! Image available in Downloads")
            return render_template('edit.html',brightness_value=brightness_value,contrast_value=contrast_value,blur_value=blur_value,sharp_value=sharp_value,denoise_value=denoise_value,rotate_value=rotate_value,resize_value=resize_value)
       else:
            edit_img=''
            edited=''
            brightness_value='0'
            contrast_value='1'
            sharp_value=''
            resize_value=''
            rotate_value=''
            denoise_value=''
            blur_value='0'
            flash("Oops Something went wrong !")
            return render_template('edit.html',brightness_value=brightness_value,contrast_value=contrast_value,blur_value=blur_value,sharp_value=sharp_value,denoise_value=denoise_value,rotate_value=rotate_value,resize_value=resize_value)

    return render_template('edit.html',brightness_value=brightness_value,contrast_value=contrast_value,blur_value=blur_value,sharp_value=sharp_value,denoise_value=denoise_value,rotate_value=rotate_value,resize_value=resize_value)



###########################################################################################compress page
com_img=''
@app.route('/compression',methods=['GET','POST'])                        
def compress():        
    if request.method=='POST':
       global com_img
       if request.form['button']=='Upload' and request.form['path']!='' and  request.files['local_file'].filename=='':
           path = request.form['path']
           a = path.split('/')
           previous = os.getcwd()
           com_img=previous+'/static/images/trash/'+a[len(a)-1]
           if os.path.isfile(previous+'/static/images/trash/'+a[len(a)-1]):
              return render_template('compression.html',image_filename='../static/images/trash/'+a[len(a)-1])
           folder = previous +'/static/images/trash/'
           os.chdir(folder)
           image_filename = wget.download(path)
           os.chdir(previous)
           return render_template('compression.html',image_filename='../static/images/trash/'+image_filename)

       elif request.form['button']=='Upload' and request.form['path']=='' and  request.files['local_file'].filename!='':
            typ = request.form['type']
            f = request.files['local_file']
            previous = os.getcwd()
            com_img=previous+'/static/images/trash/'+f.filename
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            f.save(secure_filename(f.filename))
            os.chdir(previous)
            return render_template('compression.html',image_filename='../static/images/trash/'+f.filename)

       elif request.form['button']=='Compress' and com_img!='':
           typ = request.form['type']
           compression(com_img,typ)
           com_img=''
           flash("Successfully compressed! Compressed Image available in Downloads.")
           return render_template('compression.html')

       else:
            com_img=''
            flash("Oops Something went wrong !")
            return render_template('compression.html')
    return render_template('compression.html')



#################################################################################################effects page
eff_img=''
effected=''
@app.route('/effects',methods=['GET','POST'])
def effects():
    if request.method=='POST':
       print("Entered Post")
       global eff_img
       global effected
       if request.form['button']=='Upload' and request.form['path']!='' and  request.files['local_file'].filename=='':
           path = request.form['path']
           a = path.split('/')
           previous = os.getcwd()
           eff_img=previous+'/static/images/trash/'+a[len(a)-1]
           if os.path.isfile(previous+'/static/images/trash/'+a[len(a)-1]):
              return render_template('effects.html',image_filename='../static/images/trash/'+a[len(a)-1])
           folder = previous +'/static/images/trash/'
           os.chdir(folder)
           image_filename = wget.download(path)
           os.chdir(previous)
           return render_template('effects.html',image_filename='../static/images/trash/'+image_filename)

       elif request.form['button']=='Upload' and request.form['path']=='' and  request.files['local_file'].filename!='':
            f = request.files['local_file']
            previous = os.getcwd()
            eff_img=previous+'/static/images/trash/'+f.filename
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            f.save(secure_filename(f.filename))
            os.chdir(previous)
            return render_template('effects.html',image_filename='../static/images/trash/'+f.filename)

       elif request.form['button']=='Download' and effected!='':
            download(effected)
            effected=""
            eff_img=""
            flash("Successfully Downloaded! Image available in Downloads")
            return render_template('effects.html')
                        
       elif request.form['button']=='Oreo' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            oreo(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html')
       
       elif request.form['button']=='Mercury' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            mercury(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html')

       elif request.form['button']=='Alchemy' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            alchemy(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html')
  
       elif request.form['button']=='Wacko' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            wacko(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html')

       elif request.form['button']=='Unstable' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            unstable(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html')

       elif request.form['button']=='Ore' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            ore(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html')
      
       elif request.form['button']=='Contour' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            contour(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html')   
     
       elif request.form['button']=='Snicko' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            snicko(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html') 

       elif request.form['button']=='Indus' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            indus(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html')
   
       elif request.form['button']=='Spectra' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            spectra(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html')

       elif request.form['button']=='Molecule' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            molecule(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html')
        
       
       elif request.form['button']=='Lynn' and eff_img!='':
            previous = os.getcwd()
            folder = previous +'/static/images/trash/'
            os.chdir(folder)
            lynn(eff_img)
            os.chdir(previous)
            if eff_img.count('jpeg')>0 or eff_img.count("jpg")>0:
                effected=folder+'intermediate.jpg'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.jpg')
            elif eff_img.count('png')>0:
                effected=folder+'intermediate.png'
                return render_template('effects.html',image_filename='../static/images/trash/intermediate.png')
            else:
                return render_template('effects.html')

       else:
           eff_img=''
           effected=''
           flash("Oops Something went wrong !")
           return render_template('effects.html')

    return render_template('effects.html')

############################################################################################filters page
cap =''
value=0
filter_img=''
flag=False
def stream():
    global cap
    cap=cv2.VideoCapture(0)
    while True:
        _,frame = cap.read()
        imgencode=cv2.imencode('.jpg',frame)[1]
        strinData = imgencode.tostring()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+strinData+b'\r\n')

def stop():
    global cap
    if cap.isOpened():
        cap.release()

   


###############################################################################################main function
if __name__ == '__main__':
	app.run(debug=True,port=8080)
