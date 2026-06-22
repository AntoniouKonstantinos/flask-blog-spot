from flask import Flask, render_template, request
import requests
from post import Post
import os
from dotenv import load_dotenv
import smtplib

load_dotenv(".env")

URL = "https://api.npoint.io/8c4a296e62dd1d4ce277"
MY_EMAIL = os.getenv("EMAIL")
MY_PASSWORD = os.getenv("PASSWORD")

posts = requests.get(URL).json()
post_objects = []
for post in posts:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"], post["date"], post["author"], post["image"])
    post_objects.append(post_obj)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", posts=post_objects)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return render_template("post.html", current=post_objects[post_id-1])

@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route('/contact', methods=['POST', 'GET'])
def contact_page():
    if request.method == 'POST':
        requester_name = request.form['name']
        requester_email = request.form['email']
        requester_phone = request.form['phone']
        requester_message = request.form['message']
        send_email(requester_name, requester_email, requester_phone, requester_message)
        return render_template("contact.html", flag=True)
    return render_template("contact.html", flag=False)

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL, MY_PASSWORD)
        connection.sendmail(MY_EMAIL, MY_EMAIL, email_message)


if __name__ == "__main__":
    app.run(debug=True)
