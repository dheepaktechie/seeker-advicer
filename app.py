from flask import Flask, render_template, request, redirect, session, url_for
import random

app = Flask(__name__)
app.secret_key = "supersecretkey123"


# -------------------------------
# HOME PAGE
# -------------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -------------------------------
# EXPERT LOGIN
# -------------------------------
@app.route("/expert-login", methods=["GET", "POST"])
def expert_login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "user" and password == "123":
            session["expert"] = username
            return redirect(url_for("expert_dashboard"))
        else:
            return render_template("expert-login.html", error="Invalid Credentials")

    return render_template("expert-login.html")


# -------------------------------
# EXPERT DASHBOARD
# -------------------------------
@app.route("/expert-dashboard")
def expert_dashboard():

    if "expert" not in session:
        return redirect(url_for("expert_login"))

    return render_template("expert-dashboard.html")


# -------------------------------
# SEEKER DASHBOARD (SIMULATION)
# -------------------------------
@app.route("/seeker-dashboard", methods=["GET", "POST"])
def seeker_dashboard():

    ai_output = None
    error_message = None

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        role = request.form.get("role")
        domain = request.form.get("domain")
        challenge = request.form.get("challenge")
        urgency = request.form.get("urgency")
        risk = request.form.get("risk")

        if not challenge:
            error_message = "Please describe your challenge."
        else:

            risk_score = random.randint(40, 95)

            if urgency in ["High", "Critical"]:
                complexity = "High"
            elif urgency == "Moderate":
                complexity = "Medium"
            else:
                complexity = "Low"

            ai_output = {
                "name": name,
                "email": email,
                "role": role,
                "domain_category": domain,
                "challenge": challenge,
                "complexity_level": complexity,
                "risk_score": risk_score,
                "recommended_expert": "Strategic Risk Consultant",
                "success_metrics": "Track KPIs like cost reduction %, timeline adherence, and measurable performance improvement."
            }

    return render_template(
        "seeker-dashboard.html",
        ai_output=ai_output,
        error_message=error_message
    )


# -------------------------------
# LOGOUT
# -------------------------------
@app.route("/logout")
def logout():
    session.pop("expert", None)
    return redirect(url_for("home"))


# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)