from flask import Flask, jsonify, request
from flasgger import Swagger
from database import init_db,get_db_connection
app = Flask(__name__)
Swagger(app)
init_db()
# Temporary in-memory data
items = [
    {"id": 1, "name": "Python"},
    {"id": 2, "name": "Flask"}
]
# READ - Get all items from database
@app.route("/items", methods=["GET"])
def get_items():
    """
    Get all items
    ---
    responses:
      200:
        description: A list of items
    """
    conn = get_db_connection()

    items = conn.execute(
        "SELECT * FROM tasks"
    ).fetchall()

    conn.close()
    return jsonify([dict(item) for item in items])
# READ - Get one  item
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)

    if item is None:
        return jsonify({"error": "Item not found"}), 404

    return jsonify(item)
# CREATE - Add new task to database
@app.route("/items", methods=["POST"])
def create_item():
    """
    Create a new item
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: Learn Python
            done:
              type: boolean
              example: false
    responses:
      201:
        description: Item created successfully
      400:
        description: Title is required
    """
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    title = data["title"]
    done = data.get("done", False)

    conn = get_db_connection()

    cursor = conn.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (title, done)
    )

    conn.commit()

    new_id = cursor.lastrowid

    conn.close()

    return jsonify({
        "id": new_id,
        "title": title,
        "done": done
    }), 201

# UPDATE - Update an item in database
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    """
    Update an existing item
    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID of the item to update
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            title:
              type: string
              example: Learn Django
            done:
              type: boolean
              example: true
    responses:
      200:
        description: Item updated successfully
      404:
        description: Item not found
      400:
        description: Title is required
    """

    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    title = data["title"]
    done = data.get("done", False)

    conn = get_db_connection()

    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (item_id,)
    ).fetchone()

    if task is None:
        conn.close()
        return jsonify({"error": "Item not found"}), 404

    conn.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (title, done, item_id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "id": item_id,
        "title": title,
        "done": done
    })


# DELETE - Delete an item from database
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    """
    Delete an item
    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID of the item to delete
    responses:
      200:
        description: Item deleted successfully
      404:
        description: Item not found
    """

    conn = get_db_connection()

    task = conn.execute(
        "SELECT * FROM tasks WHERE id = ?",
        (item_id,)
    ).fetchone()

    if task is None:
        conn.close()
        return jsonify({"error": "Item not found"}), 404

    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (item_id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Item deleted successfully"
    })
if __name__ == "__main__":
    app.run(debug=True)