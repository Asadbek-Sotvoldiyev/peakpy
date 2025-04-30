import pytest
from peakpy.middleware import Middleware

def test_basic_route_adding(app):
    @app.route('/home')
    def home(req, resp):
        resp.text = 'Hello from home'


def test_duplicate_routes_throws_exception(app):
    @app.route('/home')
    def home(req, resp):
        resp.text = 'Hello from home'

    with pytest.raises(AssertionError):
        @app.route('/home')
        def home(req, resp):
            resp.text = 'Hello from home2'

def test_requests_can_be_sent_by_test_client(app, client):
    @app.route('/home')
    def home(req, resp):
        resp.text = 'Hello from home'

    response = client.get("http://testserver/home")
    assert response.text == 'Hello from home'


def test_parametrized_routing(app, client):
    @app.route('/hello/{name}')
    def greeting(req, resp, name):
        resp.text = f'Hello, {name}!'

    assert client.get('http://testserver/hello/Asadbek').text == 'Hello, Asadbek!'
    assert client.get('http://testserver/hello/Matthew').text == 'Hello, Matthew!'


def test_default_response(app, client):
    response = client.get('http://testserver/nonexistent')

    assert response.status_code == 404
    assert response.text == 'Not Found'


def test_class_based_get(app, client):
    @app.route('/books')
    class Books:
        def get(self, req, resp):
            resp.text = 'Books page'

    assert client.get('http://testserver/books').text == 'Books page'


def test_class_based_post(app, client):
    @app.route('/books')
    class Books:
        def post(self, req, resp):
            resp.text = 'Endpoint to create a book'

    assert client.post('http://testserver/books').text == 'Endpoint to create a book'


def test_class_based_method_not_allowed(app, client):
    @app.route('/books')
    class Books:
        def get(self, req, resp):
            resp.text = 'Books page'

    response =  client.post('http://testserver/books')

    assert response.status_code == 405
    assert response.text == 'Method Not Allowed'


def test_alternative_route_adding(app, client):
    def new_handler(req, resp):
        resp.text = 'From new handler'

    app.add_route('/new-handler', new_handler)
    assert client.get('http://testserver/new-handler').text == 'From new handler'


def test_template_handler(app, client):
    def template(req, resp):
        resp.body = app.template(
            "test.html",
            context = {
                'new_title': 'Home',
                'new_body': 'This is the body',
            }
        )
    app.add_route('/template-handler', template)
    response = client.get('http://testserver/template-handler')
    assert "Home" in response.text
    assert "This is the body" in response.text

    assert "text/html" in response.headers['Content-Type']


def test_custom_exception_handler(app, client):
    def on_exception(req, resp, exc):
        resp.text = "Something went wrong"

    app.add_exception_handler(on_exception)

    @app.route('/exception')
    def exception_throwing_handler(req, resp):
        raise AttributeError("Some Exception")

    response = client.get('http://testserver/exception')
    assert response.text == "Something went wrong"


def test_non_existent_static_file(client):
    assert client.get('http://testserver/static/nonexistent.css').status_code == 404

def test_serving_static_file(client):
    response = client.get('http://testserver/static/test.css')

    assert response.text == "body{background-color: chocolate}"


def test_middleware_methods_are_called(app, client):
    process_reqeust_called = False
    process_response_called = False

    class SimpleMiddleware(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def process_request(self, req):
            nonlocal process_reqeust_called
            process_reqeust_called = True

        def process_response(self, req, resp):
            nonlocal process_response_called
            process_response_called = True


    app.add_middleware(SimpleMiddleware)

    @app.route('/home')
    def home(req, resp):
        resp.text = 'Hello from home'

    client.get('http://testserver/home')

    assert process_response_called is True
    assert process_reqeust_called is True


def test_allowed_methods_for_function_based_handler(app, client):
    @app.route('/home', methods=['POST'])
    def home(req, resp):
        resp.text = 'Hello from home'

    response = client.get('http://testserver/home')

    assert response.status_code == 405
    assert response.text == 'Method Not Allowed'


def test_json_response_helper(app, client):
    @app.route('/json')
    def json_response(req, resp):
        resp.json = {'name': 'PeakPy'}

    response = client.get('http://testserver/json')
    resp_data = response.json()

    assert response.headers['Content-Type'] == 'application/json'
    assert resp_data['name'] == 'PeakPy'

def test_text_handler_helper(app, client):
    @app.route('/text')
    def text_handler(req, resp):
        resp.text = 'Plain text'

    response = client.get('http://testserver/text')
    assert response.text == 'Plain text'
    assert 'text/plain' in response.headers['Content-Type']

def test_html_handler_helper(app, client):
    @app.route('/html')
    def html_handler(req, resp):
        resp.html = app.template(
            "test.html",
            context = {"new_title": "Home", "new_body": "This is the body"},
        )

    response = client.get('http://testserver/html')

    assert 'text/html' in response.headers['Content-Type']
    assert "Home" in response.text
    assert "This is the body" in response.text

