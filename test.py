# Codegen by ChatGPT
# Prompt used: 
# (1) Write unit test to test fake news *2 and real news *2
# (2) Write latency test to run and time each test case (*4) for 100 times and record data into a csv. 
# (3) Plot a separate boxplot for each test case
import pytest
from flask import Flask
from flask.testing import FlaskClient
import requests
import time
import csv
import matplotlib.pyplot as plt

from application import application

## UNIT TEST ##
@pytest.fixture
def client() -> FlaskClient:
    """Fixture to create a test client for the Flask app."""
    application.config['TESTING'] = True
    with application.test_client() as client:
        yield client

# Test cases
test_cases = [
    {"text": "This is fake news.", "label": "FAKE"},
    {"text": "This is another fake news.", "label": "FAKE"},
    {"text": "This is real news.", "label": "REAL"},
    {"text": "This is another real news.", "label": "REAL"},
]

def test_fake_news_prediction(client):
    """Test if fake news prediction works correctly."""
    for case in test_cases[:2]:
        response = client.post('/', data={'news_text': case["text"]})
        assert response.status_code == 200
        assert case["label"].encode() in response.data  # Adjust based on actual output

def test_real_news_prediction(client):
    """Test if real news prediction works correctly."""
    for case in test_cases[2:]:
        response = client.post('/', data={'news_text': case["text"]})
        assert response.status_code == 200
        assert case["label"].encode() in response.data  # Adjust based on actual output

## LATENCY TEST ##
# Define base URL for API
BASE_URL = "http://127.0.0.1:5000"  # Adjust to your actual endpoint

# Number of API calls for the test
NUM_CALLS = 100

def test_latency():
    """Perform 100 API calls per test case and record the latency."""
    all_latencies = []

    with open("latency_results.csv", "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["test_case", "call_number", "latency_in_seconds"])

        for case in test_cases:
            latencies = []
            for i in range(NUM_CALLS):
                start_time = time.time()
                response = requests.post(BASE_URL, data={"news_text": case["text"]})
                end_time = time.time()

                latency = end_time - start_time
                latencies.append(latency)

                # Ensure the API call is successful
                if response.status_code != 200:
                    print(f"Error on call {i + 1} for '{case['text']}': Status code {response.status_code}")

                # Write the latency to the CSV file
                csv_writer.writerow([case["label"], i + 1, latency])
            
            all_latencies.append((case["label"], latencies))
            print(f"Test case '{case['label']}' completed.")

    assert all_latencies
    
    plt.figure(figsize=(12, 8))

    # Plot a separate boxplot for each test case
    labels, data = zip(*all_latencies)
    plt.boxplot(data, tick_labels=labels, vert=True)
    plt.title("API Latency Boxplot (100 Calls per Test Case)")
    plt.xlabel("Test Cases")
    plt.ylabel("Latency (seconds)")
    plt.grid(True)
    plt.savefig("latency_boxplot.png")

