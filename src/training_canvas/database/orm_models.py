from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    project_name = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return f"project_name = {self.project_name}"


class Checkpoints(Base):
    __tablename__ = "checkpoints"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    checkpoint_blob_storage_uid = Column(String, nullable=False, unique=True)

    # project = relationship("Projects", back_populates="id")

    def __repr__(self):
        return f"project_id = {self.project_id}, checkpoint_blob_storage_uid = {self.checkpoint_blob_storage_uid}"


class Classes(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))

    # project = relationship("projects", back_populates="id")

    def __repr__(self):
        return f"label = {self.label}, project_id = {self.project_id}"


class Images(Base):
    __tablename__ = "images"

    blob_storage_uid = Column(String, nullable=False, primary_key=True)
    classes_id = Column(Integer, ForeignKey("classes.id"))

    # classes = relationship("Classes", back_populates="id")

    def __repr__(self):
        return f"blob_storage_uid = {self.blob_storage_uid}, classes_id = {self.classes_id}"
