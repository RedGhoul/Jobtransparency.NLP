FROM continuumio/miniconda3
ADD . /code
WORKDIR /code
RUN conda install -c intel mkl_fft
RUN conda install numpy
RUN conda install -c conda-forge rake_nltk
RUN pip install -r requirements.txt
EXPOSE 8080
CMD python base.py