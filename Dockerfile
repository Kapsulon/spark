FROM fedora:36

RUN dnf update -y
RUN dnf install -y tcl-devel
RUN dnf install -y boost-devel
RUN dnf install -y git
RUN dnf install -y cmake
RUN dnf install -y make
RUN dnf install -y gcc-c++
RUN dnf install -y python3-devel
RUN dnf clean all -y

FROM ghcr.io/epitech/coding-style-checker:latest

RUN pip install pylint==2.10.2
RUN pip cache purge

ENTRYPOINT /bin/bash
