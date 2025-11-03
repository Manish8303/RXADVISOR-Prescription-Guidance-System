from flask import Flask, render_template

# Flask app with custom folders
app = Flask(__name__, template_folder="templates", static_folder="static")

# Route 1: Landing / Entry Page
@app.route('/')
def entry():
    return render_template('entry.html')  # <-- Pehle yeh dikhega

# Route 2: Dashboard (after clicking button)
@app.route('/dashboard')
def dashboard():
    return render_template('index.html')  # <-- Button is link hoga /dashboard pe

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)