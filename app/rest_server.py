'''                                                                                                                           
Simple REST API in Python
'''

__author__     = "Jan Kogut"
__copyright__  = "Jan Kogut"
__license__    = "MIT"
__version__    = "0.0.1"
__maintainer__ = "Jan Kogut"
__status__     = "Beta"


from flask import Flask, request, jsonify
from sqlalchemy import create_engine

db_connect = create_engine('sqlite:///chinook.db')
app = Flask(__name__)


@app.route("/api/status", methods = ['GET'])
def getStatus():
    result = {'API_status':'OK'}
    return jsonify(result)

@app.route("/api/v1/employees", methods = ['GET'])
def getEmployees():
    conn = db_connect.connect()
    query = conn.execute("select * from employees")
    result = {'employees': [i[0] for i in query.cursor.fetchall()]}
    return jsonify(result)

@app.route("/api/v1/employees/<employee_id>", methods = ['GET'])
def getEmployeeId(employee_id):
    conn = db_connect.connect()
    query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
    result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
    return jsonify(result)
                

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5002"), debug=True)
            
