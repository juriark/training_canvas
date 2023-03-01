from sqlalchemy import create_engine

# Consider reading from config.toml or docker network itself (if possible)
HOST = "172.18.0.1"

# blob storage
AZURE_CONNECTION_STRING: str = (
    "DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;"
    "AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;"
    f"BlobEndpoint=http://{HOST}:10000/devstoreaccount1;"
)

# database
connection_string = f"postgresql://postgres:postgres@{HOST}:5432/postgres"
db_engine = create_engine(connection_string)
