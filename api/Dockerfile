FROM python:3.9

# Copy app
ADD . /api
WORKDIR /api

# Install requirements
RUN pip3 install -r requirements.txt

# Assuming worse case scenario of 1 CPU core, if you want to optimize for your machine
# please change the number after the "-w" parameter to the result of this expression: (2*CPU_CORES)+1

CMD ["gunicorn", "-w", "3", "-b", ":5000", "app:app"]