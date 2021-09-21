FROM python

RUN mkdir /service
COPY proto/ /service/proto/
COPY visualizer/ /service/visualizer/
WORKDIR /service/visualizer
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../proto --python_out=. \
           --grpc_python_out=. ../proto/metrics.proto

EXPOSE 5000
ENV FLASK_APP=visualize.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]