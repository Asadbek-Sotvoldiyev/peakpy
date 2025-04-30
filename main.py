from peakpy.app import PeakPy
from peakpy.middleware import Middleware

app = PeakPy()

@app.route('/home', methods=['POST'])
def home(request, response):
    response.text = "Hello, this is home page"


@app.route('/about')
def about(request, response):
    response.text = "Hello, this is about page"


@app.route('/hello/{name}')
def greeting(request, response, name):
    response.text = f"Hello, {name}"


@app.route('/books')
class Book:
    def get(self, request, response):
        response.text = "Hello, this is books page"

    def post(self, request, response):
        response.text = "Endpoint to create books"


def template(req, resp):
    resp.html = app.template(
        "test.html",
        context = {
            'new_title': 'Asadbek',
            'new_body': 'This is the body',
        }
    )
app.add_route('/template-handler', template)

@app.route("/json")
def json_template(req, resp):
    response_data = {"name": "Asadbek", "age": 30}
    resp.json = response_data


def on_exception(req, resp, exc):
    resp.text = "Something went wrong"

app.add_exception_handler(on_exception)

@app.route('/exception')
def exception_throwing_handler(req, resp):
    raise AttributeError("Some Exception")


class LoggingMiddleware(Middleware):
    def process_request(self, req):
        print("Process request")

    def process_response(self, req, resp):
        print("Process response")


app.add_middleware(LoggingMiddleware)