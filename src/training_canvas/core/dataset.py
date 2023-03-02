from pathlib import Path

import typing as t

import torch.nn
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query
from torch.utils.data import Dataset

from training_canvas.blob_storage.blob_storage import (
    upload_file_to_blob_storage,
    BlobStorageContainerNameEnum, download_image_from_azure,
)
from training_canvas.database.connection import TrainingCanvasDB
from training_canvas.database.orm_models import Classes, Projects, Images


class SketchDataset(Dataset):
    """
    The Sketch Dataset is used for initial training of the training canvas
    Datasource: http://cybertron.cg.tu-berlin.de/eitz/projects/classifysketch/
    """
    def __init__(
            self,
            project_title: str = "initial-training-on-sketch-dataset",
            transform: t.Optional[torch.nn.Sequential] = None
    ) -> None:
        with TrainingCanvasDB() as db:
            self.project_id: int = db.session.query(Projects.id).where(project_title==project_title).first()[0]
            self.labels: Query = db.get_classes_for_project(project_id=self.project_id)
            self.blob_name: Query = db.get_blobs_names_for_project(project_id=self.project_id)
        self.transform = transform

    def __getitem__(self, item: int):
        # Image
        image = download_image_from_azure(self.blob_name[item].blob_name)
        if self.transform:
            image = self.transform(image)

        # Label
        label = self.labels.filter(Classes.id == self.blob_name[item].classes_id).first().label
        return image, label

    def __len__(self) -> int:
        return len(self.blob_name)

    def from_local_directory(
        self,
        local_path_to_data: Path,
        project_title: str = "initial-training-on-sketch-dataset",
    ) -> None:
        """
        Upload local sketch dataset to blob storage and write blob_names and related image labels to database.
        :param local_path_to_data: Path to directory where the sketch dataset is stored
        :param project_title: Associated project title.
        :return:
        """
        class_labels: t.List[t.Optional[Classes]] = [None] * 251

        # Create project
        with TrainingCanvasDB() as db:
            try:
                project_id = db.add_project(project_title)
            except IntegrityError:  # project already exists - query it's ID
                project_id = (
                    db.session.query(Projects.id)
                    .filter(project_title == project_title)
                    .first()[0]
                )

        # Extract all labels from subdirectories
        for idx, sub_dir in enumerate(local_path_to_data.glob("*")):
            label = sub_dir.stem
            class_labels[idx] = Classes(label=label, project_id=project_id)

        with TrainingCanvasDB() as db:
            try:
                db.session.bulk_save_objects(class_labels)
                db.session.commit()
            except IntegrityError:
                print("Failed to write image labels to database. Reading them from database instead")
                db.session.rollback()
                class_labels = (
                    db.session.query(Classes).filter(project_id == project_id).all()
                )

        # Extract all images from subdirectories
        for class_label in class_labels:
            for img_name in local_path_to_data.joinpath(class_label.label).glob("*"):
                # Upload data to blob
                _ = upload_file_to_blob_storage(
                    file_path=img_name,
                    container=BlobStorageContainerNameEnum.IMAGES,
                    classes_id=class_label.id,
                )


# if __name__ == "__main__":
    # # Upload sketch dataset to blob storage, and write to database
    # if SKETCH_DIR.exists():
    #     SketchDataset.from_local_directory(SKETCH_DIR)
    # else:
    #     print(
    #         "Automatic download of sketch dataset is currently not supported. Please download the dataset manually "
    #         f"from http://cybertron.cg.tu-berlin.de/eitz/projects/classifysketch/, and save it to {SKETCH_DIR=}"
    #     )
