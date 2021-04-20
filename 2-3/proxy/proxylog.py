from sqlalchemy import create_engine, Column,Integer,String,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime


Base = declarative_base()

class ProxyLog(Base):
    __tablename__ = 'person'

    id = Column('id', Integer, primary_key=True)
    proxy_address = Column('proxy_address', String, unique=False)
    online = Column(DateTime, default=datetime.datetime.utcnow)
    offline = Column(DateTime, default=None)

engine = create_engine('sqlite:///proxy.db', echo=True)

Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)


