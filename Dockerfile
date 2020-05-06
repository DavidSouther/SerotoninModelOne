# Use a ubuntu base image and install the most up-to-date python
FROM ubuntu:20.04
RUN apt-get update && apt-get install --no-install-recommends --yes python3 python3-pip

WORKDIR /usr/lib/serotonin

# Before adding the entire working directory, install pip requirements.
# This keeps it in a separate phase, so it doesn't need to re-run pip every time any
# other code changes.
ADD requirements.txt ./
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Add the entire project, set some environment variables that will be used for flag
# default values, and run in PLOT mode.
ADD . .
ENV FIGURES_DIRECTORY=/usr/lib/serotonin/figures
CMD [ "python3", "./app.py", "--mode=PLOT" ]
