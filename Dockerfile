FROM ubuntu
RUN apt update
RUN apt -y install python3 python3-pip
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python-headless
RUN pip3 install -i https://pypi.tuna.tsinghua.edu.cn/simple flask
ENV LD_LIBRARY_PATH=/root/seetaFace6Python/seetaface/lib/ubuntu
ADD ./sf3.0_models/* /root/seetaFace6Python/seetaface/model/
ENV SEETAFACE6_PYTHON_VERSION=1.3
ADD ./seetaFace6Python /root/seetaFace6Python
WORKDIR /root/seetaFace6Python
EXPOSE 8080
ENTRYPOINT ["python3","main.py"]