FROM ubuntu:latest
LABEL authors="vheekey"

ENTRYPOINT ["top", "-b"]