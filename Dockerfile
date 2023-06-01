FROM fedora:36

RUN dnf update
RUN dnf install -y --no-install-recommends tcl-devel
RUN dnf install -y --no-install-recommends boost-devel
RUN dnf install -y --no-install-recommends git
RUN dnf install -y --no-install-recommends cmake
RUN dnf install -y --no-install-recommends make
RUN dnf install -y --no-install-recommends gcc-c++
RUN dnf install -y --no-install-recommends python3-devel
RUN dnf clean all -y

FROM ghcr.io/epitech/coding-style-checker:latest

RUN pip install pylint==2.10.2
RUN pip cache purge

ENTRYPOINT /bin/bash
