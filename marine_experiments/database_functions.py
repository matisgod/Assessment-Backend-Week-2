"""Functions that interact with the database."""

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection


def get_db_connection(dbname,
                      password="postgres") -> connection:
    """Returns a DB connection."""

    return connect(dbname=dbname,
                   host="localhost",
                   port=5432,
                   password=password,
                   cursor_factory=RealDictCursor)

def get_all_experiments(conn:connection) -> list[dict]:
    """Returns all experiments."""
    cursor = conn.cursor()
    query = """
SELECT 
    TO_CHAR(experiment_date,'YYYY-MM-DD') as experiment_date,
    experiment_id,
    type_name as experiment_type,
    ROUND(score/max_score*100,2) as score,
    species_name as species,
    subject_id
FROM experiment
JOIN experiment_type
    USING (experiment_type_id)
JOIN subject
    USING (subject_id)
JOIN species 
    USING (species_id)
ORDER BY experiment_date DESC
;
"""
    cursor.execute(query)
    experiments = cursor.fetchall()
    cursor.close()
    return experiments

def get_experiments_by_type(conn:connection, experiment_type: int) -> dict:
    """Returns an experiment with matching type."""
    cursor = conn.cursor()
    query = """
SELECT 
    TO_CHAR(experiment_date,'YYYY-MM-DD') as experiment_date,
    experiment_id,
    type_name as experiment_type,
    ROUND(score/max_score*100,2) as score,
    species_name as species,
    subject_id
FROM experiment
JOIN experiment_type
    USING (experiment_type_id)
JOIN subject
    USING (subject_id)
JOIN species 
    USING (species_id)
WHERE type_name = %s
ORDER BY experiment_date DESC
;"""
    cursor.execute(query,(experiment_type,))
    experiments = cursor.fetchall()
    cursor.close()
    return experiments

def get_experiments_by_score(conn: connection, score: int) -> list[dict]:
    """Returns all the experiments above a base score"""
    cursor = conn.cursor()
    query = """
SELECT 
    TO_CHAR(experiment_date,'YYYY-MM-DD') as experiment_date,
    experiment_id,
    type_name as experiment_type,
    ROUND(score/max_score*100,2) as score,
    species_name as species,
    subject_id
FROM experiment
JOIN experiment_type
    USING (experiment_type_id)
JOIN subject
    USING (subject_id)
JOIN species 
    USING (species_id)
WHERE ROUND(score/max_score*100,2) > %s
ORDER BY experiment_date DESC
;"""
    cursor.execute(query,(score,))
    experiments = cursor.fetchall()
    cursor.close()
    return experiments

def get_experiments_by_score_and_type(
        conn: connection,
        experiment_type: str,
        score: int) -> list[dict]:
    """Returns all the experiments of a specific type and above a base score"""
    cursor = conn.cursor()
    query = """
SELECT 
    TO_CHAR(experiment_date,'YYYY-MM-DD') as experiment_date,
    experiment_id,
    type_name as experiment_type,
    ROUND(score/max_score*100,2) as score,
    species_name as species,
    subject_id
FROM experiment
JOIN experiment_type
    USING (experiment_type_id)
JOIN subject
    USING (subject_id)
JOIN species 
    USING (species_id)
WHERE ROUND(score/max_score*100,2) > %s
AND type_name = %s
ORDER BY experiment_date DESC
;"""
    cursor.execute(query,(score,experiment_type))
    experiments = cursor.fetchall()
    cursor.close()
    return experiments

def delete_experiment_by_id(conn: connection, experiment_id: int)-> dict:
    """Deletes an experiment by its id."""
    cursor = conn.cursor()
    query = """
DELETE FROM experiment
WHERE experiment_id = %s
RETURNING experiment_id,TO_CHAR(experiment_date,'YYYY-MM-DD') as experiment_date"""
    cursor.execute(query,(experiment_id,))
    deleted_experiment = cursor.fetchone()
    conn.commit()
    cursor.close()
    return deleted_experiment
