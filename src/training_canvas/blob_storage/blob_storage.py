import io
import uuid
from pathlib import Path
from enum import Enum

import torch
from PIL import Image
from azure.storage.blob import ContainerClient, BlobClient
from sqlalchemy.exc import IntegrityError
from torchvision import transforms

from training_canvas.connection import AZURE_CONNECTION_STRING
from training_canvas.database.connection import TrainingCanvasDB


class BlobStorageContainerNameEnum(Enum):
    IMAGES = "images"
    CHECKPOINTS = "checkpoints"


def upload_file_to_blob_storage(
    file_path: Path, container: BlobStorageContainerNameEnum, classes_id: int
) -> BlobClient:
    """
    Uploads a file to blob storage, and adds an entry to the Images table in database.
    :param file_path: File to upload.
    :param container: Container to upload the file to.
    :param classes_id: id of the related entry in the Classes table
    :return: The blob with which to interact.
    """
    # Upload to blob
    blob_container_client: ContainerClient = ContainerClient.from_connection_string(
        conn_str=AZURE_CONNECTION_STRING, container_name=container.value
    )
    with open(file_path, "rb") as file:
        blob: BlobClient = blob_container_client.upload_blob(
            name=str(uuid.uuid4()), data=file
        )

    # Write to database
    with TrainingCanvasDB() as db:
        try:
            db.add_images(blob_name=blob.blob_name, classes_id=classes_id)
        except IntegrityError:
            print(
                f"Failed to write to Images table: blob_name={blob.blob_name}', class_id{classes_id}."
                "Reverting changes."
            )
            blob_container_client.delete_blob(name=blob.blob_name)

    print(f"Successfully uploaded {file_path=} to blob storage, {blob.url}, and added a database entry.")

    return blob


def download_image_from_azure(blob_name: str) -> torch.Tensor:
    blob_container_client: ContainerClient = ContainerClient.from_connection_string(
        conn_str=AZURE_CONNECTION_STRING, container_name=BlobStorageContainerNameEnum.IMAGES.value
    )
    img_content = blob_container_client.download_blob(blob_name).readall()
    with Image.open(io.BytesIO(img_content)) as image:
        tensor = transforms.PILToTensor()(image)
    return tensor
