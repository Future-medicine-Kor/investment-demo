from flask import Flask, request, redirect, url_for, render_template_string, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # 세션을 위해 필요한 비밀 키 설정

# Dummy user data
USER_DATA = {
    "김대성": "990307",
    "홍길동": "750808",
    "서진영": "010910",
    "이도형": "010103",
    "신채범": "010508",
    "구도윤":"000506",
    "권태희":"980617",
    "임관훈":"040617",
    "전해성":"991102",
    "김동우":"000403",
    "오경빈":"001030",
}

# HTML 템플릿을 문자열로 정의
login_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="POST">
        <div>
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit">Login</button>
    </form>
    {% if error %}
    <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
'''

dashboard_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
</head>
<body>
    <h2>Dashboard</h2>
    <p>현재 잔액: {{ balance }}</p>
    <form method="POST" action="/invest">
        <div>
            <label for="investee">투자할 사람 이름:</label>
            <input type="text" id="investee" name="investee" required>
        </div>
        <div>
            <label for="amount">투자 금액:</label>
            <input type="number" id="amount" name="amount" min="0" max="1000" required>
        </div>
        <button type="submit">투자</button>
    </form>
    {% if error %}
    <p style="color: red;">{{ error }}</p>
    {% endif %}
    <form method="POST" action="/logout">
        <button type="submit">투자 종료</button>
    </form>
</body>
</html>
'''

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in USER_DATA and USER_DATA[username] == password:
            session['username'] = username
            session['balance'] = 1000  # 초기 잔액 설정
            return redirect(url_for('dashboard'))
        else:
            error = "Invalid Credentials. Please try again."
    return render_template_string(login_template, error=error)

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    error = session.pop('error', None)
    return render_template_string(dashboard_template, balance=session['balance'], error=error)

@app.route('/invest', methods=['POST'])
def invest():
    if 'username' not in session:
        return redirect(url_for('login'))

    investee = request.form['investee']
    amount = int(request.form['amount'])
    if investee not in USER_DATA:
        session['error'] = "투자 대상이 등록되어 있지 않습니다."
    elif 0 <= amount <= session['balance']:
        session['balance'] -= amount
        with open('investment_log.txt', 'a', encoding='utf-8') as f:
            f.write(f"ID: {session['username']}, 투자 대상: {investee}, 투자 금액: {amount}\n")
        if session['balance'] <= 0:
            return redirect(url_for('logout'))
    else:
        session['error'] = "Invalid investment amount."

    return redirect(url_for('dashboard'))
sdfas


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    session.pop('balance', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5022, debug=True)
