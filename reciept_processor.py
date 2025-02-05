from flask import Flask, jsonify, request
import uuid
import re
import math
from datetime import datetime

app = Flask(__name__)

# Dictionary to store processed receipts
receipt_store = {}

@app.route('/')
def welcome():
    return jsonify({"message": "Receipt Processing API is Live!"}), 200

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request, JSON expected"}), 400

    receipt_id = str(uuid.uuid4())
    points_earned = calculate_points(data)

    receipt_store[receipt_id] = {
        'receipt': data,
        'points': points_earned
    }
    
    return jsonify({'receipt_id': receipt_id})

@app.route('/receipts/<receipt_id>/points', methods=['GET'])
def retrieve_points(receipt_id):
    receipt_entry = receipt_store.get(receipt_id)
    if not receipt_entry:
        return jsonify({'error': 'No receipt found with the given ID'}), 404
    
    return jsonify({'points': receipt_entry['points']})

def calculate_points(receipt):
    points = 0

    # Points based on retailer name
    points += len(re.sub(r'[^a-zA-Z0-9]', '', receipt['retailer']))

    # Check if total is a whole number
    total_price = float(receipt['total'])
    if total_price.is_integer():
        points += 50

    # Check if total is a multiple of 0.25
    if math.isclose(total_price % 0.25, 0, abs_tol=1e-9):
        points += 25

    # Assign 5 points for every two items
    points += (len(receipt['items']) // 2) * 5

    # Points based on item description length
    for item in receipt['items']:
        description_length = len(item['shortDescription'].strip())
        if description_length % 3 == 0:
            item_price = float(item['price'])
            points += math.ceil(item_price * 0.2)

    # Points for odd purchase dates
    purchase_date = datetime.strptime(receipt['purchaseDate'], '%Y-%m-%d')
    if purchase_date.day % 2 != 0:
        points += 6

    # Points for purchases made between 2:00 PM and 4:00 PM
    purchase_time = datetime.strptime(receipt['purchaseTime'], '%H:%M')
    if datetime.strptime('14:00', '%H:%M') < purchase_time < datetime.strptime('16:00', '%H:%M'):
        points += 10

    return points

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
