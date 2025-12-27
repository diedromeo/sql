from flask import Flask, request
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE SETUP ----------------
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

# ---------------- LOGIN ROUTE ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        # ❌ INTENTIONALLY VULNERABLE QUERY (CTF PURPOSE)
        query = f"""
        SELECT * FROM users
        WHERE username = '{username}' AND password = '{password}'
        """
        print("[DEBUG QUERY]:", query)

        c.execute(query)
        user = c.fetchone()
        conn.close()

        if user:
            return success_page()
        else:
            error = "Invalid credentials"

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
  cursor:pointer;
}}
.error {{
  color:#f87171;
  margin-top:10px;
}}
.hint {{
  opacity:.6;
  margin-top:20px;
  font-size:13px;
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

  <div class="hint">Authorized access only</div>
</div>

</body>
</html>
"""

# ---------------- SUCCESS PAGE ----------------
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
  max-width:600px;
  background:#111827;
  padding:40px;
  border-radius:14px;
  box-shadow:0 20px 40px rgba(0,0,0,.6);
}
.flag {
  color:#22c55e;
  font-size:20px;
  margin:15px 0;
}
.typing {
  border-left:3px solid #22c55e;
  padding-left:15px;
  white-space:pre-line;
  font-family:monospace;
  font-size:14px;
  margin-top:20px;
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

This login portal was vulnerable to SQL Injection.

Your input was directly added to the SQL query
without proper sanitization.

This allowed you to modify the query logic
and bypass authentication.

This attack is known as:
Authentication Bypass using SQL Injection.

In real applications:
• Always use parameterized queries
• Never trust user input
• Validate and sanitize everything
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

if __name__ == "__main__":
    app.run(debug=True)
