from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    project_name = Column(String, nullable=False, unique=True)


class Checkpoints(Base):
    __tablename__ = "checkpoints"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, nullable=False)
    checkpoint_blob_storage_uid = Column(String, nullable=False, unique=True)

    project = relationship("Projects", back_populates="id")


class Classes(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    project_id = Column(Integer, nullable=False)

    project = relationship("Projects", back_populates="id")


class Images(Base):
    __tablename__ = "images"

    blob_storage_uid = Column(String, nullable=False, primary_key=True)
    classes_id = Column(Integer, nullable=False)

    classes = relationship("Classes", back_populates="id")
