FROM python:3.11.1-alpine

LABEL maintainer="olehoryshshuk@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/apps

COPY requirements.txt ./

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]