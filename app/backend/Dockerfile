FROM python:3.12-slim

WORKDIR /workspace
COPY pyproject.toml README.md schema.yaml ./
COPY app ./app
COPY public/notes ./public/notes
# The extraction agent's guidelines, for the private refresh after the interview commands.
COPY docs/extraction-guidelines.md docs/extraction-examples.yaml ./docs/
RUN pip install --no-cache-dir .

EXPOSE 8000
CMD ["uvicorn", "app.backend.knowledge_radar.api:app", "--host", "0.0.0.0", "--port", "8000"]
