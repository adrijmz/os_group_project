IMAGE_NAME = os_group_project
TAG_NAME = latest
PORT = 5000

build:
	docker build -t $(IMAGE_NAME):$(TAG_NAME) -f docker/Dockerfile .

run:
	docker run -p $(PORT):$(PORT) $(IMAGE_NAME):$(TAG_NAME)

shell:
	docker run -it $(IMAGE_NAME):$(TAG_NAME) /bin/bash
