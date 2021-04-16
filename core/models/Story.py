from service.server import db
import datetime
from sqlalchemy import Boolean, Column, Numeric, String
from sqlalchemy.dialects.postgresql import JSONB, TIMESTAMP, BYTEA

class Story(db.Model):
    __tablename__ = 'stories'
    __table_args__ = {'schema' : 'stories_schema'}

    id 	= Column(String(255), primary_key=True)
    created_at = Column(TIMESTAMP)
    grapher_name = Column(String)
    name = Column(String(255))
    description = Column(String)
    duration = Column(Numeric)
    state = Column(String(20))
    file = Column(BYTEA)
    file_type = Column(String(20))
    latitude = Column(Numeric)
    longitude = Column(Numeric)
    
    def serialize(self):
        self.__dict__.pop('_sa_instance_state')
        return self.__dict__

    def __getitem__(self, item):
        return getattr(self, item)