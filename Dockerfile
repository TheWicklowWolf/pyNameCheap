FROM python:3.12-alpine

# Set build arguments
ARG RELEASE_VERSION
ENV RELEASE_VERSION=${RELEASE_VERSION}

# Create User
ARG UID=1001
ARG GID=1001
RUN addgroup -g $GID general_user && \
    adduser -D -u $UID -G general_user -s /bin/sh general_user

# Create directories
COPY . /pynamecheap
WORKDIR /pynamecheap

# Install requirements and run code as general_user
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
USER general_user
CMD ["python", "pyNameCheap.py"]
