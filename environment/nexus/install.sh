#!/usr/bin/bash

## On met à jour le systeme pour pouvoir installer

sudo apt update -y

## On installe le pré-requis Java

sudo apt install -y openjdk-8-jdk

useradd -M -d /opt/nexus -s /bin/bash -r nexus
echo "nexus   ALL=(ALL)       NOPASSWD: ALL" > /etc/sudoers.d/nexus

wget https://sonatype-download.global.ssl.fastly.net/repository/downloads-prod-group/3/nexus-3.29.2-02-unix.tar.gz

mkdir /opt/nexus

tar xzf nexus-3.29.2-02-unix.tar.gz -C /opt/nexus --strip-components=1

chown -R nexus: /opt/nexus

sed -i 's/#run_as_user=""/run_as_user="nexus"/' /opt/nexus/bin/nexus.rc

## On modifie la configuration pour qu'elle fonctionne

sudo sed -i 's/..\/sonatype-work/.\/sonatype-work/g' /opt/nexus/bin/nexus.vmoptions
sudo sed -i 's/2073/1024/g' /opt/nexus/bin/nexus.vmoptions

sudo -u nexus /opt/nexus/bin/nexus start

## Service

cat > /etc/systemd/system/nexus.service << 'EOL'
[Unit]
Description=nexus service
After=network.target
[Service]
Type=forking
LimitNOFILE=65536
ExecStart=/opt/nexus/bin/nexus start
ExecStop=/opt/nexus/bin/nexus stop
User=nexus
Restart=on-abort
[Install]
WantedBy=multi-user.target
EOL

sudo /opt/nexus/bin/nexus stop
systemctl daemon-reload
systemctl enable --now nexus.service

## On attend que la config de Nexus se termine, on le stop, on modifie le port par défaut de Nexus sur 8086 et on le start

sleep 180
sudo /opt/nexus/bin/nexus stop
sudo sed -i 's/# application-port=8081/application-port=8086/' /opt/nexus/sonatype-work/nexus3/etc/nexus.properties
sudo sed -i 's/# application-host=0.0.0.0/application-host=192.168.0.101/' /opt/nexus/sonatype-work/nexus3/etc/nexus.properties
systemctl daemon-reload
systemctl enable --now nexus.service

## On active le firewall, on ouvre le port 8086 et les connexions ssh

yes | sudo ufw enable
sudo ufw allow 8086/tcp
sudo ufw allow ssh

## Afficher le mot de passe

echo 'Mot de passe admin \n'
cat /opt/nexus/sonatype-work/nexus3/admin.password
echo '\n\n'