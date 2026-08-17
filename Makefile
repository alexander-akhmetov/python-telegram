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

# Publishing to PyPI happens in .github/workflows/release.yml, through trusted
# publishing, when a version tag is pushed. There is no manual upload target.
.PHONY: release
release:
	@echo "Bump __version__ in telegram/__init__.py, merge it, then push the tag:"
	@echo "  git tag <version> && git push origin <version>"
