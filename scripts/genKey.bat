@echo off

echo "Creating folder"
mkdir "../cert/"

echo "Creating RSA key pair..."
openssl genrsa -out ../cert/server.key 2048
openssl req -new -key ../cert/server.key -out ../cert/server.csr -subj "/C=US/ST=State/L=City/O=TestOrg/OU=TestUnit/CN=localhost"
openssl x509 -req -days 3650 -in ../cert/server.csr -signkey ../cert/server.key -out ../cert/server.crt

echo "Verifying..."
openssl x509 -in ../cert/server.crt -text -noout

echo "Done."
pause >nul
