#   Copyright 2022 Filip Strajnar
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

# Quickly write to a file
def safe_write(file_path,content):
  f=open(file_path, "w", encoding="utf-8")
  f.write(content)
  f.close()

certificate_docker_compose=f'''#   Copyright 2021 Filip Strajnar
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

certificate_compose_path=os.path.join("Certbot","docker-compose.yaml")
https_compose_path=os.path.join("conf.d","https.conf")
safe_write(certificate_compose_path,certificate_docker_compose)

def https_template(to_insert: str) -> str:
  return r"""server {
    listen       443 ssl;
    server_name  """ + cert_domain + r""";
    ssl_certificate     /certificate/fullchain.pem;
    ssl_certificate_key /certificate/privkey.pem;

    """ + to_insert + r"""
}"""

# Branch
if file_or_proxy == "static":
  insertion=r"""location / {
        root   /usr/share/nginx/static;
        index  index.html;
    }"""
  safe_write(https_compose_path,https_template(insertion))
elif file_or_proxy == "proxy":
  insertion=r"""location / {
        proxy_pass   """ + location + r""";
    }"""
  safe_write(https_compose_path,https_template(insertion))
