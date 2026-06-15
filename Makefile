.PHONY: install run migrate test docker-build docker-run docker-stop

VERSION=1.0.0
IMAGE_NAME=student-api

install:
	pip install -r requirements.txt

run:
	flask db upgrade && python run.py

test:
	pytest tests/ -v

docker-build:
	docker build -t $(IMAGE_NAME):$(VERSION) .

docker-run:
	docker run -d \
		--name student-api \
		-p 5000:5000 \
		-e DATABASE_URL=sqlite:///students.db \
		-e LOG_LEVEL=INFO \
		$(IMAGE_NAME):$(VERSION)

docker-stop:
	docker stop student-api
	docker rm student-api