from flask import Flask, request, Response
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
    </video>
  </div>

  <div class="card">
    <h2>Robot Demo – Part 2</h2>
    <video controls>
      <source src="/video2.mp4" type="video/mp4">
    </video>
  </div>
</section>

<footer>
  <p>DevFest Nashik • Developer Friendly</p>
</footer>

</body>
</html>
"""

# ---------------- RANGE-SAFE VIDEO STREAMING ----------------
def stream_video(path):
    file_size = os.path.getsize(path)
    range_header = request.headers.get('Range', None)

    if range_header:
        byte1, byte2 = 0, None
        match = range_header.replace('bytes=', '').split('-')
        byte1 = int(match[0])
        if len(match) > 1 and match[1]:
            byte2 = int(match[1])

        length = file_size - byte1
        if byte2:
            length = byte2 - byte1 + 1

        with open(path, 'rb') as f:
            f.seek(byte1)
            data = f.read(length)

        rv = Response(data, 206, mimetype='video/mp4',
                      content_type='video/mp4',
                      direct_passthrough=True)
        rv.headers.add(
            'Content-Range',
            f'bytes {byte1}-{byte1 + length - 1}/{file_size}'
        )
        rv.headers.add('Accept-Ranges', 'bytes')
        return rv

    # Fallback (no range)
    with open(path, 'rb') as f:
        data = f.read()

    return Response(data, mimetype='video/mp4')

@app.route("/video1.mp4")
def video1():
    return stream_video(os.path.join(BASE_DIR, "video1.mp4"))

@app.route("/video2.mp4")
def video2():
    return stream_video(os.path.join(BASE_DIR, "video2.mp4"))

# ---------------- REAL ROBOTS.TXT ----------------
@app.route("/robots.txt")
def robots():
    return Response(
        """User-agent: *
Disallow: /admin
Disallow: /internal
Disallow: /secret

# 👀 real dev spotted
FLAG: ctf7{robots_txt_real_flask}
""",
        mimetype="text/plain"
    )

# ---------------- ENTRY POINT ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
