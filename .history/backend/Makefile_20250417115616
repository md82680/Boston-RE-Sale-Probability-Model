.PHONY: test
test:
	pytest tests/ -v

.PHONY: test-cov
test-cov:
	pytest tests/ --cov=api --cov-report=term-missing

.PHONY: test-cov-html
test-cov-html:
	pytest tests/ --cov=api --cov-report=html 