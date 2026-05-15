-- Write a query that will find the average scores for each experiment type and species 
-- displaying the following columns:

-- - Type name
-- - Species name
-- - Average score (round to 1 d.p.)

-- Only return the experiment types and species that have an average score of higher than 
-- 5 and order by average score in descending order.

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
    type_name, species_name,ROUND(AVG(score),1) as average_score
    FROM 
        full_table
    GROUP BY 
        type_name,species_name
        HAVING
            AVG(score)>5
    ORDER BY 
        average_score DESC