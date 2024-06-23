.PHONY: docker/build
docker/build:
	docker build -f Dockerfile . -t akhmetov/python-telegram

.PHONY: docker/send-message
docker/send-message:
	docker run -i -t \
				-v /tmp/docker-python-telegram/:/tmp/ \
				akhmetov/python-telegram \
				python3 /app/examples/send_message.py $(API_ID) $(API_HASH) $(PHONE) $(CHAT_ID) $(TEXT)

.PHONY: docker/echo-bot
docker/echo-bot:
	docker run -i -t \
				-v /tmp/docker-python-telegram/:/tmp/ \
				akhmetov/python-telegram \
				python3 /app/examples/echo_bot.py $(API_ID) $(API_HASH) $(PHONE)

.PHONY: docker/get-instant-view
docker/get-instant-view:
	docker run -i -t \
				-v /tmp/docker-python-telegram/:/tmp/ \
				akhmetov/python-telegram \
				python3 /app/examples/echo_bot.py $(API_ID) $(API_HASH) $(PHONE)


.PHONY: clean
clean:
	rm -rf dist

.PHONY: build-pypi
build-pypi: clean
	python3 -m build

.PHONY: release-pypi
release-pypi:build-pypi
	twine upload dist/*
