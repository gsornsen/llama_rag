VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip3
CHAINLIT := $(VENV)/bin/chainlit

.PHONY: env run

env:
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

run:
	$(CHAINLIT) run src/chat_agent.py -h
