


mkdir -p ssl


openssl req -x509 -newkey rsa:4096 \
    -keyout ssl/key.pem \
    -out ssl/cert.pem \
    -days 3650 \
    -nodes


openssl x509 -in ssl/cert.pem -noout -fingerprint -sha256 \
| cut -d= -f2 \
> ssl/fingerprint.txt

# | tr -d ':' \
# | tr 'A-F' 'a-f' \

