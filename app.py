from flask import Flask, send_file, Response
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------- HOME PAGE ----------------
@app.route("/")
def index():
    return """
<!DOCTYPE html>
<html>
<head>
<title>DevFest Nashik | Robotics Showcase</title>
<style>
body{
  margin:0;
  font-family:Arial;
  background:#0b0b0b;
  color:white;
}
header{
  padding:60px 20px;
  text-align:center;
  background:linear-gradient(135deg,#111827,#000);
}
section{
  max-width:900px;
  margin:auto;
  padding:40px 20px;
}
.card{
  background:#111827;
  padding:20px;
  border-radius:14px;
  margin-bottom:30px;
}
video{
  width:100%;
  border-radius:12px;
  outline:none;
}
footer{
  text-align:center;
  padding:20px;
  opacity:.6;
}
</style>
</head>
<body>

<header>
  <h1>🤖 DevFest Nashik</h1>
  <p>Robotics & AI Showcase</p>
</header>

<section>
  <div class="card">
    <h2>Robot Demo – Part 1</h2>
    <video controls>
      <source src="/video1.mp4" type="video/mp4">
      Your browser does not support video.
    </video>
  </div>

  <div class="card">
    <h2>Robot Demo – Part 2</h2>
    <video controls>
      <source src="/video2.mp4" type="video/mp4">
      Your browser does not support video.
    </video>
  </div>

  <div class="card">
    <h2>About</h2>
    <p>
      This portal showcases robotics demos from DevFest Nashik.
      Built for developers, by developers.
    </p>
  </div>
</section>

<footer>
  <p>DevFest Nashik • Developer Friendly</p>
</footer>

</body>
</html>
"""

# ---------------- VIDEO ROUTES (NO STATIC) ----------------
@app.route("/video1.mp4")
def video1():
    return send_file(os.path.join(BASE_DIR, "video1.mp4"), mimetype="video/mp4")

@app.route("/video2.mp4")
def video2():
    return send_file(os.path.join(BASE_DIR, "video2.mp4"), mimetype="video/mp4")

# ---------------- REAL ROBOTS.TXT ----------------
@app.route("/robots.txt")
def robots():
    content = """User-agent: *
Disallow: /admin
Disallow: /internal
Disallow: /secret

# 👀 curious developer detected :-)
# robots.txt is real here, not JS fake

FLAG: ctf7{robots_txt_real_flask}
"""
    return Response(content, mimetype="text/plain")

# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
