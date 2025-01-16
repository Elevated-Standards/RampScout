# RampScout

> Cloud Asset Inventory Generator

## Purpose

This project generates a FedRAMP-aligned inventory of assets in different cloud providers. Currently, it supports Amazon Web Services (AWS) and has placeholders for Microsoft Azure and Google Cloud Platform (GCP).

Example OutPut: [2025-01-10-Inventory.xlsx](output/2025/Jan/2025-01-10-Inventory.xlsx)



## Supported Cloud Providers

- [X] Amazon Web Services
  - [AWS Workflow YML](.github/workflows/aws-inventory.yml)
  - [Github Action AWS Inventory Configuration](docs/aws-inventory.md)
- [ ] Microsoft Azure
- [ ] Google Cloud Platform

## Project Structure


## Setup

1. **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set up Python environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### AWS Inventory


### Azure Inventory


### GCP Inventory



## Configuration

- **Column Mapping:** [column_mapping.json]()
- **AWS Configuration:** [aws.json]()
- **Azure Configuration:** [azure.json]()
- **GCP Configuration:** [googlecloud.json]()



## License


