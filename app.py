import json
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
STUDENTS_FILE = 'students.json'

def load_data():
    with open(STUDENTS_FILE, 'r') as json_file:
        students = json.load(json_file)
    return students

@app.route('/student', methods=['POST'])
def new_student():
    data = request.get_json()
    name=data["name"]
    email=data["email"]
    students=load_data()
    if len(students)==0:
        student_id=1
        
    else:
        last_id=students[-1]["student_id"]
        student_id=last_id+1
    stu={
        "student_id":student_id,
        "name":name,
        "email":email,
        "matah":0,
        "english":0,
        "computer":0
    }
    students.append(stu)
    with open(STUDENTS_FILE, 'w') as json_file:
        json.dump(students, json_file)
    
    return data

@app.route('/student', methods=['GET'])
@app.route('/student/<int:student_id>', methods=['GET'])
def read_student(student_id = -1):
    # print("gggg")
    students = load_data()
    # print(student_id)
    if int( student_id) == -1:
        print(students)
        return students
    else:
        for student in students:
            if int(student['id']) == student_id:
                return student
        return {"msg": "there is no student"}

@app.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id=-1):
    students = load_data()
    input_data = request.get_json()
    for student in students:
        if student["student_id"]==int(student_id):
            student["math"]=input_data["math"]
            student["english"]=input_data["english"]
            student["syber"]=input_data["syber"]
            
    with open(STUDENTS_FILE, 'w') as json_file:
        json.dump(students, json_file)
    return students

@app.route('/student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    students = load_data()
    index = 0
    for student in students:
        if int(student['id']) == student_id:
            students.pop(index)
            break
        else:
            index += 1
    with open(STUDENTS_FILE, 'w') as json_file:
        json.dump(students, json_file)
    return jsonify({"msg": "student deleted"})


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)





