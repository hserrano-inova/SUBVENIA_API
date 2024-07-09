FROM python:3.11-slim

WORKDIR /opt/SUBVIA

#RUN apt-get update && apt-get install -y \
#    uvicorn \
#    gunicorn \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/*

#RUN useradd -m evalia

COPY requirements.txt ./

#RUN chown -R evalia:evalia /opt/EVALIA

#USER evalia

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8001

# Comando para correr la aplicación con Gunicorn
#CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "main:app"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "2"]
#CMD ["/bin/bash"]
