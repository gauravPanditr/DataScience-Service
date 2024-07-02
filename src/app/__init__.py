from flask import Flask, request, jsonify
from service.messageService import MessageService
from kafka import KafkaProducer
import json

app = Flask(__name__)
app.config.from_pyfile('config.py')

messageService = MessageService()
producer = KafkaProducer(
    bootstrap_servers=app.config['KAFKA_BOOTSTRAP_SERVERS'],
    security_protocol='SASL_SSL',
    sasl_mechanism='SCRAM-SHA-256',
    sasl_plain_username=app.config['KAFKA_USERNAME'],
    sasl_plain_password=app.config['KAFKA_PASSWORD'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

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
    app.run(host="localhost", port=8000, debug=True)
