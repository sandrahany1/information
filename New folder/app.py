from flask import Flask
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager


mysql = MySQL()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''  
    app.config['MYSQL_DB'] = 'task_db'

    
    app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'  

    
    mysql.init_app(app)
    jwt.init_app(app)

    
    from auth import auth_bp  
    from product import product_bp  

    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)

    return app

if __name__ == "__main__":
    
    app = create_app()
    app.run(debug=True)









