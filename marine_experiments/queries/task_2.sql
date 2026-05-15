-- The government agency (who would like you to know that they have your best interest at heart) want to be able to understand the performance of the animals relative to the maximum scores in the experiments. 
-- Write a query that should return a set of rows that give information about subject's performance in each experiment. Each object should contain the following information only:

-- Experiment ID
-- Subject ID
-- Species
-- Experiment Date
-- Experiment Type Name
-- Score
-- Score should be expressed as a percentage rounded to 2 d.p. (e.g. "70.34%"). The percentage score should be calculated based on the maximum score for that type of experiment.

-- Dates should be expressed as strings in the YYYY-MM-DD format.

-- Experiments should be sorted in descending order by date.

WITH 
    full_table AS
        (SELECT 
            *
        FROM
            subject AS su
        JOIN species AS se
            USING (species_id)
        JOIN experiment as e
            USING (subject_id)
        JOIN experiment_type as et
            USING (experiment_type_id)
    ) 
SELECT 
    experiment_id,
    subject_id,
    species_name as species,
    experiment_date,
    type_name as experiment_type,
    to_char(ROUND(score/max_score*100,2),'FM999D00%') AS score
FROM 
    full_table
ORDER BY experiment_date DESC
;