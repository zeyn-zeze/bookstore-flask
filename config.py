class Config:
    
    SECRET_KEY = 'book_store_secret_key'
    SESSION_COOKIE_NAME = 'session'
    

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/book_store'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

