.PHONY: all citest image run test release test-release

IMAGE_NAME ?= codeclimate/python-test-reporter

all: image

citest:
	docker run \
	  --rm \
	  --env CIRCLECI \
	  --env CIRCLE_BRANCH \
	  --env CIRCLE_SHA1 \
	  --env CODECLIMATE_REPO_TOKEN \
	  --entrypoint=/bin/sh \
	  $(IMAGE_NAME) -c 'python setup.py test && codeclimate-test-reporter'

image:
	docker build --tag $(IMAGE_NAME) .

run: image
	docker run --rm $(IMAGE_NAME)

test: image
	docker run \
	  -it \
	  --rm \
	  --entrypoint=/bin/sh \
	  $(IMAGE_NAME) -c 'python setup.py test'

release: image
	docker run \
	  --rm \
	  --volume ~/.pypirc:/home/app/.pypirc \
	  --entrypoint=/bin/sh \
	  $(IMAGE_NAME) -c 'bin/release'

test-release: image
	docker run \
	  --rm \
	  --volume ~/.pypirc:/home/app/.pypirc \
	  --entrypoint=/bin/sh \
	  $(IMAGE_NAME) -c 'bin/test-release'
