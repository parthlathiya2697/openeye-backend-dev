from sqlalchemy import Column, Integer, String

from app.db.base_class import Base


class Badge(Base):
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    text_color = Column(String)
    background_color = Column(String)
