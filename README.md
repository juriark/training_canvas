# training_canvas
A training tool for a simple classification task, where users draw objects, and a CNN is trained in the background to classify this object

# Stuff to mention
- Source of dataset: https://paperswithcode.com/dataset/sketch
- That this repo serves as a playground/showcase for ideas/concepts, and is not meant to serve as a full-blown, production ready backend. There are many things to be improved, such as
  - This might not even be a good use case for a Deep Learning model. As mentioned in the original paper, a Support Vector Machine might do a just as good job, with less computational effort. In general, **don't use Deep Learning for the sake of it**. If you can solve your problem with a more traditional approach, use it. The reason it was used here, was to play around with pytorch and classification models.
- Regarding model architecture: Resnet (or whatever) was used. Little consideration was given on more suitable architectures (read as: fast but less accurate, e.g. TinyUNet?)


# Stuff to try
## ML part:
- Try re-training the last layer(s) only
- Consider imbalanced dataset!
- Apply distortions/flipping/rotation to input image


# Some features that would be nice for the future
- Monitor the training process, and develop some active learning strategy from it, e.g. let the user know, which class needs more sketches.


# Steps:
## Setup:
- docker compose: we need a container with minio (simulates azure), postgres (or other DB) and one for business logic and backend

## Business logic (ML part):
- Download the data
- Train a ResUnet/Resnet model from torchvision with that data - this will be the model we use further. Store this model
- Freeze the model, except for the last few layers. For that, use the same training script, but have some `is_fine_tuning` kwarg, that if True will freeze most of the layers

## Backend part (REST API):

