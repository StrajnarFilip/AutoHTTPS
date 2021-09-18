#!/bin/sh
certbot certonly \
--non-interactive \
--agree-tos \
--email ${user_email} \
--domain ${user_domain} \
--standalone -v \
--key-type ecdsa \
--elliptic-curve secp384r1 ;

cp /etc/letsencrypt/live/live.filips.xyz/fullchain.pem /certificate ;
cp /etc/letsencrypt/live/live.filips.xyz/privkey.pem /certificate