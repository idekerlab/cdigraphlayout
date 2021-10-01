FROM continuumio/miniconda3

RUN conda install -y -c conda-forge python-igraph


RUN mkdir /tmp/cdigraphlayout
COPY dist/*.whl /tmp/cdigraphlayout

RUN /opt/conda/bin/pip install /tmp/cdigraphlayout/cdigraphlayout*whl

RUN rm -rf /tmp/cdigraphlayout


ENTRYPOINT ["/opt/conda/bin/cdigraphlayoutcmd.py"]
CMD ["--help"]
