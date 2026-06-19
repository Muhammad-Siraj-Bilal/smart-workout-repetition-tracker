import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, Response, request
import json
import plan_func
import freqs_app, weights_app, infer
import pandas as pd
import datetime

cred = credentials.Certificate("signin-example-pkey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
email = 'anushka.narsima@gmail.com'
c_workout = db.collection('Users').document(email).get().to_dict()['workout_plan'][0]['name']

app = Flask(__name__)  

@app.route('/plan', methods=['GET'])
def plan():
    email = request.args.get('email')
    doc_ref = db.collection('Users').document(email)
    doc = doc_ref.get().to_dict()
    formResponse = doc['form_response']
    exercises = doc['form_exercises']
    newOptions = plan_func.makePlan(formResponse, exercises)
    print(newOptions)
    # Update workout plan
    doc_ref.update({'workout_plan': newOptions})

    response = json.dumps(['Success'])
    response = Response(response, status=200, content_type='application/json')
    response.headers['X-My-Header'] = 'foo'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

@app.route('/test', methods=['GET'])
def test():
    l = request.args.getlist('arr')
    result = l[0].strip('][').split(',')
    result = [int(x) for x in result]
    print(result)

    response = json.dumps(['Success'])
    response = Response(response, status=200, content_type='application/json')
    response.headers['X-My-Header'] = 'foo'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

@app.route('/time', methods=['GET'])
def time():
    now = datetime.datetime.now()
    today = datetime.date.today().strftime("%B %d, %Y")
    current_time = now.strftime("%H:%M:%S")
    print(current_time)

    response = json.dumps([str(current_time), str(today)])
    response = Response(response, status=200, content_type='application/json')
    response.headers['X-My-Header'] = 'foo'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

@app.route('/sendArgs', methods=['GET'])
def sendArgs():
    data = request.args.get('ag_data')[1:-1].split(',')
    data = [float(x) for x in data]
    print('data = ',data)
    db.collection('Users').document(email).update({'ag_data': firestore.ArrayUnion(data)})
        #Link bw watch n user should be dynamically defined

    response = json.dumps(['Success'])
    response = Response(response, status=200, content_type='application/json')
    response.headers['X-My-Header'] = 'foo'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

# @app.route('/cworkout', methods=['GET'])
# def cworkout():
#     global c_workout
#     to_return = c_workout
#     doc_ref = db.collection('Users').document(email)
#     doc = doc_ref.get().to_dict()
#     plan = doc['workout_plan']

#     # if c_workout == 'Finished':
#     #     c_workout = plan[0]['name']
#     # else:
#     for i in range(len(plan)):
#         if plan[i]['name'] == c_workout and i < len(plan)-1:
#             num = i+1
#             next = plan[num]['name']
#         elif plan[i]['name'] == c_workout and i == len(plan)-1:
#             next = 'Finished'

#     response = json.dumps([c_workout, next])
#     response = Response(response, status=200, content_type='application/json')
#     response.headers['X-My-Header'] = 'foo'
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response, 200

# @app.route('/rfid', methods=['GET'])
# def rfid():
#     scanned = request.args.get('id')
#     gym = db.collection('Users').document(email).get().to_dict()['membership']['gym']
#     eqs = db.collection('Gyms').document(gym).get().to_dict()['equipment']
#     for i in eqs:
#         if i['rfid'] == scanned:
#             name = i['name']
    
#     global c_workout
#     next = c_workout
#     c_workout = name

#     response = json.dumps([c_workout, next])
#     response = Response(response, status=200, content_type='application/json')
#     response.headers['X-My-Header'] = 'foo'
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response, 200

@app.route('/params', methods=['GET'])
def params():
    eqname = request.args.get('name')
    time = request.args.get('time')
    diff = request.args.get('diff')
    needsEq = bool(request.args.get('needs_eq'))
    areas = request.args.getlist('areas')


    doc_ref = db.collection('Users').document(email)
    doc = doc_ref.get().to_dict()
    ag_data = doc['ag_data']

    l = []
    for i in range(0, len(ag_data), 6):
        l.append([ag_data[i], ag_data[i+1], ag_data[i+2], ag_data[i+3], ag_data[i+4], ag_data[i+5]])

    df = pd.DataFrame(l)
    df = df.round(3)
    df = df.rename(columns={0: 'x_a', 1: 'y_a', 2: 'z_a', 3: 'x_g', 4: 'y_g', 5: 'z_g'})
    print(df.head())
    print(len(df))

    freqs = freqs_app.findFreqs(df, 10)
    weights = weights_app.findWeights(df, freqs, 10)
    freqs = {'a_x':freqs['x_a'], 'a_y':freqs['y_a'], 'a_z':freqs['z_a'], 'g_x':freqs['x_g'], 'g_y':freqs['y_g'], 'g_z':freqs['z_g']}
    weights ={'a_x': weights['x_a'], 'a_y': weights['y_a'], 'a_z': weights['z_a'], 'g_x': weights['x_g'], 'g_y': weights['y_g'], 'g_z': weights['z_g']} 
    db.collection('equipment').document(eqname).set({'freqs': freqs, 'weights': weights, 'difficulty': diff, 'needs_eq': needsEq, 'reps': True, 'target_areas': areas, 'time': time})
    db.collection('Users').document(email).update({'ag_data': []})

    response = json.dumps(['Success'])
    response = Response(response, status=200, content_type='application/json')
    response.headers['X-My-Header'] = 'foo'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

@app.route('/pred', methods=['GET'])
def pred():
    global c_workout
    eqname = c_workout

    doc_ref = db.collection('Users').document(email)
    doc = doc_ref.get().to_dict()
    ag_data = doc['ag_data']

    eq_ref = db.collection('equipment').document(eqname)
    doc = eq_ref.get().to_dict()
    freqs, weights = doc['freqs'], doc['weights']

    l = []
    for i in range(0, len(ag_data), 6):
        l.append([ag_data[i], ag_data[i+1], ag_data[i+2], ag_data[i+3], ag_data[i+4], ag_data[i+5]])

    df = pd.DataFrame(l)
    df = df.round(3)
    df = df.rename(columns={0: 'x_a', 1: 'y_a', 2: 'z_a', 3: 'x_g', 4: 'y_g', 5: 'z_g'})
    print(df.head())
    print(len(df))

    acc_freqs = {'x': freqs['x_a'], 'y': freqs['y_a'], 'z': freqs['z_a']}
    acc_weights = {'x': weights['x_a'], 'y': weights['y_a'], 'z': weights['z_a']}
    df_acc = df[df.columns[:3]].rename(columns={'x_a':'x', 'y_a':'y', 'z_a': 'z'})
    acc_result = infer.findReps(df_acc, acc_freqs, acc_weights)
    gyr_freqs = {'x': freqs['x_g'], 'y': freqs['y_g'], 'z': freqs['z_g']}
    gyr_weights = {'x': weights['x_g'], 'y': weights['y_g'], 'z': weights['z_g']}
    df_gyr = df[df.columns[3:6]].rename(columns={'x_g':'x', 'y_g':'y', 'z_g': 'z'})
    gyr_result = infer.findReps(df_gyr, gyr_freqs, gyr_weights)
    print(acc_result, gyr_result)

    if sum(acc_weights) > sum(gyr_weights):
        reps = acc_result
    else:
        reps = gyr_result

    changed = False
    for i in range(len(plan)):
        if plan[i]['name'] == c_workout and i < len(plan)-1:
            num = i+1
            changed = True
            c_workout = plan[num]['name']
        elif plan[i]['name'] == c_workout and i == len(plan)-1:
            c_workout = 'Finished'
            changed = True
    if not changed:
        c_workout = plan[0]['name']

    # Add to progress
    current_date = datetime.now().strftime("%Y-%m-%d")
    data = {'name': eqname, 'reps': reps, 'time': doc['time']*reps}
    db.collection('Users').document(email).update({f"progress.{current_date}": firestore.ArrayUnion(data)})
    
    # Clear ag_data    
    db.collection('Users').document(email).update({'ag_data': []})

    response = json.dumps([reps])
    response = Response(response, status=200, content_type='application/json')
    response.headers['X-My-Header'] = 'foo'
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)