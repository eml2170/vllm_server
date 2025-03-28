# https://docs.vllm.ai/en/latest/deployment/docker.html
FROM vllm/vllm-openai:v0.8.0

RUN pip install vllm==0.8.0

# Copy requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-deps -r requirements.txt

# Copy server code
COPY code/server.py /app/server.py

WORKDIR /app

EXPOSE 5000

CMD ["python", "server.py"]