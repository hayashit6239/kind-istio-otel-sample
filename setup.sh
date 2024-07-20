#!/bin/bash
set -e
set -o pipefail

# brew をインストール
sudo apt-get update
sudo apt-get install -y build-essential procps curl file git
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
user=`whoami`
echo 'eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"' >> /home/${user}/.profile
eval "$(/home/linuxbrew/.linuxbrew/bin/brew shellenv)"
sudo apt-get install build-essential
brew install gcc

brew install kind skaffold kubectl istioctl

# docker がなければインストール
sudo apt-get install -y docker.io
sudo systemctl start docker

# sudo なしで実行可能にする
sudo gpasswd -a ${user} docker