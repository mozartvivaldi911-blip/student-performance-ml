from flask import Flask, render_template_string

app = Flask(__name__)

HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>BLACK WOLF PRO // OMNI-EYES GRID</title>
    <style>
        body {
            background-color: #050505;
            color: #00ff66;
            font-family: monospace;
            text-align: center;
            padding-top: 50px;
        }
        h1 {
            font-size: 2.5em;
            text-shadow: 0 0 10px #00ff66;
        }
        .box {
            border: 2px solid #00ff66;
            display: inline-block;
            padding: 20px 40px;
            box-shadow: 0 0 20px rgba(0, 255, 102, 0.3);
            background: #101010;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>BLACK WOLF PRO</h1>
        <p>STATUS: ONLINE & SECURE ⚡</p>
        <p>SYSTEM ARCHITECTURE: ACTIVE ON CLOUD</p>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HOME_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

