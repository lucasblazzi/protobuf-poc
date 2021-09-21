FROM python

RUN mkdir /service
COPY proto/ /service/proto/
COPY prices/ /service/prices/
WORKDIR /service/prices
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../proto --python_out=. \
           --grpc_python_out=. ../proto/metrics.proto

ENTRYPOINT [ "python", "app.py" ]