


mkdir -p ssl


IP=$(ip route get 1.1.1.1 | awk '{print $7}') && \
openssl req -x509 -newkey rsa:2048 \
  -nodes \
  -keyout ssl/key.pem \
  -out ssl/cert.pem \
  -days 3650 \
  -subj "/CN=$IP" \
  -addext "subjectAltName=IP:$IP,DNS:localhost"