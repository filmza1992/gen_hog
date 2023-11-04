FROM python:3.10.6

# 
WORKDIR /FirstContainer

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 -y

# 
COPY ./requirements.txt /FirstContainer/requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /FirstContainer/requirements.txt

# 
COPY ./app /FirstContainer/app


ENV PYTHONPATH "${PYTHONPATH}:/FirstContainer"

# a
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]