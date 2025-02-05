# Receipt Processor API

The Receipt Processor API is a Flask-based application that processes receipts and calculates reward points based on predefined rules.

## Installation & Setup

To set up the API, first clone the repository using:

```bash
git clone https://github.com/Manasaavula23/receipt-challenge.git
cd receipt-challenge
```

Next, create a virtual environment and install the required dependencies by running:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Once setup is complete, start the API by executing:

```bash
python reciept_processor.py
```

which will run the service at `http://127.0.0.1:5000`.

## API Endpoints

- **Process a Receipt (POST)**: Sends a receipt for processing.

  ```bash
  Invoke-RestMethod -Uri "http://127.0.0.1:5000/receipts/process" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{
    "retailer": "Walgreens",
    "purchaseDate": "2022-01-02",
    "purchaseTime": "08:13",
    "items": [
      { "shortDescription": "Pepsi - 12-oz", "price": "1.25" },
      { "shortDescription": "Dasani", "price": "1.40" }
    ],
    "total": "2.65"
  }' -ContentType "application/json"
  ```

  The response returns a unique `receipt_id`.

- **Retrieve Points (GET)**: Fetches the points for a processed receipt.
  ```bash
  http://127.0.0.1:5000/receipts/{receipt_id}/points
  ```
