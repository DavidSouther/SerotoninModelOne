docker build -t serotonin .
docker run -v $(PWD)/figures:/usr/lib/serotonin/figures $@ serotonin
