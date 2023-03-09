# DISCLAIMER
If I shared the link to this repository with you, please be aware that this is in a very early stage, and at this point probably serves as a means for you to get a general idea of my tech stack and my coding style. This project is mostly my **playground for trying out different technologies, frameworks and ideas related to machine learning and full stack development**, and at such not planned to ever be finished, but instead constantly updated and adapted.  

Also, ML-related development is currently on hold, since my GPU broke.


## Training Canvas
Training Canvas is going to be a Web App, in which users can draw an object, and a neural network makes a prediction on what they have drawn. Users can also train their own model, by drawing objects, and so creating their own training dataset, as well as specifying their own hyperparameters used for training.  


### Functionality Web App
- User can create a new, empty project
- User can add a class to a project, e.g. House, which will create a database entry for this class, relating to the project.
- User can use a canvas to draw a house. This image is then stored in blob storage, and a database entry is created for the blob name
- Once a certain number of images have been drawn per class, user can train a network to classify objects.
- Any image drawn afterwards serves as input for the model, and a classification is given.
- User has the option to tell the backend that the model prediction is wrong. If that is the case, user is prompted if the image should be added to the training dataset. If yes, image is written to blob + metadata to database, and the model is retrained.
- User can create mutiple of such objects, and draw multiple instances per object.
- User knows how many object he/she has drawn per class, and what classes exist per project.
- User can monitor performance of current model, as well as class accuracy.

### Stack (v0.1.0)
- `pytorch`: GPU training and inference, dataset and dataloaders. Consider pretrained models from torchvision
- `onnxruntime`: consider for faster inference. Since model is retrained often, tracing the model graph might be a significant slowdown though (which is also why nvidia's TensorRT is not feasible)! Compare to `torch.jit`
- `fastapi`: REST API
- `alembic`: database migrations
- `sqlalchemy`: ORM, because we like python, typehints and autocomplete, and therefore avoid raw sql

## Milestones (not in a scrum kind of way)
### **[REACHED]**
- Create concept of application, design the API and the database
- Setting up a docker container network, with three containers:
  - A postgres container
  - A azurite container, which emulates Azure blob storage
  - A backend container, including business logic
- Implementing database structure and SQLAlchemy models
- Implementing blob storage structure (probably just two containers: one for the images, one for the model checkpoints)
- Download sketch dataset (https://paperswithcode.com/dataset/sketch), create script to upload data to blob storage, and create a pytorch `Dataset`

### **[ON HOLD]**
- [GPU BROKE] Decide on a CNN architecture (consider deep ResUnet with pruning; or a much smaller net, maybe TinyNet?)
- [GPU BROKE] Train the CNN on sketch dataset, upload checkpoints to blob storage - this trained network should be availbe in finished app

### **[IN PROGRESS]**

### **[TODO]**
- Currently there seems to be a problem with CUDA. Investigate, consider switching directly to lambda stack **high prio**
- Implement pre-commit hooks, to check types, run code formatter and linter **high prio**
- Come up with a training strategy 
  - When to retrain? (e.g. retrain on button-click, retrain on new image, retrain in regular intervals)
  - When to stop training? (early stopping vs. fixed number of epochs)
  - What data to use? (entire dataset, or is there a way to finetune on newly added images only?)
  - Which layers to train?
- Create Endpoints
- ... (plan further ahead)
- Use github for improving project management. Don't want to have this in a README
- Research Postman API, and see if and how to use it to test the API.

### **[TODO in a very far away future]**
- User authentification + dashboard of projects
- Try an active learning approach, where user gets feedback on what he/she should draw, so that the model can reduce uncertainty
- Learn TypeScript and a reactive framework (and probably freshen up on semantic HTML) to implement the Frontend
