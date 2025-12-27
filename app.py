from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# ---------------- DATABASE INIT ----------------
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)
    c.execute("SELECT * FROM users")
    if not c.fetchall():
        c.execute("INSERT INTO users VALUES (NULL, 'admin', 'admin123')")
    conn.commit()
    conn.close()

init_db()

# ---------------- ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    success = False

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        # ⚠️ SAFE DEMO MODE
        # Still shows auth-bypass concept but Render-safe
        if "'" in password or "OR" in password.upper():
            success = True
        else:
            c.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, password)
            )
            if c.fetchone():
                success = True

        conn.close()

        if success:
            return success_page()
        else:
            error = "Invalid credentials"

    return login_page(error)

# ---------------- HTML PAGES ----------------
def login_page(error):
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>DevFest Nashik | Secret Portal</title>
<style>
body {{
  background:#0f172a;
  color:white;
  font-family:Arial;
  display:flex;
  justify-content:center;
  align-items:center;
  height:100vh;
}}
.container {{
  background:#111827;
  padding:40px;
  border-radius:14px;
  width:360px;
  text-align:center;
  box-shadow:0 20px 40px rgba(0,0,0,.6);
}}
input {{
  width:100%;
  padding:12px;
  margin:10px 0;
  border:none;
  border-radius:8px;
}}
button {{
  padding:12px;
  width:100%;
  background:#2563eb;
  border:none;
  color:white;
  border-radius:8px;
  font-size:16px;
}}
.error {{
  color:#f87171;
}}
.hint {{
  opacity:.6;
  font-size:13px;
  margin-top:15px;
}}
</style>
</head>
<body>

<div class="container">
  <h2>🔐 DevFest Nashik</h2>
  <p>Internal Speaker Portal</p>

  <form method="POST">
    <input name="username" placeholder="Username" required>
    <input name="password" placeholder="Password" required>
    <button>Login</button>
  </form>

  <div class="error">{error}</div>
  <div class="hint">For demo & learning only</div>
</div>

</body>
</html>
"""

def success_page():
    return """
<!DOCTYPE html>
<html>
<head>
<title>Access Granted</title>
<style>
body {
  background:#020617;
  color:#e5e7eb;
  font-family:Arial;
  display:flex;
  justify-content:center;
  align-items:center;
  height:100vh;
}
.container {
  max-width:650px;
  background:#111827;
  padding:40px;
  border-radius:14px;
}
.flag {
  color:#22c55e;
  font-size:20px;
  margin:15px 0;
}
.typing {
  font-family:monospace;
  white-space:pre-line;
  margin-top:20px;
  border-left:3px solid #22c55e;
  padding-left:15px;
}
</style>
</head>
<body>

<div class="container">
  <h2>✅ Access Granted</h2>
  <div class="flag">ctf7{sql_injection_auth_bypass}</div>
  <div id="typing" class="typing"></div>
</div>

<script>
const text = `
What just happened?

This portal demonstrates Authentication Bypass.

In vulnerable applications,
user input is trusted blindly.

Attackers can manipulate logic
to gain access without real credentials.

This technique is called:
SQL Injection – Authentication Bypass

Fix in real apps:
• Use parameterized queries
• Never trust user input
• Validate everything
`;

let i = 0;
function typeEffect() {
  if (i < text.length) {
    document.getElementById("typing").innerHTML += text.charAt(i);
    i++;
    setTimeout(typeEffect, 25);
  }
}
typeEffect();
</script>

</body>
</html>
"""

# ---------------- RENDER SAFE ENTRY ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
