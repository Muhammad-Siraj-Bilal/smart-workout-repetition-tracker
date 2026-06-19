# Smart Workout Repetition Tracker

A smart fitness backend that generates personalised workout plans and uses accelerometer and gyroscope data to automatically estimate exercise repetitions.

The project combines a Flask REST API, Firebase Firestore and signal-processing techniques to support workout planning, exercise calibration, repetition tracking and progress storage.

## Features

* Personalised workout-plan generation
* Exercise filtering by difficulty and target body area
* Accelerometer and gyroscope data processing
* Automatic exercise repetition counting
* Sensor-axis frequency calibration
* Reliability weighting for motion-sensor axes
* Firebase Firestore integration
* User workout-progress tracking
* REST API endpoints for external applications and wearable devices

## How It Works

The system receives six-axis motion data:

* Accelerometer X, Y and Z
* Gyroscope X, Y and Z

The sensor readings are processed using low-pass filtering and peak detection.

For each exercise, the system:

1. Tests different filtering frequencies.
2. Selects frequencies that produce results closest to the expected repetition count.
3. Assigns reliability weights to each sensor axis.
4. Detects movement peaks.
5. Selects the most reliable repetition estimate.
6. Stores the completed workout in Firebase Firestore.

## Project Structure

```text
smart-workout-repetition-tracker/
├── firebase_app.py
├── freqs_app.py
├── infer.py
├── plan_func.py
├── weights_app.py
├── features/
│   ├── __init__.py
│   └── data_trans.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Main Files

* `firebase_app.py` – Flask API and Firebase Firestore integration
* `plan_func.py` – Personalised workout-plan generation
* `freqs_app.py` – Sensor frequency calibration
* `weights_app.py` – Sensor-axis reliability weighting
* `infer.py` – Exercise repetition prediction
* `features/data_trans.py` – Signal-filtering utilities

## Technologies Used

* Python
* Flask
* Firebase Admin SDK
* Firebase Firestore
* Pandas
* NumPy
* SciPy
* Matplotlib
* Signal processing
* REST APIs

## Installation

Clone the repository:

```bash
git clone https://github.com/Muhammad-Siraj-Bilal/smart-workout-repetition-tracker.git
cd smart-workout-repetition-tracker
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### macOS or Linux

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Requirements

Add the following packages to `requirements.txt`:

```text
Flask
firebase-admin
pandas
numpy
scipy
matplotlib
```

## Firebase Configuration

This application requires a Firebase service-account credential.

Never upload your Firebase private key to GitHub.

Store the credential locally and set the following environment variable.

### Windows PowerShell

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="path\to\service-account-key.json"
```

### Windows Command Prompt

```cmd
set GOOGLE_APPLICATION_CREDENTIALS=path\to\service-account-key.json
```

### macOS or Linux

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account-key.json"
```

The application should load the credential using:

```python
import os
from firebase_admin import credentials

firebase_key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
cred = credentials.Certificate(firebase_key_path)
```

Add credential files to `.gitignore`:

```gitignore
# Firebase credentials
signin-example-pkey.json
*-pkey.json
service-account*.json

# Environment variables
.env

# Python
__pycache__/
*.py[cod]

# Virtual environments
venv/
.venv/
env/

# IDE and operating-system files
.vscode/
.idea/
.DS_Store
Thumbs.db
```

## Running the Application

Start the Flask server:

```bash
python firebase_app.py
```

The server runs by default at:

```text
http://127.0.0.1:5000
```

The application is configured to accept connections from other devices on the same network through:

```text
http://0.0.0.0:5000
```

## API Endpoints

### Generate Workout Plan

```http
GET /plan?email=user@example.com
```

Generates a personalised workout plan using the user’s saved questionnaire responses and available exercises.

### Submit Sensor Data

```http
GET /sendArgs?ag_data=[x_a,y_a,z_a,x_g,y_g,z_g]
```

Submits accelerometer and gyroscope readings to Firebase.

### Configure Exercise Parameters

```http
GET /params
```

Example parameters:

```text
name=Squat
time=3
diff=easy
needs_eq=false
areas=legs
```

This endpoint calculates and stores:

* Sensor frequencies
* Sensor weights
* Exercise difficulty
* Required equipment
* Target body areas
* Exercise duration

### Predict Repetitions

```http
GET /pred
```

Processes stored sensor data and estimates the number of repetitions completed.

### Get Current Date and Time

```http
GET /time
```

Returns the current server time and date.

### Test Array Input

```http
GET /test?arr=[1,2,3]
```

Used to test array handling through query parameters.

## Workout-Plan Generation

The workout-plan generator considers:

* Requested workout duration
* Exercise difficulty
* Target body areas
* Available exercises
* Repetition-based exercises
* Time-based exercises

Exercises are filtered according to the user’s preferences. Exercise duration and repetition values are then adjusted to approximately match the requested workout time.

## Repetition Detection

The repetition-detection process uses:

1. Low-pass filtering to reduce sensor noise.
2. Local-maximum detection to identify movement peaks.
3. Frequency calibration for each sensor axis.
4. Reliability weights to identify the most accurate axes.
5. Accelerometer and gyroscope comparison to select the final result.

## Firebase Collections

The application currently works with collections such as:

```text
Users
equipment
Gyms
```

User documents may contain fields including:

```text
form_response
form_exercises
workout_plan
ag_data
progress
membership
```

Exercise documents may contain:

```text
freqs
weights
difficulty
needs_eq
reps
target_areas
time
```

## Current Limitations

This repository represents a prototype and may require further development before production use.

Current areas for improvement include:

* Replacing hardcoded user email addresses with authenticated users
* Adding proper request validation
* Using POST requests for sensor-data submission
* Improving error handling
* Securing API endpoints
* Correcting unfinished workout-progression logic
* Adding automated tests
* Adding Firebase Authentication
* Improving handling of empty or incomplete sensor datasets
* Moving configuration values into environment variables

## Security Notice

Firebase service-account files contain sensitive private credentials.

Never commit files such as:

```text
signin-example-pkey.json
service-account.json
firebase-key.json
```

If a service-account key has previously been exposed, it should be disabled or deleted through Google Cloud IAM and replaced with a new key.

## Future Improvements

* Firebase Authentication integration
* Mobile application integration
* Smartwatch or wearable-device connectivity
* Real-time repetition tracking
* Exercise-form classification
* Machine-learning-based activity recognition
* Workout-history dashboards
* User progress visualisation
* Support for additional exercise types
* Improved workout recommendation algorithms

## Repository

[Smart Workout Repetition Tracker](https://github.com/Muhammad-Siraj-Bilal/smart-workout-repetition-tracker)

## Author

**Muhammad Siraj Bilal**

## Licence

This project is intended for educational and research purposes.
