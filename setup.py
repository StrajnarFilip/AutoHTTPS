from encodings import utf_8
import sys
import os

# Example invocation:
# python3 setup.py "my.domain.com" "my@email.com" "static"
# python3 setup.py "my.domain.com" "my@email.com" "proxy" "http://127.0.0.1:5000"

# First argument is domain
cert_domain=sys.argv[1]
# Second is email
cert_email=sys.argv[2]
# Static files or proxy (static OR proxy)
file_or_proxy=sys.argv[3]
# Location, example: http://127.0.0.1:5000
location=sys.argv[4]

new_certbot_compose=f'''#   Copyright 2021 Filip Strajnar
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
      user_email: "{cert_email}"
      user_domain: "{cert_domain}"
    entrypoint: "sh"
    command: "/script/script.sh"'''

cert_compose_path=os.path.join("Certbot","docker-compose.yaml")
cert_dockercompose_file=open(cert_compose_path, "w", encoding=utf_8)
cert_dockercompose_file.write(new_certbot_compose)

insertion=""
# Branch
if file_or_proxy == "static":
  insertion="""location / {
        root   /usr/share/nginx/static;
        index  index.html;
    }"""
elif file_or_proxy == "proxy":
  insertion="""location / {
        proxy_pass   {location};
    }"""

https_template="""server {
    listen       443 ssl;
    server_name  {cert_domain};
    ssl_certificate     /certificate/fullchain.pem;
    ssl_certificate_key /certificate/privkey.pem;

    {insertion}
}"""

https_compose_path=os.path.join("conf.d","https.conf")
https_conf_file=open(https_compose_path, "w", encoding=utf_8)
https_conf_file.write(https_template)