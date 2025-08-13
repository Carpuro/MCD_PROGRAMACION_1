# Programación 1 – Histogramas (Docker-ready)

This repository provides a Dockerized Python 3.11 environment with pandas and matplotlib.
It plots histograms from a CSV and saves PNG files to `output/`.

## Quick start (build locally)

```bash
docker build -t programacion1:latest .
docker run --rm -v ${PWD}/data:/app/data -v ${PWD}/output:/app/output programacion1:latest