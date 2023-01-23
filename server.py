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
    students = load_data()
    students.append(data)
    
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
        return {"msg": "no such student"}

@app.route('/student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    students = load_data()
    input_data = request.get_json()
    student_found = False
    for student in students:
        if int(student['id']) == student_id:
            student_found = True
            student.update(input_data)
            break
    if not student_found:
        return {"msg": "no such student"}
    with open(STUDENTS_FILE, 'w') as json_file:
        json.dump(students, json_file)
    return input_data

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





