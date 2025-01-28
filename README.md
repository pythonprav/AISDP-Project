.
├── README.md  
├── data-preprocessing
│   ├── Dockerfile           # Dockerfile for containerizing the preprocessing service.
│   ├── preprocess.py        # Script for data preprocessing tasks.
│   └── test_preprocess.py   # Unit tests for the preprocess module.
├── model-inference
│   ├── Dockerfile           # Dockerfile for containerizing the inference service.
│   ├── inference.py         # Script for loading the model and serving predictions.
│   └── test_inference.py    # Unit tests for the inference module.
├── model-training
│   ├── Dockerfile           # Dockerfile for containerizing the model training service.
│   ├── train_model.py       # Script for training the model.
│   └── test_train.py        # Unit tests for the model training module.
├── requirements.txt         # List of project dependencies.
└── web-application
    ├── Dockerfile           # Dockerfile for containerizing the web application.
    └── winequality_app.py   # Backend and frontend integration for user interaction.