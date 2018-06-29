
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
engine = create_engine(
    'mssql+pyodbc://1410332003:Qwe123456!@163.17.136.65/1410332003'
)
#app = Flask(__name__)




