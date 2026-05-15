"""An API for handling marine experiments."""

from flask import Flask, jsonify, request

from database_functions import (
    get_db_connection,
    get_all_experiments,
    get_experiments_by_score,
    get_experiments_by_type,
    get_experiments_by_score_and_type,
    delete_experiment_by_id
)


app = Flask(__name__)

"""
For testing reasons; please ALWAYS use this connection. 

- Do not make another connection in your code
- Do not close this connection

If you do not understand this instructions; as a coach to explain
"""
conn = get_db_connection("marine_experiments")

def check_experiment_type(experiment_type: str):
    """Checks that the experiment type is allowed."""
    if not isinstance(experiment_type,str):
        return False
    return experiment_type.lower() in [
        "intelligence",
        "obedience",
        "aggression"
    ]

def check_experiment_score(experiment_score: int):
    """Checks that the experiment score is allowed."""
    if not isinstance(experiment_score,str):
        return False
    try:
        experiment_score = int(experiment_score)
    except ValueError:
        return False
    valid_experiment = 0 <= experiment_score <= 100
    return valid_experiment
@app.get("/")
def home():
    """Returns an informational message."""
    return jsonify({
        "designation": "Project Armada",
        "resource": "JSON-based API",
        "status": "Classified"
    })

@app.get("/experiment")
def get_experiments():
    """Returns experiments. Can be filtered by type and score."""
    experiment_type = request.args.get("type")
    min_score = request.args.get("score_over")
    if experiment_type and not check_experiment_type(experiment_type):
        return {"error":"Invalid value for \'type\' parameter"}, 400

    if min_score and not check_experiment_score(min_score):
        return {"error":"Invalid value for \'score_over\' parameter"}, 400
    if not experiment_type and not min_score:
        experiments = get_all_experiments(conn)

    elif experiment_type and not min_score:
        experiment_type = experiment_type.lower()
        experiments = get_experiments_by_type(conn,experiment_type)
    elif not experiment_type and min_score:
        experiments = get_experiments_by_score(conn,min_score)
    else:
        experiment_type = experiment_type.lower()
        experiments = get_experiments_by_score_and_type(conn,experiment_type,min_score)
    return experiments, 200

@app.delete("/experiment/<int:experiment_id>")
def delete_experiment(experiment_id: int) -> dict:
    """Deletes an experiment by its id."""
    deleted_experiment = delete_experiment_by_id(conn,experiment_id)
    if deleted_experiment is None:
        return {"error": f"Unable to locate experiment with ID {experiment_id}."}, 404
    return deleted_experiment, 200
if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()
