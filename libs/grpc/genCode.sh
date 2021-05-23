#!/bin/bash

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. talent.proto
python -m grpc_tools.protoc -I. --python_betterproto_out=. talent.proto
