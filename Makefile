IMAGE_NAME := ai_beats
TAG ?= latest

ai_beats:
	make music music_continuation image video audio_clip

music:
	docker run --rm \
	-v $(PWD)/beats/:/app/beats/ \
	-v $(HOME)/.cache/huggingface/:/root/.cache/huggingface/ \
	${IMAGE_NAME}:${TAG} \
	python src/music.py

music_continuation:
	docker run --rm \
	-v $(PWD)/beats/:/app/beats/ \
	-v $(HOME)/.cache/huggingface/:/root/.cache/huggingface/ \
	${IMAGE_NAME}:${TAG} \
	python src/music_continuation.py

image:
	docker run --rm \
	-v $(PWD)/beats/:/app/beats/ \
	-v $(HOME)/.cache/huggingface/:/root/.cache/huggingface/ \
	${IMAGE_NAME}:${TAG} \
	python src/image.py

video:
	docker run --rm \
	-v $(PWD)/beats/:/app/beats/ \
	-v $(HOME)/.cache/huggingface/:/root/.cache/huggingface/ \
	${IMAGE_NAME}:${TAG} \
	python src/video.py

audio_clip:
	docker run --rm \
	-v $(PWD)/beats/:/app/beats/ \
	${IMAGE_NAME}:${TAG} \
	python src/audio_clip.py

build:
	docker build -t ${IMAGE_NAME}:${TAG} .

lint:
	isort ./src
	black ./src
	flake8 ./src
	mypy --ignore-missing-imports ./src