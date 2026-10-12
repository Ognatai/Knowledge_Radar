FROM python:3.12-slim

# git for the Review Dashboard: the proposal branches (mounted .git) and the private
# inbox branches; the mounts belong to the host user, hence safe.directory.
RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && git config --system --add safe.directory '*'

WORKDIR /workspace
COPY pyproject.toml README.md schema.yaml ./
COPY app ./app
COPY public/notes ./public/notes
# The subject areas: the parts of the study guide.
COPY public/areas.yaml ./public/areas.yaml
# The extraction agent's guidelines, for the private refresh after the interview commands.
COPY docs/extraction-guidelines.md docs/extraction-examples.yaml ./docs/
RUN pip install --no-cache-dir ".[claude]"

EXPOSE 8000
CMD ["uvicorn", "app.backend.knowledge_radar.api:app", "--host", "0.0.0.0", "--port", "8000"]
