import os
from web_server import app

if __name__ == '__main__':
    print('This is the main function')
    api_port = os.environ.get('API_PORT', '0.0.0.0')
    api_host = int(os.environ.get('API_HOST', 8080))

    # run flask app
    app.run(host=api_port, port=api_host, debug=False)