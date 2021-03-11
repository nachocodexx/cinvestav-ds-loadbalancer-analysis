FROM python:3
WORKDIR /usr/src/app
COPY main.py ./
RUN mkdir /usr/src/app/bins
COPY ./bins/generator ./bins/
COPY ./bins/single ./bins/
COPY requirements.txt ./
RUN echo $(pwd)
RUN pip install --no-cache-dir -r requirements.txt
#RUN pip install -r requirements.txt
CMD ["python","main.py"]
