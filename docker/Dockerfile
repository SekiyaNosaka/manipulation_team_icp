#FROM nvidia/cuda:11.4.2-devel-ubuntu20.04
FROM ubuntu:18.04

# コンテナにプロキシ環境変数を追加
# ENV https_proxy "http://wwwproxy.kanazawa-it.ac.jp:8080"
# ENV http_proxy "http://wwwproxy.kanazawa-it.ac.jp:8080"

# rosのインストール時にtzdataのタイムゾーン選択で止まらないように
ENV DEBIAN_FRONTEND=noninteractive

# aptを日本のミラーに設定
RUN sed -i.bak -e "s/http:\/\/archive\.ubuntu\.com/http:\/\/jp\.archive\.ubuntu\.com/g" /etc/apt/sources.list

# 基本的なaptパッケージのインストール
RUN apt-get update
# sudo: sudo用  
# x11-apps: xeyes用
# net-tools: ifconfig用
# mesa-utils: glxgears用
# gnupg: rosのadd-key用
# eog: jpeg, png, gif等の画像可視化用
RUN apt-get install -y curl \
    sudo \
    gnupg \
    x11-apps \
    iputils-ping \
    net-tools \
    mesa-utils \
    dbus-x11 \
    vim \
    eog

# 使用ソフトの諸々インストール
RUN apt-get install -y python3 \
    python3-pip \
    libjpeg-dev \
    zlib1g-dev \
    meshlab \
    pcl-tools
RUN pip3 install open3d==0.8.0
RUN pip3 install matplotlib

# aptのキャッシュを削除してイメージの容量削減
RUN rm -rf /var/lib/apt/lists/

