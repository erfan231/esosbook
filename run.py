from esosbook import app, csrf
import os


host = ""
port = 5000

if __name__ == '__main__':
    app.run(debug=True, host=host, port=port)
