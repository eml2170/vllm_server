# vllm_server
Example implementation of a vllm server to extract diagnoses from medical notes. Uses Gemma-2b for proof-of-concept, but should be swapped out for a larger/biomedical-tuned model.

## Usage
Create virtual env and install requirements: `pip install -r requirements.txt`.
Run the server: `python code/server.py`.
Test a request: `curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{"clinical_note": "Patient presents with fever and cough"}'`.

## Docker
Build container with `docker build --platform linux/arm64 -t llm-server .`.
Run container with `docker run -p 5000:5000 llm-server`.

TODO: base docker image currently doesn't support Apple Silicon (i.e. will not build on a macbook).