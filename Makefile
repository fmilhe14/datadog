COMPOSE = docker-compose -p datadog

.PHONY: run
run:
	$(COMPOSE) build app
	$(COMPOSE) up app

.PHONY: test-unit
test-unit:
	$(COMPOSE) build test-unit
	$(COMPOSE) run test-unit

.PHONY: test
test: test-unit

