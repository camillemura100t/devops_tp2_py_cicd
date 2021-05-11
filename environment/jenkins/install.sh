#!/bin/bash

## On met à jour le systeme pour pouvoir installer

sudo apt update -y

## On installe le pré-requis Java

sudo apt install -y openjdk-11-jdk

## On installe la version stable de Jenkins et ses prérequis en suivant la documentation officielle : https://www.jenkins.io/doc/book/installing/linux

wget -q -O - https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
sudo sh -c 'echo deb https://pkg.jenkins.io/debian-stable binary/ > \
	/etc/apt/sources.list.d/jenkins.list'
sudo apt -y update
sudo apt -y install jenkins

## On modifie le port par défaut de Jenkins sur 8087

sudo sed -i 's/HTTP_PORT=8080/HTTP_PORT=8087/' /etc/default/jenkins

## Démarrer le service Jenkins

sleep 10

sudo systemctl daemon-reload
sudo systemctl stop jenkins
sudo systemctl start jenkins

## Créer un utilisateur userjob avec son home sur la partition créé

sudo mkdir -p /home/userjob
sudo useradd -m userjob -d /home/userjob

## Lui donner les permissions (via le fichier sudoers) d'utiliser apt (et seulement apt pas l'ensemble des droits admin)

echo 'userjob ALL=(ALL:ALL) /usr/bin/apt' | sudo EDITOR='tee -a' visudo

## On active le firewall, on ouvre le port 8087 et les connexions ssh

yes | sudo ufw enable
sudo ufw allow 8087/tcp
sudo ufw allow ssh

## Afficher à la fin de l'execution du script le contenu du fichier /var/lib/jenkins/secrets/initialAdminPassword pour permettre de récupérer le mot de passe

echo 'Mot de passe admin \n'
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
echo '\n\n'