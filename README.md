# PeakPy: Python web framework built for learning purposes

![Purpose](https://img.shields.io/badge/purpose-learning-green)
![PyPI - Version](https://img.shields.io/pypi/format/peakpy)

PeakPy is a Python Web framework built for learning purposes.

It's a WSGI framework and can be used with any WSGI application server such as GUNICORN.

## Installation

```shell
pip install peakpy
```

## How to use it

### Dynamic Routes:
Handle dynamic URLs with parameters:
```python
from peakpy import PeakPy

app = PeakPy()

@app.route("/hello/{name}")
def greet(req, resp, name):
    resp.text = f"Hello, {name}!"
```

### Templates:
Render HTML templates with Jinja2:
```python
from peakpy import PeakPy

app = PeakPy(templates_dir="templates")

@app.route("/hello/{name}")
def greet(req, resp, name):
    resp.html = app.template("index.html", context={"name": name})
```

Create templates/index.html::
```html
<!DOCTYPE html>
<html>
<head>
    <title>Hello</title>
</head>
<body>
    <h1>Hello, {{ name }}!</h1>
</body>
</html>
```

### Static Files:
Place static files (e.g., style.css) in the static directory. They are served at /static/:
```css
/* static/style.css */
body {
    background-color: lightblue;
}
```

Link it in your template:
```html
<link rel="stylesheet" href="/static/style.css">
```
Access http://localhost:8000/static/style.css directly.

### Templates and Static Files
PeakPy supports dynamic HTML rendering with Jinja2 templates and static file serving with WhiteNoise.
- Templates: Store Jinja2 template files (e.g., .html) in a directory. By default, PeakPy looks for templates in the templates directory. To use a custom directory, specify template_dir when creating the PeakPy instance:
    ```python
  app = PeakPy(template_dir="my_templates")
  ```
  If template_dir is not provided, it defaults to templates.
- Static Files: Store static assets (e.g., .css, .js, images) in a directory. By default, PeakPy serves files from the static directory at /static/. To use a custom directory, specify static_dir:
  ```python
  app = PeakPy(static_dir="my_static")
  ```
  If static_dir is not provided, it defaults to static. 
- Example with custom directories:
  ```python
  app = PeakPy(template_dir="custom_templates", static_dir="custom_static")
    ```
  Ensure the specified directories exist in your project root.


### Middleware:
Add middleware to process requests or responses:
```python
from peakpy import PeakPy, Middleware

app = PeakPy()

class LoggingMiddleware(Middleware):
    def process_request(self, req):
        print(f"Received request: {req.path}")
    
    def process_response(self, req, resp):
        print("Response sent")

app.add_middleware(LoggingMiddleware)

@app.route("/home")
def home(req, resp):
    resp.text = "Hello from PeakPy!"
```

### JSON Responses:
Return JSON data:
```python
from peakpy import PeakPy

app = PeakPy()

@app.route("/api")
def api(req, resp):
    resp.json = {"message": "Welcome to the API"}
```
Access http://localhost:8000/api to get a JSON response.

### Custom Error Handling:
Handle exceptions gracefully:
```python
from peakpy import PeakPy

app = PeakPy()

def on_exception(req, resp, exc):
    resp.status_code = 500
    resp.text = "Something went wrong!"

app.add_exception_handler(on_exception)

@app.route("/error")
def error(req, resp):
    raise ValueError("Test error")
```
Visit http://localhost:8000/error to see the custom error message.

## Contributing
Contributions are welcome! Fork the repository, create a branch, and submit a pull request on GitHub.

## Contact
For support or feedback, open an issue on the GitHub repository or email blogasadbek@gmail.com.
