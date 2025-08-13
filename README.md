# MCD Programación 1 – Dockerized sessions

This repository provides a Dockerized Python 3.11 environment with pandas and matplotlib.

## Quick start (build locally)

Each session has its own program under `sessions/<nn_topic>/name.py`.  
Docker image bundles Python 3.11 with selected libraries.
d 
## Build the image

```bash
docker build -t mcd_prog1:latest .