from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import date

# Define the base class
Base = declarative_base()

class Regions(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    region_name = Column(String, nullable=False, unique=True)
    created_at = Column(Date, default=date.today)
    modified_at = Column(Date, default=date.today)

    def __repr__(self):
        return f"<Regions(id={self.id}, name='{self.region_name}', created_at={self.created_at}, modified_at={self.modified_at})>"


class Provinces(Base):
    __tablename__ = "provinces"

    id = Column(Integer, primary_key=True, autoincrement=True)
    province_name = Column(String, nullable=False, unique=True)
    region_id = Column(Integer, nullable=False)
    created_at = Column(Date, default=date.today)
    modified_at = Column(Date, default=date.today)

    def __repr__(self):
        return f"<Provinces(id={self.id}, name='{self.region_name}', created_at={self.created_at}, modified_at={self.modified_at}, region_id={self.region_id})>"

engine = create_engine("sqlite:///provinces.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
