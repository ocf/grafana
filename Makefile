DOCKER_REVISION ?= grafana-testing-$(USER)
DOCKER_TAG = docker-push.ocf.berkeley.edu/grafana:$(DOCKER_REVISION)
RANDOM_PORT := $(shell expr $$(( 8000 + (`id -u` % 1000) + 2 )))

# OCF-UPDATE-CHECK relmon=13916
GF_VERSION := 8.4.3

.PHONY: dev
dev: cook-image
	@echo "Will be accessible at http://$(shell hostname -f ):$(RANDOM_PORT)/"
	docker run --rm -p "$(RANDOM_PORT):3000" "$(DOCKER_TAG)"

.PHONY: cook-image
cook-image:
	docker build --build-arg grafana_version=$(GF_VERSION) --pull -t $(DOCKER_TAG) .

.PHONY: push-image
push-image:
	docker push $(DOCKER_TAG)
