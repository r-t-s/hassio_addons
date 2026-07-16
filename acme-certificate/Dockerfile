ARG BUILD_FROM
FROM $BUILD_FROM

# Copy data for add-on
COPY run.sh run.py notify.sh /
RUN apk add --no-cache python3 openssl git
RUN git clone https://github.com/acmesh-official/acme.sh.git
RUN chmod a+x /run.sh /run.py /notify.sh
RUN ln -s /homeassistant /config

CMD [ "/run.sh" ]