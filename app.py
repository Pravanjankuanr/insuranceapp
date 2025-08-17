from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return "Hello, Flask!"

# ---------- MySQL Connection ----------
def get_db_connection():
    return mysql.connector.connect(
        host="sql.freedb.tech",
        port=3306,
        user="freedb_Pravanjan",
        password="9$3C7gBkMG?uw4y",
        database="freedb_lidata"
    )

# ---------- LOGIN ----------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "Invalid credentials"}), 401

    except mysql.connector.Error as err:
        return jsonify({"success": False, "message": f"MySQL Error: {err}"}), 500

# ---------- CREATE CUSTOMER ----------
@app.route("/create_customer", methods=["POST"])
def create_customer():
    data = request.json
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO customer (cust_id, cust_name, mob_number, dob, pan, email, address, state_code, state_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data["cust_id"], data["cust_name"], data["mobile"], data["dob"],
            data["pan"], data["email"], data["address"],
            data["state_code"], data["state_name"]
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Customer added successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------- SEARCH CUSTOMER ----------
@app.route('/get_customer', methods=['GET'])
def get_customer():
    query = request.args.get("query")
    if not query:
        return jsonify({"success": False, "message": "No search query provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM customer
        WHERE cust_id = %s OR cust_name = %s OR pan = %s
        LIMIT 1
    """, (query, query, query))
    customer = cursor.fetchone()
    cursor.close()
    conn.close()

    if customer:
        return jsonify(success=True, data=customer)
    return jsonify(success=False, message="Customer not found.")

@app.route('/get_all_customers', methods=['GET'])
def get_all_customers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customer")
        customers = cursor.fetchall()
        cursor.close()
        conn.close()

        if customers:
            return jsonify(success=True, data=customers)
        else:
            return jsonify(success=False, message="No customers found.")

    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


# ---------- DELETE CUSTOMER ----------
@app.route('/delete_customer', methods=['DELETE'])
def delete_customer():
    data = request.get_json()
    cust_id = data.get("query")

    if not cust_id:
        return jsonify({"success": False, "message": "No customer ID provided"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM customer WHERE cust_id = %s", (cust_id,))
    conn.commit()
    rows_deleted = cursor.rowcount
    cursor.close()
    conn.close()

    if rows_deleted > 0:
        return jsonify({"success": True, "message": "Customer deleted successfully"})
    else:
        return jsonify({"success": False, "message": "Customer not found"}), 404

# ---------- UPDATE CUSTOMER ----------
@app.route('/update_customer', methods=['PUT'])
def update_customer():
    data = request.get_json()

    required_fields = ["cust_id", "cust_name", "mob_number", "dob", "pan", "email", "address", "state_code", "state_name"]
    if not all(field in data and data[field] for field in required_fields):
        return jsonify(success=False, message="Missing required fields."), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        update_query = """
            UPDATE customer
            SET cust_name = %s, mob_number = %s, dob = %s, pan = %s, email = %s,
                address = %s, state_code = %s, state_name = %s
            WHERE cust_id = %s
        """
        cursor.execute(update_query, (
            data["cust_name"],
            data["mob_number"],
            data["dob"],
            data["pan"],
            data["email"],
            data["address"],
            data["state_code"],
            data["state_name"],
            data["cust_id"]
        ))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(success=True, message="Customer updated successfully.")
    
    except Exception as e:
        return jsonify(success=False, message=f"Error: {str(e)}"), 500






# ---------- State Backend ----------
@app.route('/get_state', methods=['GET'])
def get_all_states():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT state_Code, state_Name FROM state")
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if results:
            return jsonify({"success": True, "states": results})
        else:
            return jsonify({"success": False, "message": "No states found"}), 404

    except mysql.connector.Error as err:
        return jsonify({"success": False, "message": f"MySQL Error: {err}"}), 500

@app.route('/get_state/search', methods=['GET'])
def search_state():
    search_value = request.args.get("query")

    if not search_value:
        return jsonify({"success": False, "message": "Query parameter is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT state_Code, state_Name
            FROM state
            WHERE state_Code LIKE %s OR state_Name LIKE %s
        """
        like_value = f"%{search_value}%"
        cursor.execute(query, (like_value, like_value))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        if result:
            return jsonify({"success": True, "states": [result]})  # ✅ wrapped in list
        else:
            return jsonify({"success": False, "message": "No matching states found"}), 404

    except mysql.connector.Error as err:
        return jsonify({"success": False, "message": f"MySQL Error: {err}"}), 500


@app.route('/add_state', methods=['POST'])
def add_state():
    data = request.json
    code = data.get("state_Code")
    name = data.get("state_Name")

    if not code or not name:
        return jsonify(success=False, message="State code and name are required"), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM state WHERE state_Code = %s", (code,))
        if cursor.fetchone():
            return jsonify(success=False, message="State code already exists."), 409
        cursor.execute("INSERT INTO state (state_Code, state_Name) VALUES (%s, %s)", (code, name))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True, message="State added successfully.")
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

@app.route('/bulk_add_state', methods=['POST'])
def bulk_add_state():
    data = request.json  # should be a list of {"state_Code": ..., "state_Name": ...}
    inserted = 0
    skipped = 0

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for row in data:
            code = row.get("state_Code")
            name = row.get("state_Name")
            if not code or not name:
                continue
            cursor.execute("SELECT * FROM state WHERE state_Code = %s", (code,))
            if cursor.fetchone():
                skipped += 1
                continue
            cursor.execute("INSERT INTO state (state_Code, state_Name) VALUES (%s, %s)", (code, name))
            inserted += 1

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True, inserted=inserted, skipped=skipped)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

@app.route('/delete_state', methods=['DELETE'])
def delete_state():
    code = request.args.get("code")
    if not code:
        return jsonify({"success": False, "message": "State code is required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM state WHERE state_Code = %s", (code,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "State code not found"}), 404

        cursor.execute("DELETE FROM state WHERE state_Code = %s", (code,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"success": True, "message": "State deleted successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/update_state', methods=['PUT'])
def update_state():
    data = request.json
    code = data.get("state_Code")
    name = data.get("state_Name")

    if not code or not name:
        return jsonify({"success": False, "message": "State code and name are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM state WHERE state_Code = %s", (code,))
        if not cursor.fetchone():
            return jsonify({"success": False, "message": "State code not found"}), 404

        cursor.execute("UPDATE state SET state_Name = %s WHERE state_Code = %s", (name, code))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"success": True, "message": "State updated successfully"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


# ---------- Plan Backend ----------

# ---------- CREATE (POST) ----------
@app.route("/add_plan", methods=["POST"])
def add_plan():
    data = request.json
    code = data.get("plan_code")
    name = data.get("plan_name")
    if not code or not name:
        return jsonify({"error": "Missing plan_code or plan_name"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM plan WHERE plan_code = %s", (code,))
        if cursor.fetchone():
            return jsonify({"message": "Plan already exists"}), 409

        cursor.execute("INSERT INTO plan (plan_code, plan_name) VALUES (%s, %s)", (code, name))
        conn.commit()
        return jsonify({"message": "Plan added successfully"}), 201
    except Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# ---------- READ (GET) ----------
# Get all plans (used in View All)
@app.route("/get_all_plans", methods=["GET"])
def get_all_plans():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM plan")
        result = cursor.fetchall()
        return jsonify({"success": True, "plans": result})
    except Error as err:
        return jsonify({"success": False, "error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# Search plans by code or name (used in Search)
@app.route("/get_plan/search", methods=["GET"])
def search_plan():
    query = request.args.get("query", "").strip()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM plan WHERE plan_code LIKE %s OR plan_name LIKE %s",
            (f"%{query}%", f"%{query}%")
        )
        result = cursor.fetchall()
        if result:
            return jsonify({"success": True, "plans": result})
        else:
            return jsonify({"success": False, "message": "No matching plans found."})
    except Error as err:
        return jsonify({"success": False, "error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()


# ---------- UPDATE (PUT) ----------
@app.route("/update_plan/<plan_code>", methods=["PUT"])
def update_plan(plan_code):
    data = request.json
    name = data.get("plan_name")
    if not name:
        return jsonify({"error": "Missing plan_name"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM plan WHERE plan_code = %s", (plan_code,))
        if not cursor.fetchone():
            return jsonify({"message": "Plan not found"}), 404

        cursor.execute("UPDATE plan SET plan_name = %s WHERE plan_code = %s", (name, plan_code))
        conn.commit()
        return jsonify({"message": "Plan updated successfully"})
    except Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

# ---------- DELETE ----------
@app.route("/delete_plan/<plan_code>", methods=["DELETE"])
def delete_plan(plan_code):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM plan WHERE plan_code = %s", (plan_code,))
        if not cursor.fetchone():
            return jsonify({"message": "Plan not found"}), 404

        cursor.execute("DELETE FROM plan WHERE plan_code = %s", (plan_code,))
        conn.commit()
        return jsonify({"message": "Plan deleted successfully"})
    except Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route("/bulk_add_plan", methods=["POST"])
def bulk_add_plan():
    data = request.json.get("plans", [])
    inserted = 0
    skipped = 0

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        for row in data:
            code = row.get("plan_code")
            name = row.get("plan_name")
            if not code or not name:
                continue
            cursor.execute("SELECT * FROM plan WHERE plan_code = %s", (code,))
            if cursor.fetchone():
                skipped += 1
                continue
            cursor.execute("INSERT INTO plan (plan_code, plan_name) VALUES (%s, %s)", (code, name))
            inserted += 1
        conn.commit()
        return jsonify(success=True, inserted=inserted, skipped=skipped, message=f"Inserted: {inserted}, Skipped: {skipped}")
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500
    finally:
        cursor.close()
        conn.close()

# ---------- Partner Backend ----------

@app.route("/add_partner", methods=["POST"])
def add_partner():
    data = request.json
    code = data.get("cp_code")
    name = data.get("cp_name")

    if not code or not name:
        return jsonify(success=False, message="Code and Name required."), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cp WHERE CP_Code = %s", (code,))
        if cursor.fetchone():
            return jsonify(success=False, message="CP already exists."), 409

        cursor.execute("INSERT INTO cp (CP_Code, CP_Name) VALUES (%s, %s)", (code, name))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify(success=True, message="Channel partner added."), 201
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

@app.route("/bulk_add_cp", methods=["POST"])
def bulk_add_cp():
    data = request.json.get("partners", [])
    inserted = 0
    skipped = 0

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        for row in data:
            code = row.get("cp_code")
            name = row.get("cp_name")
            if not code or not name:
                continue
            cursor.execute("SELECT * FROM cp WHERE CP_Code = %s", (code,))
            if cursor.fetchone():
                skipped += 1
                continue
            cursor.execute("INSERT INTO cp (CP_Code, CP_Name) VALUES (%s, %s)", (code, name))
            inserted += 1

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify(success=True, inserted=inserted, skipped=skipped)

    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

@app.route("/get_all_cp", methods=["GET"])
def get_all_cp():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT CP_Code as cp_code, CP_Name as cp_name FROM cp")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(success=True, partners=data)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

@app.route("/get_cp/search", methods=["GET"])
def search_cp():
    query = request.args.get("query", "")
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        search = f"%{query}%"
        cursor.execute("SELECT CP_Code as cp_code, CP_Name as cp_name FROM cp WHERE CP_Code LIKE %s OR CP_Name LIKE %s", (search, search))
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(success=True, partners=data)
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500

@app.route("/delete_cp/<cp_code>", methods=["DELETE"])
def delete_cp(cp_code):
    try:
        conn = mysql.connection
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cp WHERE CP_Code = %s", (cp_code,))
        if cursor.fetchone() is None:
            return jsonify({"success": False, "message": "Partner not found"}), 404

        cursor.execute("DELETE FROM cp WHERE CP_Code = %s", (cp_code,))
        conn.commit()

        return jsonify({"success": True, "message": f"Partner '{cp_code}' deleted successfully"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@app.route("/update_cp/<cp_code>", methods=["PUT"])
def update_cp(cp_code):
    try:
        data = request.get_json()
        cp_name = data.get("cp_name")

        if not cp_name:
            return jsonify({"success": False, "message": "cp_name is required"}), 400

        conn = mysql.connection
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cp WHERE CP_Code = %s", (cp_code,))
        if cursor.fetchone() is None:
            return jsonify({"success": False, "message": "Partner not found"}), 404

        cursor.execute("UPDATE cp SET CP_Name = %s WHERE CP_Code = %s", (cp_name, cp_code))
        conn.commit()

        return jsonify({"success": True, "message": f"Partner '{cp_code}' updated successfully"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


# ---------- Run Server ----------
if __name__ == '__main__':
    app.run(debug=True)