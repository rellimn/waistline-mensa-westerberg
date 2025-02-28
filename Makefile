DOCKER_IMAGE = waistline-mensa-westerberg
DOCKER_TAG = latest
JSON_OUTPUT = output.json

.PHONY: build run clean

build:
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

run:
	sudo docker run --rm -v $(shell pwd):/app $(DOCKER_IMAGE):$(DOCKER_TAG)

clean:
	-docker rmi $(DOCKER_IMAGE):$(DOCKER_TAG)
