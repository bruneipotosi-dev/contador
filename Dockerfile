FROM python:3.14-slim
WORKDIR /usr/local/app


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py ./
RUN useradd --system --create-home --shell /usr/sbin/nologin --uid 1000 appuser
USER appuser

CMD ["python", "app.py"]
EXPOSE 5000