from app import PeakPyApp

app = PeakPyApp()

@app.route('/home')
def home(request, response):
    response.text = "Hello, this is home page"


@app.route('/about')
def about(request, response):
    response.text = "Hello, this is about page"