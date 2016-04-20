.PHONY: all clean-pyc image test test-release release run

IMAGE_NAME ?= codeclimate/python-test-reporter

all: image

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

image:
	docker build --tag $(IMAGE_NAME) .

test: image
	docker run \
	  -it \
	  --rm \
	  --entrypoint=/bin/sh \
	  $(IMAGE_NAME) -c 'python setup.py testcov'

test-release: image
	docker run \
	  --rm \
	  --volume ~/.pypirc:/home/app/.pypirc \
	  --entrypoint=/bin/sh \
	  $(IMAGE_NAME) -c 'bin/test-release'

release: image
	docker run \
	  --rm \
	  --volume ~/.pypirc:/home/app/.pypirc \
	  --entrypoint=/bin/sh \
	  $(IMAGE_NAME) -c 'bin/release' && bin/post-release

run: image
	docker run --rm $(IMAGE_NAME) --debug
