IMAGE_TAG ?= latest
IMAGE ?= training-canvas:${IMAGE_TAG}

build:
	docker build --tag "${IMAGE}" .

shell:
	docker run -it \
    -v ~/Projects/training_canvas:/app ${IMAGE}

typecheck:
	docker run -v ~/Projects/training_canvas/src:/app/src ${IMAGE} mypy src/

lint:
	docker run -v ~/Projects/training_canvas/src:/app/src ${IMAGE} pylint src/

black:
	docker run -v ~/Projects/training_canvas/src:/app/src ${IMAGE} black src/

# TODO:
#  setup
#    - docker compose
#    - alembic upgrade head
#    - _azure_setup()
#    - optional: upload SketchDataset to blob storage (for that data needs to be stored on local device)
