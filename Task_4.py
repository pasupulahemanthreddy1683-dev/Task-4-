from flask import Flask, request, jsonify

app = Flask(__name__)
users = []
next_id = 1

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify({
        "count": len(users),
        "users": users
    })

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)

    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def add_user():
    global next_id
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400
    new_user = {
        "id": next_id,
        "name": data["name"]
    }
    users.append(new_user)
    next_id += 1
    return jsonify({
        "message": "User created successfully",
        "user": new_user
    }), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        user["name"] = data.get("name", user["name"])
        return jsonify({
            "message": "User updated successfully",
            "user": user
        })
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        users = [u for u in users if u["id"] != user_id]
        return jsonify({"message": "User deleted successfully"})

    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)