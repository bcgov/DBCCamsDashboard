# Overview

A dashboard for cams showing up, stale, or delayed.

## Development

### Requirements

1. Docker Desktop to build and run the code locally
2. Git (to provide git bash for the run command that mounts the local directory)

### Setup - Local Development

1. Clone the repository
2. Change directory into the cloned repository
3. Install the Required libraries: 'pip install -r requirements.txt'
4. Run the application (option 1): streamlit run Main.py
5. Run the application (option 2): python -m streamlit run Main.py

### Setup - Docker

1. Clone the repository
2. Build the image: `docker build -t cams .`
3. Run the image: ` docker run -dp 8501:8501 cams`

Be default, the docker build process clones the repo into the image.  To run the
image so that local changes are reflected after refreshing the page, use this
command instead to mount the local directory over the repo in the image:

`docker run -dp 8501:8501 --mount type=bind,src="$(pwd)",target=/app cams`

The site should be available at http://localhost:8051/.

