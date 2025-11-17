#!bin/bash


# sudo docker build \
#     -t moge:latest \
#     -f dockerfile ..

sudo docker build \
    --build-arg HTTP_PROXY=http://2.2.2.110:8118 \
    --build-arg HTTPS_PROXY=http://2.2.2.110:8118 \
    -t moge:latest \
    -f dockerfile ..


# cd your_project
# docker build -t your-image-name -f docker/Dockerfile .
# 注意末尾的点(.)，它定义了构建上下文为当前目录 (your_project)

# cd your_project/docker
# 构建上下文需要指向项目根目录 ..
# docker build -t your-image-name -f Dockerfile ..


# -f 指定了 dockerfile 文件的路径