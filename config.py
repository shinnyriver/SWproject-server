class Config:
    SECRET_KEY = "secretkey"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://photo_user:1234@localhost/photo_diary"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
