# Build stage
FROM nvidia/cuda:12.3.2-devel-ubuntu22.04 AS build

# Install necessary build dependencies and conda
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install Miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh

# Set up the conda environment
COPY environment.yml .
RUN /opt/conda/bin/conda env create -f environment.yml

# Activate the conda environment
SHELL ["conda", "run", "-n", "gaussian_splatting_reduced", "/bin/bash", "-c"]

# Copy your source code and build the extension
COPY . /gaussian_splatting_reduced
WORKDIR /gaussian_splatting_reduced
RUN python setup.py build_ext --inplace

# Runtime stage
FROM nvidia/cuda:12.3.2-base-ubuntu22.04

# Install conda in the runtime stage
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh \
    && bash miniconda.sh -b -p /opt/conda \
    && rm miniconda.sh

# Copy the conda environment from the build stage
COPY --from=build /opt/conda/envs/gaussian_splatting_reduced /opt/conda/envs/gaussian_splatting_reduced

# Set up the runtime environment
ENV PATH=/opt/conda/envs/gaussian_splatting_reduced/bin:$PATH
ENV PYTHONPATH=/gaussian_splatting_reduced

# Copy the built extension from the build stage
COPY --from=build /gaussian_splatting_reduced/ /gaussian_splatting_reduced/

# Set the entrypoint and command
ENTRYPOINT ["python", "/gaussian_splatting_reduced/your_script.py"]