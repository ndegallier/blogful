import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://ubuntu:football12@localhost:5432/blogful"
    DEBUG = True