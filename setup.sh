#!/bin/bash

# Example invocation:
# setup.sh "my.domain.com" "my@email.com" "static"
# setup.sh "my.domain.com" "my@email.com" "proxy" "http://127.0.0.1:5000"

# First argument is domain
cert_domain=$1
# Second is email
cert_email=$2
# Static files or proxy (static OR proxy)
file_or_proxy=$3
# Location, example: http://127.0.0.1:5000
location=$4

new_certbot_compose='#   Copyright 2021 Filip Strajnar
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# Certificate will be inside ./certificate/fullchain.pem
# Private key will be inside ./certificate/privkey.pem
#
version: "3.3"
services:
  certbotcert:
    image: certbot/certbot
    ports:
      - "0.0.0.0:80:80"
      - "0.0.0.0:443:443"
    volumes:
      - ./letsencrypt:/etc/letsencrypt
      - ./var:/var
      - ./certificate:/certificate
      - ./script:/script
    environment:
      user_email: '$cert_email'
      user_domain: '$cert_domain'
    entrypoint: "sh"
    command: "/script/script.sh"'

echo $new_certbot_compose > ./Certbot/docker-compose.yaml

# Branch
if test $file_or_proxy = "static" ; then
  insertion="location / {
        root   /usr/share/nginx/static;
        index  index.html;
    }"
elif test $file_or_proxy = "proxy" ; then
  insertion="location / {
        proxy_pass   ${location};
    }"
fi

https_template="server {
    listen       443 ssl;
    server_name  ${cert_domain};
    ssl_certificate     /certificate/fullchain.pem;
    ssl_certificate_key /certificate/privkey.pem;

    $insertion
}"

echo $https_template > ./conf.d/https.conf

cd Certbot ; docker-compose up -d
cd .. ; docker-compose up -d