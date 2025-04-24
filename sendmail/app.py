from flask import Flask, render_template, url_for, redirect, request, flash
from email_validator import validate_email,EmailNotValidError
import logging
import os
from flask_mail import Mail, Message



app = Flask(__name__) # __name__ => __main__
app.config["SECRET_KEY"]= "asdjh21321ADzds23a"
app.logger.setLevel(logging.DEBUG)
app.logger.debug("debug")

#app.config에 이메일 정보 입력
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")

mail = Mail(app)

@app.route("/")
def index():
	return "메일 보내기 미니프로젝트"

@app.route("/contact")
def contact():
	return render_template("contact.html")

@app.route("/contact/complete" , methods=["GET","POST"])
def contact_complete():
	if request.method == "POST":
		name = request.form["name"]
		email = request.form["email"]
		message = request.form["message"]

		#입력된 정보의 유효성 검증
		vaild = True

		if not name: 
			flash("사용자명은 필수로 입력해주세요")
			vaild = False
		
		if not  email:
			flash("이메일 양식을 맞춰주세요")
			vaild = False

		try:
			validate_email(email)
		except:
			flash("이메일 양식을 맞춰주세요!!!!!!!!!!!!!!!!!!!")
			vaild = False
		
		if not message:
			flash("문의 내용을 필수로 입력해주세요")
			vaild = False
		
		if not vaild: #valid  == False not 만나서 ture
			return redirect(url_for("contact"))
		
		flash("나문희")

		send_email(email,"문희는 감자가 먹구시픈뎅,,","contact_mail", user_name = name , description = message)


		return redirect(url_for("contact_complete"))
	return render_template("contact_complete.html")
	

def send_email(to, subject, template, **kwargs):
	msg = Message(subject, recipients=[to])
	msg.body = render_template(template + ".txt",**kwargs)
	msg.html = render_template(template + ".txt",**kwargs)
	msg.charset = 'utf-8'
	mail.send(msg)


if __name__ == "__main__":
	app.run(debug=True)

