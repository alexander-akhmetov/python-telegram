docker-build:
	docker build -f Dockerfile . -t akhmetov/python-telegram

docker-send-message:docker-build
	docker run -i -t akhmetov/python-telegram python3 /app/examples/send_message.py $(API_ID) $(API_HASH) $(PHONE) $(CHAT_ID) $(TEXT)

release-pypi:
	test -n "$(VERSION)"
	python setup.py sdist
	twine upload dist/python-telegram-$(VERSION).tar.gz
