# Equitary Repository

Welcome to the official repository of Equitary Inc., which houses the codebase for our automated due-diligence report builder. This repository contains a collection of Python scripts and JavaScript files crucial for generating and managing due-diligence reports based on financial statements and metrics.

## Repository Structure

Below is a brief overview of the key components in the repository:

### Python Scripts

- **`dd_prod_gpt4_vanilla.py`**: This is the main production script. It uses the OpenAI API to generate due diligence reports by processing three distinct financial reports (income statement, cash flow statement, balance sheet) provided in CSV format, along with various financial metrics.

- **`dd_app_localhost_gpt4_vanilla.py`**: Utilized for local testing of the production script. It helps ensure that any new changes to the main script function as expected before being deployed.

- **`dd_machinetest_gpt4_vanilla.py`**: This script is intended for experimental features that may not perform correctly in a local environment. It is not recommended for regular testing.

- **`s3_upload.py`**: Handles the uploading of financial documents to an AWS S3 bucket. Following upload, these documents are converted to CSV via `xls_to_csv.py`, stored in a database with `s3_to_db.py`, and the S3 bucket is subsequently cleared.

- **`s3_upload_localhost.py`**: Used for local development testing of the S3 upload functionalities before they are implemented in the production environment.

- **`xls_to_csv.py`**: Converts files from XLS format to CSV using the CloudConvert API after they are uploaded to S3.

- **`s3_to_db_new.py`**: Transfers the CSV files from S3 to a database table, clears the S3 bucket after transfer, and prepares the data for further processing.

### JavaScript Files

- **`document_upload.js`**: Manages the frontend functionalities related to document uploads on a Wix site.

- **`due_diligence_report.js`**: Manages the display functionalities for the due diligence reports on the frontend.

### Folders

- **`templates`**: Contains HTML/CSS templates that are used by the frontend for the s3 upload and the due diligence report generation functionalities.

## Getting Started

To get started with the Equitary repository, clone the repository and install necessary dependencies.

```bash
git clone https://github.com/equitary/equitary.git
cd equitary
pip install -r requirements.txt
```

### Usage

- To run the main production script:
```bash
python dd_prod_gpt4_vanilla.py
```

- For testing changes locally before production:
```bash
python dd_app_localhost_gpt4_vanilla.py
```

## Contributing

We welcome contributions from the community. Before submitting your contribution, please ensure you have completed the following steps:

1. Fork the repository.
2. Create a new branch for your feature.
3. Add your changes and commit them.
4. Push your branch and submit a pull request.

## Support

For any questions or issues, please open an issue on the repository, and a maintainer will assist you.

## License

This project is licensed under the CC0 1.0 Universal License - see the [LICENSE.md](LICENSE) file for details. 

This README aims to provide all necessary information for both using and contributing to the repository. For any additional information or clarification, contributors and users are encouraged to open an issue in the repository.

