from server.database import Base, engine

Base.metadata.create_all(engine)