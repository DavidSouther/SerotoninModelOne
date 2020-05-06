docker build -t serotonin .
docker run -v %cd%/figures:/usr/lib/serotonin/figures serotonin
