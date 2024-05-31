from flask import Flask, jsonify, request

app = Flask(__name__)

tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    print("Received JSON data:", data)
    task = {
        'id': len(tasks) + 1,
        'title': data.get('title'),
        'description': data.get('description'),
        'done': False
    }
    tasks.append(task)
    return jsonify({'message': 'Task created successfully', 'task': task}), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = cursor.fetchone()
    if task is None:
        return jsonify({'message': 'Task not found'}), 404
    title = data.get('title', task[1])
    description = data.get('description', task[2])
    done = data.get('done', task[3])
    cursor.execute("UPDATE tasks SET title=?, description=?, done=? WHERE id=?", (title, description, done, task_id))
    conn.commit()
    return jsonify({'message': 'Task updated successfully', 'task': {'id': task_id, 'title': title, 'description': description, 'done': done}})

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cursor.execute("SELECT * FROM tasks WHERE id=?", (task_id,))
    task = cursor.fetchone()
    if task is None:
        return jsonify({'message': 'Task not found'}), 404
    cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, port='80')