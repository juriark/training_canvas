# Dummy fastapi setup to check connections
from fastapi import FastAPI
import typing as t
from azure.storage.blob import BlobServiceClient

app = FastAPI()


# # Test db connection works
# def _get_engine():
#     connection_string = f"postgresql://postgres:postgres@172.18.0.1:5432/postgres"
#     engine = create_engine(connection_string)
#     return engine


@app.get("/")
def read_root():
    # return {"Hello": os.getenv("AZURITE_ACCOUNT_KEY")}
    return {"hello": "you again"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: t.Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/create_container")
def create_container(container_name: str):
    connection_string = "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=http://172.18.0.1:10000/devstoreaccount1;"

    # Create container
    blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(
        connection_string
    )
    blob_service_client.create_container(container_name)

    # # Upload blob to that container
    # blob_client: BlobClient = BlobClient.from_connection_string(connection_string, container_name="test-container", blob_name="test-blob")
    # blob_client.upload_blob(blob_to_write)


# if __name__ == "__main__":
#     engine = _get_engine()
#     with engine.connect() as con:
#         # statement = text("""INSERT INTO project (id, project_name) VALUES (2, 'some_project');""")
#         print(con.execute(text('SELECT * FROM project')).all())
