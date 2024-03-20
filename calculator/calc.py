from flask import Flask, jsonify
import requests
import time
from collections import deque

app = Flask(__name__)
window_size = 10
stored_numbers = deque(maxlen=window_size)

def fetch_numbers(number_id):
    try:
        response = requests.get(f'http://20.244.56.144/numbers/{number_id}')
        response.raise_for_status()  # Raise an exception for any non-2XX response
        numbers = response.json().get('numbers', [])
        unique_numbers = set(numbers) - set(stored_numbers)  # Exclude duplicates
        stored_numbers.extend(unique_numbers)
    except Exception as e:
        print(f"Error fetching numbers: {e}")

def calculate_average():
    total_sum = sum(stored_numbers)
    return total_sum / len(stored_numbers) if stored_numbers else 0

def refresh_data(number_id):
    start_time = time.time()
    fetch_numbers(number_id)
    elapsed_time = time.time() - start_time
    if elapsed_time > 0.5:
        print("Warning: Fetching data took longer than 500ms.")

@app.route('/numbers/<number_id>', methods=['GET'])
def get_numbers(number_id):
    refresh_data(number_id)
    average = calculate_average()
    response_data = {
        'windowPrevState': list(stored_numbers),
        'windowCurrState': list(stored_numbers),
        'numbers': list(stored_numbers),
        'avg': round(average, 2)
    }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=9876)
