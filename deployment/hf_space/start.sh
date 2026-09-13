
#!/bin/bash

set -e

echo "Starting FastAPI..."

uvicorn app:app \
    --host 127.0.0.1 \
    --port 8000 &


echo "Starting Streamlit..."

exec streamlit run streamlit.py \
    --server.address=0.0.0.0 \
    --server.port=7860 \
    --server.headless=true
