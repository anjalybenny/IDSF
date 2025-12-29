# IDSF

Artifact for our project in the Seminar Urban Computing

## Prerequisites

Before you begin, ensure you have met the following requirements:
* **Python 3.8+** installed.
* **Git** installed.

## Installation

To set up the project locally on your machine, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone git@github.com:anjalybenny/IDSF.git
    cd IDSF
    ```

2.  **Create and activate a virtual environment:**
    It is recommended to run this project in a virtual environment to manage dependencies.
    ```bash
    # Create the virtual environment
    python3 -m venv venv

    # Activate the virtual environment (macOS/Linux)
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

This project runs using **Streamlit**. To start the application, make sure your virtual environment is active and run the following command:

```bash
streamlit run app.py