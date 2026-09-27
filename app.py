from flask import Flask, request, redirect, session

app = Flask(__name__)
app.secret_key = "mysecretkey123"


USERS = {
    "asha": "asha123",
    "ravi": "ravi123"
}

APPLICATIONS = {
    "asha": [
        {"company": "TechNova", "role": "Web Dev Intern", "date": "2026-08-01", "status": "Interview"},
        {"company": "Cloudify", "role": "Cloud Support Intern", "date": "2026-08-10", "status": "Applied"}
    ],
    "ravi": [
        {"company": "DataWorks", "role": "Data Analyst Intern", "date": "2026-07-20", "status": "Offer"}
    ]
}

STATUS_LIST = ["Applied", "Interview", "Offer", "Rejected"]


STYLE = """
<style>
body { font-family: Arial; background: #f4f6f9; margin: 0; padding: 0; }
.topbar { background: #2563eb; color: white; padding: 18px 30px; font-size: 20px; font-weight: bold; }
.container { max-width: 800px; margin: 30px auto; background: white; padding: 25px 30px;
             border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
a { color: #2563eb; text-decoration: none; font-weight: bold; }
table { width: 100%; border-collapse: collapse; margin-top: 15px; }
th, td { padding: 12px; text-align: left; border-bottom: 1px solid #e5e7eb; }
th { background: #f0f4fa; }
input, select { width: 100%; padding: 10px; margin: 6px 0 16px 0; border: 1px solid #ccc;
        border-radius: 6px; box-sizing: border-box; }
button { background: #2563eb; color: white; padding: 10px 18px; border: none;
         border-radius: 6px; font-size: 15px; cursor: pointer; }
button:hover { background: #1d4ed8; }
</style>
"""


@app.route("/")
def home():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    apps = APPLICATIONS[username]

    rows = ""
    for i in range(len(apps)):
        item = apps[i]


        options_html = ""
        for option in STATUS_LIST:
            if option == item["status"]:
                options_html += f'<option value="{option}" selected>{option}</option>'
            else:
                options_html += f'<option value="{option}">{option}</option>'

        rows += f"""
        <tr>
            <td>{item['company']}</td>
            <td>{item['role']}</td>
            <td>{item['date']}</td>
            <td>
                <form method="post" action="/update/{i}" style="margin:0;">
                    <select name="status" onchange="this.form.submit()">{options_html}</select>
                </form>
            </td>
        </tr>
        """

    page = f"""
    <html>
    <head>{STYLE}</head>
    <body>
        <div class="topbar">Internship Tracker - Welcome, {username}</div>
        <div class="container">
            <p><a href="/add">+ Add New Application</a> &nbsp; | &nbsp; <a href="/logout">Logout</a></p>
            <table>
                <tr>
                    <th>Company</th><th>Role</th><th>Date Applied</th><th>Status</th>
                </tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """
    return page


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in USERS and USERS[username] == password:
            session["username"] = username
            return redirect("/")
        else:
            return f"""
            <html><head>{STYLE}</head><body>
            <div class="container" style="max-width:350px; margin-top:100px; text-align:center;">
                <p style="color:red;">Invalid login.</p>
                <a href="/login">Try again</a>
            </div>
            </body></html>
            """

    return f"""
    <html>
    <head>{STYLE}</head>
    <body>
        <div class="container" style="max-width:350px; margin-top:80px;">
            <h2>Internship Tracker</h2>
            <form method="post">
                Username: <input name="username">
                Password: <input name="password" type="password">
                <button type="submit">Login</button>
            </form>
            <p style="font-size:13px; color:#555;">Demo: asha / asha123 <br> Demo: ravi / ravi123</p>
        </div>
    </body>
    </html>
    """


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/add", methods=["GET", "POST"])
def add():
    if "username" not in session:
        return redirect("/login")

    username = session["username"]

    if request.method == "POST":
        company = request.form["company"]
        role = request.form["role"]
        date = request.form["date"]
        APPLICATIONS[username].append({
            "company": company,
            "role": role,
            "date": date,
            "status": "Applied"
        })
        return redirect("/")

    return f"""
    <html>
    <head>{STYLE}</head>
    <body>
        <div class="container" style="max-width:400px; margin-top:60px;">
            <h2>Add Internship Application</h2>
            <form method="post">
                Company: <input name="company">
                Role: <input name="role">
                Date Applied: <input name="date" type="date">
                <button type="submit">Save</button>
            </form>
            <br><a href="/">Back to Dashboard</a>
        </div>
    </body>
    </html>
    """


@app.route("/update/<int:index>", methods=["POST"])
def update(index):
    if "username" not in session:
        return redirect("/login")

    username = session["username"]
    chosen_status = request.form["status"]
    APPLICATIONS[username][index]["status"] = chosen_status
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
