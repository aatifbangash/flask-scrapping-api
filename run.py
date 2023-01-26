from api import app

if __name__ == '__main__':
    app.config.from_object("config.BaseConfig")
    
    app_debug = app.config['DEBUG']
    
    app.run(debug=app_debug) #default port is 5000