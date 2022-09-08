FROM continuumio/anaconda3

WORKDIR /usr/src

# Create env
COPY environment.yml .
SHELL ["/bin/bash", "-c"]
RUN conda env create -f environment.yml


COPY data data
COPY models models
COPY static static
COPY templates templates
COPY text_lines text_lines
COPY utils utils
COPY neural_style_transfer.py neural_style_transfer.py
COPY app.py app.py

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "pytorch-nst", "python", "app.py"]

