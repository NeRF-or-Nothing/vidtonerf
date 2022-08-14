# Intermediary backend
## This repository contains mosst of the intermediary API services/libraries to connect the actual NeRF rendering engine to the front end.
## The bulk of this project will be the Flask API for the frontend to relay data and information on the video to process and how to process it.
## The NeRF engine can then take that information, render the video, and relay the processed result back to the frontend.
</br>

# The Flask API
## Located [here](./web-server/), the Flask API is the main internal API we will be using to connect the frontend to the backend.
</br>

# The NeRF API
## This API will be a simple wrapper around the NeRF engine to fine-tune what we want the engine to exactly render and how we want to render it.
</br>
