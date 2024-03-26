
from flask import Flask,render_template,request
from flask_mail import Mail,Message
from flask import Flask, request, jsonify
from flask import render_template
from flask_cors import CORS, cross_origin
import pickle
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from flask_mail import Mail
from flask_mail import Message
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher_suite = Fernet(key)
# nltk.download()


app=Flask(__name__)


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='discoverjohnsamuel11@gmail.com'
app.config['MAIL_PASSWORD']='imdmhafjpisacoaz'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

mail=Mail(app)


@app.route('/')
def index():

    return render_template("index1.html")
def clean_text(a):
    text = re.sub('[^a-zA-Z0-9]', ' ', a)
    text = text.lower()
    text = nltk.word_tokenize(text)
    text = [WordNetLemmatizer().lemmatize(word) for word in text if word not in (stopwords.words('english'))]
    text = ' '.join(text)
    return text

@app.route('/base',methods=['GET','POST'])
def base():
    if request.method=="POST":

        email=request.form["email"]
        subject=request.form["subject"]
        msg=request.form["message"]
        dict = {"a": "#", "b": "#","c": "#", "d": "#","e": "#","f":"#","g": "#", "h": "#","i": "#", "j": "#","k": "#","l":"#","m": "#", "n": "#","o": "#", "p": "#","q": "#","r":"#","s": "#", "t": "#","u": "#", "v": "#","w": "#","x":"#","y": "#", "z": "#","1": "#", "2": "#","3": "#","4":"#","5": "#", "6": "#","7": "#","8":"#","9": "#", "0": "#"}
        num = msg[::-1]
        for i in dict:
            num = num.replace(i, dict[i])
        encode=f"{num}"
        
        #encode=cipher_suite.encrypt(msg.encode())
        #msg.encode('utf-16', 'surrogatepass')
        print(encode,"hello")
        messag=Message(subject,sender="HARI",recipients=[email])
        spam=Message(subject,sender="hari",recipients=[email])
        spam.body=encode
        messag.body=msg
        message = request.form.get('message')
    with open('../Model/spamClassifier.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('../Model/count_vect', 'rb') as f:
        vectorizer = pickle.load(f)
    if model.predict(vectorizer.transform([clean_text(message)])):
        a='THIS IS A BULLYING COMMENT '
        mail.send(spam)
        return render_template('index1.html',a=a)
        
    else:
        mail.send(messag)
        b='NON BULLYING COMMENT'
        
        return render_template('index1.html',b=b)
         
        

if __name__ == "__main__":

    app.run(debug=True)