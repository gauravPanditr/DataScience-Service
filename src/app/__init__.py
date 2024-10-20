from flask import Flask, request, jsonify
from service.messageService import MessageService
from confluent_kafka import Producer
import os

import json

from dotenv import load_dotenv
load_dotenv()
print("Kafka Bootstrap Servers:", os.getenv('KAFKA_BOOTSTRAP_SERVERS'))
app = Flask(__name__)

messageService = MessageService()
producer_config = {
    'bootstrap.servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'SCRAM-SHA-256',
    'sasl.username': os.getenv('KAFKA_USERNAME'),
    'sasl.password': os.getenv('KAFKA_PASSWORD')
}

# Initialize the Kafka Producer
producer = Producer(producer_config)

@app.route('/v1/ds/message', methods=['POST'])
def handle_message():

    try:
        # Get the message from the request
        message = request.json.get('message')
        
        # Process the message using the service
        result = messageService.process_message(message)
        
        if result is not None:
            # Ensure result is a dictionary (assuming result is an instance of Expense)
            serialized_result = result.dict()
            
            # Send the serialized result to the Kafka topic (if needed)
            producer.send('expense_service', serialized_result)
            
             

            return jsonify(serialized_result), 200
        else:
            return jsonify({'error': 'Invalid message format'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def handle_get():
    return 'Hello world' 

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
