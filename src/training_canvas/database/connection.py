from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import typing as t

from training_canvas.connection import db_engine
from training_canvas.database.orm_models import (
    Projects,
    Base,
    Classes,
    Images,
    Checkpoints,
)


class TrainingCanvasDB:
    def __init__(self) -> None:
        self.session = Session(db_engine)

    def __enter__(self) -> "TrainingCanvasDB":
        return self

    def __exit__(self, *args: t.Any) -> None:
        self.session.close()

    @staticmethod
    def _write_to_db(session: Session, object: Base) -> Base:
        session.add(object)
        try:
            session.commit()
            session.refresh(object)
        except IntegrityError:
            session.rollback()
            print(
                f"Table '{object.__tablename__}' already contains an entry for value '{object}'."
            )
        return object

    def add_project(self, project_name: str) -> t.Optional[int]:
        """
        Add a row to the projects table.
        :param project_name: Name of the project.
        :return: id of the added row. If the project already exists, returns None
        """
        project = self._write_to_db(self.session, Projects(project_name=project_name))
        return project.id

    def add_classes(self, label: str, project_id: int) -> int:
        """
        Add a row to the classes table.
        :param label: The name of the class.
        :param project_id: The id of the project this class belongs to
        :return: id of the added row. If the row already exists, returns None
        """
        classes = self._write_to_db(
            self.session, Classes(label=label, project_id=project_id)
        )
        return classes.id

    def add_images(self, blob_storage_uid: str, classes_id: int) -> int:
        """
        Add a row to the images table.
        :param blob_storage_uid: The URL of the blob in azure.
        :param classes_id: The id of class that defines the label of the image
        :return: id of the added row. If the row already exists, returns None
        """
        image = self._write_to_db(
            self.session,
            Images(blob_storage_uid=blob_storage_uid, classes_id=classes_id),
        )
        return image.blob_storage_uid

    def add_checkpoints(self, project_id: int, checkpoint_blob_storage_uid: str) -> int:
        """
        Add a row to the images table.
        :param blob_storage_uid: The URL of the blob in azure.
        :param classes_id: The id of class that defines the label of the image
        :return: id of the added row. If the row already exists, returns None
        """
        checkpoint = self._write_to_db(
            self.session,
            Checkpoints(
                project_id=project_id,
                checkpoint_blob_storage_uid=checkpoint_blob_storage_uid,
            ),
        )
        return checkpoint.id
