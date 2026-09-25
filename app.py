from flask import Flask, request, render_template_string, redirect, session

app = Flask(__name__)
app.secret_key = "internship-tracker-secret"


# DEMO USERS


USERS = {
    "asha": {"password": "asha123", "name": "Asha Menon"},
    "ravi": {"password": "ravi123", "name": "Ravi Kumar"}
}

# Each user has their own list of internship applications
APPLICATIONS = {
    "asha": [
        {"company": "TechNova", "role": "Web Dev Intern", "status": "Interview", "date": "2026-08-01"},
        {"company": "Cloudify", "role": "Cloud Support Intern", "status": "Applied", "date": "2026-08-10"}
    ],
    "ravi": [
        {"company": "DataWorks", "role": "Data Analyst Intern", "status": "Offer", "date": "2026-07-20"}
    ]
}

STATUS_OPTIONS = ["Applied", "Interview", "Offer", "Rejected"]


def logged_in():
    return "username" in session


# LOGIN PAGE

LOGIN_PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Internship Tracker - Login</title>
<style>
body { font-family: Arial; background: #eef2f7; display:flex; justify-content:center; align-items:center; height:100vh; margin:0; }
.box { background:white; padding:30px; border-radius:10px; width:300px; box-shadow:0 2px 10px #ccc; }
input { width:100%; padding:10px; margin:6px 0 14px 0; box-sizing:border-box; }
button { width:100%; padding:10px; background:#2563eb; color:white; border:none; border-radius:5px; }
.error { color:red; text-align:center; }
.hint { font-size:12px; color:#555; margin-top:15px; }
</style>
</head>
<body>
<div class="box">
<h2>Internship Tracker</h2>
{% if error %}<p class="error">{{ error }}</p>{% endif %}
<form method="post">
<label>Username</label>
<input type="text" name="username" required>
<label>Password</label>
<input type="password" name="password" required>
<button type="submit">Login</button>
</form>
<p class="hint">Demo: asha / asha123 <br> Demo: ravi / ravi123</p>
</div>
</body>
</html>
"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in USERS and USERS[username]["password"] == password:
            session["username"] = username
            return redirect("/")
        return render_template_string(LOGIN_PAGE, error="Invalid username or password")
    return render_template_string(LOGIN_PAGE, error=None)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# COMMON PAGE LAYOUT

PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Internship Tracker</title>
<style>
body { font-family: Arial; background:#f4f7fb; margin:0; }
.nav { background:#111827; color:white; padding:15px 25px; display:flex; justify-content:space-between; align-items:center; }
.nav a { color:white; text-decoration:none; margin-left:15px; }
.main { padding:25px; max-width:800px; margin:auto; }
table { width:100%; border-collapse: collapse; background:white; }
th, td { padding:10px; border-bottom:1px solid #ddd; text-align:left; }
.status { padding:4px 8px; border-radius:5px; font-size:13px; }
.Applied { background:#dbeafe; color:#1d4ed8; }
.Interview { background:#fef3c7; color:#b45309; }
.Offer { background:#dcfce7; color:#15803d; }
.Rejected { background:#fee2e2; color:#b91c1c; }
.card { background:white; padding:20px; border-radius:8px; margin-bottom:20px; box-shadow:0 2px 8px #ddd; }
input, select { padding:8px; margin:5px 0; width:100%; box-sizing:border-box; }
button { padding:8px 15px; background:#2563eb; color:white; border:none; border-radius:5px; }
</style>
</head>
<body>
<div class="nav">
  <div>Internship Tracker — {{ name }}</div>
  <div><a href="/logout">Logout</a></div>
</div>
<div class="main">
{{ content | safe }}
</div>
</body>
</html>
"""


# DASHBOARD - list all internship applications

@app.route("/")
def dashboard():
    if not logged_in():
        return redirect("/login")
    username = session["username"]
    apps = APPLICATIONS.get(username, [])

    content = """
    <div class="card">
      <h2>Your Internship Applications</h2>
      <a href="/add"><button>+ Add New Application</button></a>
    </div>
    <div class="card">
      <table>
        <tr><th>Company</th><th>Role</th><th>Date Applied</th><th>Status</th><th>Update</th></tr>
        {% for i in range(apps|length) %}
        <tr>
          <td>{{ apps[i].company }}</td>
          <td>{{ apps[i].role }}</td>
          <td>{{ apps[i].date }}</td>
          <td><span class="status {{ apps[i].status }}">{{ apps[i].status }}</span></td>
          <td>
            <form method="post" action="/update/{{ i }}">
              <select name="status" onchange="this.form.submit()">
                {% for s in status_options %}
                <option value="{{ s }}" {% if s == apps[i].status %}selected{% endif %}>{{ s }}</option>
                {% endfor %}
              </select>
            </form>
          </td>
        </tr>
        {% endfor %}
      </table>
    </div>
    """
    rendered = render_template_string(content, apps=apps, status_options=STATUS_OPTIONS)
    return render_template_string(PAGE, name=USERS[username]["name"], content=rendered)



# ADD NEW APPLICATION

<div class="card">
  <h2>Add Internship Application</h2>
  <form method="post">
    <label>Company Name</label>
    <input type="text" name="company" required>
    <label>Role</label>
    <input type="text" name="role" required>
    <label>Date Applied</label>
    <input type="date" name="date" required>
    <button type="submit">Save</button>
  </form>
  <br>
  <a href="/">Back to Dashboard</a>
</div>
"""


@app.route("/add", methods=["GET", "POST"])
def add():
    if not logged_in():
        return redirect("/login")
    username = session["username"]
    if request.method == "POST":
        new_app = {
            "company": request.form["company"],
            "role": request.form["role"],
            "date": request.form["date"],
            "status": "Applied"
        }
        APPLICATIONS.setdefault(username, []).append(new_app)
        return redirect("/")
    rendered = render_template_string(ADD_FORM)
    return render_template_string(PAGE, name=USERS[username]["name"], content=rendered)


# UPDATE STATUS

@app.route("/update/<int:index>", methods=["POST"])
def update(index):
    if not logged_in():
        return redirect("/login")
    username = session["username"]
    new_status = request.form["status"]
    if 0 <= index < len(APPLICATIONS.get(username, [])):
        APPLICATIONS[username][index]["status"] = new_status
    return redirect("/")



# RUN LOCALLY

if __name__ == "__main__":
    app.run(debug=True)
