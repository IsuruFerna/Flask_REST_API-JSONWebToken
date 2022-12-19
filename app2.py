from flask import Flask, render_template, request

app = Flask('__name__')

app.config['SECRET_KEKY'] = 'thisissecret'

@app.route('/')
def index():
  return 'hello'

@app.route('/login')
def login():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True, port='8001')

