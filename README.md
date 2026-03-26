# Chromosome Image Analysis Using Deep Learning
## Project Overview

This project aims to build an intelligent system for chromosome image analysis and abnormality detection from medical images. The work includes:

- building a baseline CNN model
- comparing CNN with a Transformer-based model
- exploring a hybrid CNN + RNN model
- selecting the best-performing model
- deploying the selected model in a FastAPI web application for real-time inference

The project is designed as both an academic study and a practical software system.

## Objectives

The main objectives are:

- analyze chromosome images using deep learning
- compare multiple architectures fairly
- study the effectiveness of CNN, Transformer, and CNN+RNN
- evaluate models using standard classification metrics
- integrate the best model into a web-based system

## Models to Compare

The following models will be implemented and evaluated:

### 1. CNN
A convolutional neural network used as the baseline model for image feature extraction and prediction.

### 2. Vision Transformer
A Transformer-based image model used to capture global relationships within chromosome images.

### 3. CNN + RNN
A hybrid architecture where:
- CNN extracts spatial features
- RNN processes sequential representations of these features

## Expected Workflow

The project pipeline follows these steps:

1. collect and inspect the dataset
2. preprocess chromosome images
3. split data into training, validation, and test sets
4. train CNN model
5. train Transformer model
6. train CNN+RNN model
7. compare all models
8. select the best-performing model
9. deploy the selected model using FastAPI
10. provide a simple web interface for image upload and prediction

## Repository Structure

```bash
project/
│
├── app/
│   ├── main.py
│   ├── preprocessing.py
│   ├── predict.py
│   ├── model_loader.py
│   ├── templates/
│   │   └── index.html
│   └── static/
│       └── style.css
│
├── scripts/
│   ├── prepare_dataset.py
│   ├── train_cnn.py
│   ├── train_transformer.py
│   ├── train_cnn_rnn.py
│   ├── compare_models.py
│   └── evaluate.py
│
├── models/
│   ├── cnn_model.keras
│   ├── transformer_model.keras
│   ├── cnn_rnn_model.keras
│   └── best_model.keras
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── train/
│   ├── val/
│   └── test/
│
├── results/
│   ├── metrics.csv
│   ├── comparison_table.csv
│   └── figures/
│
├── tests/
│   ├── test_api.py
│   └── test_models.py
│
├── requirements.txt
├── README.md
└── .gitignore
