FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY server.py .
RUN useradd --create-home --uid 10001 bridgeuser && mkdir -p /app/data/strategytune_reports /app/data/research_inbox && chown -R bridgeuser:bridgeuser /app
USER bridgeuser
EXPOSE 8000
CMD ["python", "server.py"]
