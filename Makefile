.PHONY: help install run-api run-web run-desktop build-index clean

help:
	@echo "Available commands:"
	@echo "  install        - Install dependencies"
	@echo "  run-api        - Start FastAPI backend"
	@echo "  run-web        - Start Streamlit web app"
	@echo "  run-desktop    - Start PyQt5 desktop app"
	@echo "  build-index    - Build Pinecone index from documents"
	@echo "  clean          - Remove __pycache__ and .pyc files"

install:
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm

run-api:
	uvicorn backend.main:app --host 0.0.0.0 --port 8000

run-web:
	streamlit run frontend/web/app.py

run-desktop:
	python -m frontend.app.agriboot_desktop

build-index:
	python scripts/build_index.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
	find . -type f -name "*.pyc" -delete