from flask import Flask, request, jsonify, render_template
from utils.database import register_user, get_user
from flask_cors import CORS
from dotenv import load_dotenv
from google.cloud import storage
import os

app = Flask(__name__)
load_dotenv()

CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit, adjust as needed

# Route to handle user registration
@app.route('/register', methods=['POST'])
def register():
    data = request.json

    print(data)
    # Check if 'name' exists in the data before accessing it
    if 'name' not in data:
        return jsonify({"error": "Missing 'name' in request data"}), 400

    name = data['name']
    email = data['email']
    password = data['password']

    success = register_user(name,email,password)

    print(name, email, password)

    if success:
        return jsonify({"message": "Successfully registered"}), 200
        # return redirect(url_for('dashboard'))
    else:
        return jsonify({"message": "Failed to register user", "result" : success}), 500


@app.route('/login')
def login_page():
    return render_template('frontend/index.html')  # Load the login page

# Route to handle user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data['email']
    password = data['password']

    user = get_user(email, password)

    if user:
        # return redirect(url_for('dashboard'))
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401

@app.route('/dashboard')
def dashboard():
    return render_template('frontend/dashboard.html')  # You can also render an HTML template here

# Route to handle document upload
@app.route('/upload-document', methods=['POST'])
def upload_document():
    app.logger.info(f"Received request: {request.files}")
    app.logger.info(f"Form data: {request.form}")

    # Clear existing environment variable
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    load_dotenv()

    if 'file' not in request.files:
        return jsonify({"message": "No file part in the request"}), 400

    file = request.files['file']
    email = request.form.get('email')

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if not email:
        return jsonify({"message": "No email provided"}), 400

    if file and email:
        try:

            client = storage.Client.from_service_account_json(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
            bucket = client.get_bucket(os.getenv('GCP_BUCKET_NAME'))

            if not bucket:
                return jsonify({"message": "GCP bucket not configured"}), 500

            # Create a new blob and upload the file's content.
            blob = bucket.blob(f"{email}/{file.filename}")
            blob.upload_from_string(
                file.read(),
                content_type=file.content_type
            )

            return jsonify({"message": "File uploaded successfully"}), 200
        except Exception as e:
            app.logger.error(f"Upload error: {str(e)}")
            return jsonify({"message": f"Failed to upload file: {str(e)}"}), 500
    else:
        return jsonify({"message": "Missing file or email"}), 400

# Route to list all documents in GCP bucket
@app.route('/list-documents', methods=['POST'])
def list_documents():

    # Clear existing environment variable
    if "GOOGLE_APPLICATION_CREDENTIALS" in os.environ:
        del os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

    load_dotenv()

    # Initialize Google Cloud Storage client
    storage_client = storage.Client.from_service_account_json(os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))
    bucket_name = os.getenv('GCP_BUCKET_NAME')

    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs(prefix=f"{email}/")

    documents = [blob.name.split('/')[-1] for blob in blobs if not blob.name.endswith('/')]
    return jsonify(documents)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
