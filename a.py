from flask import Flask, request, jsonify, render_template
import openai

app = Flask(__name__)

# OpenAI API 키 설정
openai.api_key = 'your-openai-api-key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    
    # OpenAI API를 사용하여 응답 생성
    response = openai.Completion.create(
        engine="text-davinci-004",
        prompt=user_input,
        max_tokens=100
    )
    
    generated_text = response.choices[0].text.strip()
    
    return jsonify({'response': generated_text})

if __name__ == '__main__':
    app.run(debug=True)
