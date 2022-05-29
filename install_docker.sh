#!/bin/bash
# 川隅君が作成したdockerのインストールshファイル
# 基本的に公式サイトでのインストールで事足りるので参照しなくてもよい
# ただしnvidia製GPUユーザーの場合は，"nvidia-docker"を別途入れる必要があるかもなので
# ここの34-40行目 or 公式サイトから導入する必要があるかも(未調査, 会までに調査間に合ったら案内したい)

sudo apt-get update
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update
sudo apt-get install -y docker-ce

COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d\" -f4)
sudo curl -L "https://github.com/docker/compose/releases/download/"$COMPOSE_VERSION"/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo docker run hello-world

# コンテナ内でctrl-pを二度押ししなくて良くなる設定
mkdir /home/$USER/.docker/
echo -e '{\n    "detachKeys": "ctrl-\\\\"\n}\n' >> /home/$USER/.docker/config.json

# nvidia環境でgpusオプションが扱えるようになるコード
# Intel環境に入れても無駄だけどエラーは起こさないみたい
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit

#dockerをパスワードなしで動作するよう設定
sudo gpasswd -a $USER docker
sudo service docker restart
echo "sudo無しでdockerコマンドを使用するために, コンピューターを再起動してください."

