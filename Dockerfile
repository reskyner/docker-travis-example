# pull base container with miniconda in it:
FROM continuumio/miniconda

# use bash from now on
SHELL ["/bin/bash", "-c"]

# make a place to work and copy code in
RUN mkdir /immunocore
WORKDIR /immunocore
COPY . /immunocore
RUN chmod 775 run_tests.sh
