from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Projects(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    project_name = Column(String, nullable=False, unique=True)

    classes = relationship("Classes", back_populates="project")
    checkpoints = relationship("Checkpoints", back_populates="project")

    def __repr__(self):
        return f"project_name = {self.project_name}"


class Checkpoints(Base):
    __tablename__ = "checkpoints"
    __table_args__ = (
        UniqueConstraint(
            "checkpoint_blob_name",
            "project_id",
            name="uc_checkpoint_blob_name_project_id",
        ),
    )

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    checkpoint_blob_name = Column(String, nullable=False, unique=True)

    project = relationship("Projects", back_populates="checkpoints")

    def __repr__(self):
        return f"project_id = {self.project_id}, checkpoint_blob_name = {self.checkpoint_blob_name}"


class Classes(Base):
    __tablename__ = "classes"
    __table_args__ = (
        UniqueConstraint("label", "project_id", name="uc_label_project_id"),
    )

    id = Column(Integer, primary_key=True)
    label = Column(String, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"))

    project = relationship("Projects", back_populates="classes")

    def __repr__(self):
        return f"label = {self.label}, project_id = {self.project_id}"


class Images(Base):
    __tablename__ = "images"

    blob_name = Column(String, nullable=False, primary_key=True)
    classes_id = Column(Integer, ForeignKey("classes.id"))

    # classes = relationship("Classes", back_populates="id")

    def __repr__(self):
        return f"blob_name = {self.blob_name}, classes_id = {self.classes_id}"
