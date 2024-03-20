import requests

def fetch_data(number_id):
    try:
        response = requests.get(f'http://20.244.56.144:9876/numbers/{number_id}')
        response.raise_for_status()  # Raise an exception for any non-2XX response
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")

# Example usage:
if __name__ == "__main__":
    number_id = 'e'  # Change to 'p', 'f', or 'r' for other types of numbers
    data = fetch_data(number_id)
    print("Response:")
    print(data)
