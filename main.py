import os

import sendgrid
from flask import Flask, request
from sendgrid.helpers.mail import *

SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def mail():
    if request.method == "POST":
        sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
        from_email = Email(request.form.get("from_email"))
        to_email = Email(request.form.get("to_email"))
        subject = request.form.get("subject")
        content = Content("text/plain", request.form.get("content"))
        mail = Mail(from_email, subject, to_email, content)
        response = sg.client.mail.send.post(request_body=mail.get())
        if response.status_code == 202:
            return "Email sent successfully!"
        else:
            return "Status Code: " + str(response.status_code)
    else:
        return """
        <html>
           <body>
              <form action = "http://localhost:5000/" method = "POST">
                 <p>From: <input type = "text" name = "from_email" value="test@example.com" style="width: 500px;" /></p>
                 <p>To: <input type = "text" name = "to_email" value="test@example.com" style="width: 500px;" /></p>
                 <p>Subject: <input type = "text" name = "subject" value="Sending with SendGrid is Fun" style="width: 500px;" /></p>
                 <p>Content: <input type ="text" name = "content" value="and easy to do anywhere, even with Python" style="width: 500px;" /></p>
                 <p><input type = "submit" value = "send email" /></p>
              </form>
           </body>
        </html>
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
