from flask import Flask, jsonify, request, render_template
from flask_httpauth import HTTPBasicAuth

from lib.config import ADMIN_USERNAME, ADMIN_PASSWORD
from lib.openai_utils import generate_seo_content, SeoResult

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return username


@app.route("/")
def hello_world():
    return render_template("home.html")


@app.post("/generate")
@auth.login_required
def generate():
    html = request.json.get('html', '').strip()
    keywords = request.json.get('keywords', '').strip()

    if not html or not keywords:
        return jsonify({"error": "Html or Keywords can't be empty!", "success": False})

    content: SeoResult = generate_seo_content(html, keywords)
    return jsonify({"content": content.dict(), "success": True})


@app.get("/compare")
def compare():
    return render_template("compare.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)