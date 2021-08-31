FROM locustio/locust

# Install requirements
RUN pip3 install pytest

COPY . /testing
COPY locustfile.py /locustfile.py

# Shell script that runs locust and the testing http server
CMD ["/testing/cmd.sh"]
ENTRYPOINT [ "sh" ]
