IMAGE_NAME := ai_beats
TAG ?= latest

beats:
	make music

music:
	docker run --rm \
	-v $(PWD)/beats/:/app/beats/ \
	${IMAGE_NAME}:${TAG} \
	python src/music.py

build:
	docker build -t ${IMAGE_NAME}:${TAG} .

lint:
	isort ./src
	black ./src
	flake8 ./src
	mypy --ignore-missing-imports ./src