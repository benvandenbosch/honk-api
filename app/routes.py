from app import honk

@honk.route('/')
@honk.route('/index')
def index():
    return "Hello, Honk!"
