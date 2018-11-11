'''                                                                                                                           
Simple REST API in Python
'''

__author__     = "Jan Kogut"
__copyright__  = "Jan Kogut"
__license__    = "MIT"
__version__    = "0.0.1"
__maintainer__ = "Jan Kogut"
__status__     = "Beta"

from flask import Flask, request, jsonify, abort
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#####################
app = Flask(__name__)

engine = create_engine('sqlite:///chinook.db', echo=True)
Base = declarative_base(engine)

class Employees(Base):
    """ Class for declarative_base ORM db access """

    __tablename__ = 'employees'
    __table_args__ = {'autoload':True}


def loadSession():
    """ 
    ---> Create session 
    <--- Return session object
    """

    metadata = Base.metadata
    Session  = sessionmaker(bind=engine)
    session  = Session()
    return session
                                    

## API STATUS
@app.route("/api/status", methods = ['GET'])
def getStatus():
    """ 
    ---> Check API Status
    <--- Return JSON with API_status
    """

    result = {'API_status':'OK'}
    return jsonify(result)


## GET employees
@app.route("/api/v1/employees", methods = ['GET'])
def getEmployees():
    """
    ---> Select all employees
    <--- Return JSON with employeeID
    """
    
    result = { "employees": dict(session.query(Employees.EmployeeId,Employees.LastName).all()) }
    return jsonify(result)


## GET employeeId
@app.route("/api/v1/employees/<int:employeeId>", methods = ['GET'])
def getEmployeeIdData(employeeId):  
    """
    ---> Select employee depending on employeeId
    <--- Return JSON with employeeIds data
    """

    filterQuery = session.query(Employees).filter(Employees.EmployeeId==employeeId).all()
    result = { x: getattr(filterQuery[0], x) for x in Employees.__table__.columns.keys() }
    return jsonify(result)


## POST create employee
@app.route("/api/v1/employees/new", methods = ['POST'])
def insertNewEmployee():
    """
    ---> Add (create) new employee from JSON payload
    <--- Return added JSON payload with response code
    """
    
    payload = request.json
    if not payload or not 'LastName' in payload:
        abort(400)

    newEmp = Employees(**dateNormalizer(payload))
    session.add(newEmp)
    session.flush()
    session.commit()
    return jsonify(payload),201


if __name__ == "__main__":
    session = loadSession()

    def dateNormalizer(payload):
        """
        ---> SQLite DateTime type only accepts Python datetime 
        <--- Return normalized JSON payload with Python datetime
        """

        import timestring
        
        normalizedBirthDate  = timestring.Date(payload['BirthDate']).date
        normalizedHireDate   = timestring.Date(payload['HireDate']).date
        payload['BirthDate'] = normalizedBirthDate
        payload['HireDate']  = normalizedHireDate
        return payload
        
    app.run(host="0.0.0.0", port=int("5002"), debug=True)
