import logging

from azure.core.exceptions import ResourceExistsError
from azure.storage.blob import BlobServiceClient

from training_canvas.blob_storage.blob_storage import BlobStorageContainerNameEnum
from training_canvas.connection import AZURE_CONNECTION_STRING

_logger = logging.getLogger("__name__")
_logger.setLevel(logging.DEBUG)


def _azure_setup():
    """Create azure containers"""
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(
        AZURE_CONNECTION_STRING
    )
    for container_name in BlobStorageContainerNameEnum:
        try:
            container = blob_service_client.create_container(container_name.value)
            _logger.info(f"Successfully created azure container {container}.")
        except ResourceExistsError:
            _logger.info(f"Azure container '{container_name}' already exists.")
            pass


if __name__ == "__main__":
    _azure_setup()
