docker-build:
	docker build -f Dockerfile . -t akhmetov/python-telegram

docker-send-message:
	docker run -i -t \
				-v /tmp/docker-python-telegram/:/tmp/ \
				akhmetov/python-telegram \
				python3 /app/examples/send_message.py $(API_ID) $(API_HASH) $(PHONE) $(CHAT_ID) $(TEXT)

docker-echo-bot:
	docker run -i -t \
				-v /tmp/docker-python-telegram/:/tmp/ \
				akhmetov/python-telegram \
				python3 /app/examples/echo_bot.py $(API_ID) $(API_HASH) $(PHONE)

docker-get-instant-view:
	docker run -i -t \
				-v /tmp/docker-python-telegram/:/tmp/ \
				akhmetov/python-telegram \
				python3 /app/examples/echo_bot.py $(API_ID) $(API_HASH) $(PHONE)


release-pypi:
	test -n "$(VERSION)"
	python setup.py sdist
	twine upload dist/python-telegram-$(VERSION).tar.gz
