from crypt import methods
from curses import flash
from urllib import request
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["STATIC_FOLDER"] = "templates/static"
app.config["STATIC_URL_PATH"] = "/static"
app.secret_key = "HelKey"
app.config['UPLOAD_FOLDER'] = 'upload'

VPvotes = {
    'vp1' : 0,
    'vp2' : 0,
    'vp3' : 0
 }
Svotes = {
        'scan1' : 0,
        'scan2' : 0,
        'scan3' : 0
    }

Tvotes = {
        'tcan1' : 0,
        'tcan2' : 0,
        'tcan3' : 0
    }

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
     username = request.form["clg-id"]
     session["user"] = username
     passowrd = request.form["password"]

     element1 = username
     element2 = passowrd
     if auth(element1,element2) == True:
         return redirect(url_for("valid"))
     else:
          Flask("invaid inputs")
          return render_template("login.html")
    return render_template("login.html")


def auth(username, password):
    file = '/Users/adithyarparashar/Desktop/voter.csv'
    element1 = username
    element2 = password
    try:
      df = pd.read_csv(file)
      found1 = False
      found2 = False
      for index, row in df.iterrows():
        for column_name, cell_value in row.items():
            if str(cell_value) == element1:
                found1 = True
            elif str(cell_value) == element2:
                 found2 = True

        if found1 and found2:
            df = df[df.apply(lambda row: (row.astype(str) != element1) & (row.astype(str) != element2), axis=1)]
            df.to_csv(file, index=False)
            return True
            break

      if found1 and found2:
        # Perform operations when both elements are found
        df = df[df.apply(lambda row: (row.astype(str) != element1) & (row.astype(str) != element2), axis=1)]
        df.to_csv(file, index=False)
      else:
        print("invalid")
    except Exception as e:
      print("An error occurred:", str(e))


@app.route("/list")
def flist():
    return render_template("list.html", canNames=canNames, VPvotes=VPvotes, Svotes=Svotes,Tvotes=Tvotes)


@app.route("/valid")
def valid():
    return render_template("VPvote.html", canNames=canNames)

@app.route("/Svalid", methods=['POST','GET'])
def Svalid():
    if request.method == 'POST':
     Vvote = request.form.get("vpCan")
     if Vvote == 'can1':
        VPvotes['vp1']+=1
    elif Vvote == 'can2':
        VPvotes['vp2']+=1
    else:
        VPvotes['vp3']+=1
    return render_template("Svote.html", canNames=canNames)

@app.route("/Tvalid", methods=['POST','GET'])
def Tvalid():
    if request.method == 'POST':
        Svote = request.form.get("Scan")
        if Svote == 'can1':
         Svotes['scan1']+=1
        elif Svote == 'can2':
         Svotes['scan2']+=1
        else:
         Svotes['scan3']+=1
    return render_template("Tvote.html", canNames=canNames)

@app.route("/done", methods=['POST','GET'])
def done():
    if request.method == 'POST':
        Tvote = request.form.get("Tcan")
        if Tvote == 'can1':
         Tvotes['tcan1']+=1
        elif Tvote == 'can2':
         Tvotes['tcan2']+=1
        else:
         Tvotes['tcan3']+=1
    return redirect(url_for("home"))


def great(list):
    count = 0
    large = max(list)
    for num in list:
        if num >= large:
            count += 1
    return count


@app.route("/result")
def result():
    
    VPwinner = max(VPvotes, key=VPvotes.get)
    VPname = max(VPvotes.values())
    if VPwinner in canInfo:
        name1 = canInfo[VPwinner][0]
        img1 = canInfo[VPwinner][1]

    Vtotal = sum(VPvotes.values())
    VPpercent = (VPname/Vtotal)*100

    num1 = list(VPvotes.values())
    vptie = great(num1)
    

    Swinner = max(Svotes, key=Svotes.get)
    Sname = max(Svotes.values())
    if Swinner in canInfo:
        name2 = canInfo[Swinner][0]
        img2 = canInfo[Swinner][1]
    
    Stotal = sum(Svotes.values())
    Spercent = (Sname/Stotal)*100

    num2 = list(Svotes.values())
    stie = great(num2) 
   
    Twinner = max(Tvotes, key=Tvotes.get)
    Tname = max(Tvotes.values())
    if Twinner in canInfo:
        name3 = canInfo[Twinner][0] 
        img3 = canInfo[Twinner][1]

    Ttotal = sum(Tvotes.values())
    Tpercent = (Tname/Ttotal)*100

    num3 = list(Tvotes.values())
    ttie = great(num3)

    result = {
        'vp': [name1, img1],
        'sac': [name2,img2],
        'tre': [name3, img3]
    }
    
    return render_template("res.html", result=result, 
    VPpercent=VPpercent, Spercent=Spercent, Tpercent=Tpercent,
    VPname=VPname, Sname=Sname, Tname=Tname,
    vptie=vptie,stie=stie,ttie=ttie)


@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        admin_user = request.form["username"]
        session["admin_name"] = admin_user
        admin_pass = request.form["password"]
        if admin_user == "aaa" and admin_pass == "000":
             return redirect(url_for("getinfo"))
        else:
            return "incorrect creditionals try again"
    return render_template("admin.html")
    
@app.route("/getinfo", methods=['GET','POST'])
def getinfo():
    if "admin_name" in session:
     if request.method == 'POST':
        VPcan1 = request.form["VPcan1"]
        vcan1 = request.files["vp1"]
        vp1 = 'vp1.jpg'
        vcan1.save(os.path.join(app.config['UPLOAD_FOLDER'],vp1))
        VPcan2 = request.form["VPcan2"]
        vcan2 = request.files["vp2"]
        vp2 = 'vp2.jpg'
        vcan2.save(os.path.join(app.config['UPLOAD_FOLDER'],vp2))
        VPcan3 = request.form["VPcan3"]
        vcan3 = request.files["vp3"]
        vp3 = 'vp3.jpg'
        vcan3.save(os.path.join(app.config['UPLOAD_FOLDER'],vp3))
        Scan1 = request.form["Scan1"]
        scan1 = request.files["s1"]
        s1 = 's1.jpg'
        scan1.save(os.path.join(app.config['UPLOAD_FOLDER'],s1))
        Scan2 = request.form["Scan2"]
        scan2 = request.files["s2"]
        s2 = 's2.jpg'
        scan2.save(os.path.join(app.config['UPLOAD_FOLDER'],s2))
        Scan3 = request.form["Scan3"]
        scan3 = request.files["s3"]
        s3 = 's3.jpg'
        scan3.save(os.path.join(app.config['UPLOAD_FOLDER'],s3))
        Tcan1 = request.form["Tcan1"]
        tcan1 = request.files["t1"]
        t1 = 't1.jpg'
        tcan1.save(os.path.join(app.config['UPLOAD_FOLDER'],t1))
        Tcan2 = request.form["Tcan2"]
        tcan2 = request.files["t2"]
        t2 = 't2.jpg'
        tcan2.save(os.path.join(app.config['UPLOAD_FOLDER'],t2))
        Tcan3 = request.form["Tcan3"]
        tcan3 = request.files["t3"]
        t3 = 't3.jpg'
        tcan3.save(os.path.join(app.config['UPLOAD_FOLDER'],t3))
        global canNames
        canNames = {
            'vp1' : VPcan1,
            'vp2' : VPcan2,
            'vp3' : VPcan3,
            'scan1' : Scan1,
            'scan2' : Scan2,
            'scan3' : Scan3,
            'tcan1' : Tcan1,
            'tcan2' : Tcan2,
            'tcan3' : Tcan3
        }
        global canInfo
        canInfo = {
            'vp1': [VPcan1, vp1],
            'vp2': [VPcan2, vp2],
            'vp3': [VPcan3, vp3],
            'scan1': [Scan1,s1],
            'scan2': [Scan2,s2],
            'scan3': [Scan3, s3],
            'tcan1': [Tcan1, t1],
            'tcan2': [Tcan2, t2],
            'tcan3': [Tcan3, t3]
        }
        return render_template("output.html", canNames=canNames)
     return render_template("admin_info.html")

@app.route("/serve/<filename>", methods=['GET'])
def serve(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


if __name__ == "__main__":
    app.run(debug=True)