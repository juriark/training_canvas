# Dummy fastapi setup to check connections

from fastapi import FastAPI
import typing as t
from azure.storage.blob import BlobServiceClient

app = FastAPI()

@app.get("/")
def read_root():
    # return {"Hello": os.getenv("AZURITE_ACCOUNT_KEY")}
    return {"hello": "you again"}


@app.get("/create_container")
def create_container(container_name: str):
    connection_string = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://172.18.0.1:10000/devstoreaccount1;"

    # Create container
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(
        connection_string
    )
    blob_service_client.create_container(container_name)
