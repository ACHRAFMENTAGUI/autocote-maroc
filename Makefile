.PHONY: install lint test train run-app clean help

help:
	@echo "Available commands:"
	@echo "  make install  : Install dependencies in editable mode"
	@echo "  make lint     : Run code style checks (ruff)"
	@echo "  make test     : Run unit and integration tests (pytest)"
	@echo "  make train    : Run model training with MLflow tracking"
	@echo "  make run-app  : Launch Streamlit web dashboard"
	@echo "  make clean    : Remove cached and temporary files"

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

lint:
	ruff check .

test:
	pytest tests/ -v

train:
	python -m src.models.train

run-app:
	streamlit run app/streamlit_app.py

clean:
	python -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('__pycache__')]"
	python -c "import pathlib, shutil; [shutil.rmtree(p) for p in pathlib.Path('.').rglob('.pytest_cache')]"
