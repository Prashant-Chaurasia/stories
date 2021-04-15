from service import db
import datetime
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, BYTEA

class Story(db.Model):
    __tablename__ = 'stories'
    __table_args__ = {'schema' : 'stories_schema'}

    id 	= Column(String(255), primary_key=True)
    created_at = Column(TIMESTAMP)
    grapher_name = Column(String)
    name = Column(String(255))
    description = Column(String)
    duration = Column(Integer)
    file_type = Column(String(20))
    state = Column(String(20))
    file = Column(BYTEA)
    # lattitude = Column(Boolean)
    # longitude = Column(TIMESTAMP)
    
    def serialize(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

    def __getitem__(self, item):
        return getattr(self, item)