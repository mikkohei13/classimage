 
FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Add app as the last step (invalidates cache)
COPY ./app /app

#CMD [ "python", "./your-daemon-or-script.py" ]

#CMD exec /bin/bash
