
# ProcessApp - Corporatica

**ProcessApp** is a dynamic Flask-based application designed for processing a variety of data types: tabular datasets, RGB images, and text data. The application exposes a set of RESTful APIs that allow users to upload data, perform processing tasks, and generate visual outputs such as statistics, graphs, and text summaries.

## Features

### 1. Tabular Data Processing

- **Data Upload and Management**: Users can upload tabular datasets (CSV, Excel) for analysis and management.
- **Statistical Analysis**: APIs are provided for computing key statistics such as:
  - Mean, Median, Mode
  - Quartile ranges and outlier detection
- **Data Visualization**: Generate interactive charts and graphs to visualize data trends dynamically.
- **Dataset CRUD Operations**: A web-based interface allows users to create, update, delete, and query datasets with ease.

### 2. RGB Image Processing

- **Image Upload and Storage**: Users can upload individual or multiple images, which are stored and made accessible for further manipulation.
- **Color Analysis & Segmentation**: The app offers APIs to generate color histograms, segment images, and fine-tune color processing parameters.
- **Image Editing Tools**: Supports basic image operations such as resizing, cropping, and format conversions via the web interface.

### 3. Text Data Processing

- **Text Analysis**: The app includes functionality for processing text data, including text summarization, keyword extraction, and basic sentiment analysis.
- **T-SNE Visualizations**: Provides APIs to create dynamic visualizations using T-SNE (t-distributed stochastic neighbor embedding) for dimensionality reduction on text-based datasets.
- **Text Search & Categorization**: Users can perform complex text searches, classify text, and execute custom-defined queries.

## Core Libraries and Technologies

The application is built using a combination of powerful Python libraries and tools to handle diverse data types and processing tasks:

- **Flask**: Core web framework used to create API routes and web services.
- **Flask-RESTful**: Simplifies building REST APIs within the Flask ecosystem.
- **pymongo**: Facilitates interactions with MongoDB for storing and retrieving data.
- **pandas**: Used for efficient handling and analysis of tabular datasets.
- **plotly**: Enables the creation of dynamic, interactive data visualizations for statistical outputs.
- **pydantic-settings**: Manages configuration and environment settings.
- **uuid**: Generates unique IDs for various entities, such as image and data records.
- **opencv-python**: Provides image processing capabilities for handling RGB images, generating histograms, and segmentation.
- **pillow**: Additional support for image manipulation and format conversion.
- **matplotlib**: Used for plotting static graphs and charts for data visualization.
- **scikit-learn**: Offers machine learning functionalities, including dimensionality reduction techniques like T-SNE.
- **textblob**: Facilitates text analysis tasks, including sentiment analysis and keyword extraction.
- **nltk**: Provides natural language processing (NLP) tools for text categorization, tokenization, and other text-based operations.

## Installation

### Prerequisites

- **Python 3.9+** installed
- **MongoDB** installed and running
- **Docker** (optional for containerized deployment)
- **Kubernetes** (Minikube recommended for local Kubernetes setup)

### Setup Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/processapp.git
   cd processapp
   ```
2. **Create a virtual environment and install dependencies**:

   ```bash
   python3.9 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Set environment variables**:
   Create a `.env` file with the following details:

   ```env
   FLASK_APP=src/app.py
   FLASK_ENV=development
   DATABASE_URL=mongodb://localhost:27017/processapp
   ```
4. **Run the application**:

   ```bash
   flask run
   ```

   Access the application at `http://localhost:5000`.

## K8s Setup

---

### Kubernetes Setup with Minikube

To deploy the ProcessApp application using Minikube, follow these steps:

1. **Start Minikube**:
   Ensure Minikube is running:

   ```bash
   minikube start
   ```
2. **Configure Docker for Minikube**:
   Set up your Docker environment to use Minikube’s Docker daemon:

   ```bash
   eval $(minikube docker-env)
   ```
3. **Build the Docker Image**:
   Build your Docker image for the application:

   ```bash
   docker build -t processapp:latest .
   ```
4. **Enable Ingress Addon**:
   Enable the NGINX Ingress controller in Minikube:

   ```bash
   minikube addons enable ingress
   ```
5. **Deploy Kubernetes Resources**:
   Apply the Kubernetes configuration to deploy the application. Ensure you have a file named `k8s_app.yml` with the necessary Kubernetes manifests:

   ```bash
   kubectl apply -f k8s_app.yml
   ```
6. **Access the Application**:
   Use Minikube’s service URL to access the application:

   ```bash
   minikube service processapp-service
   ```
   Alternatively, if you have set up Ingress, you may access your application via the configured hostname.
