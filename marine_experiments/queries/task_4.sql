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

SELECT species_name,experiment_id,is_predator,
    CASE 
        WHEN is_predator THEN score*1.2
        ELSE score 
        END
        AS score
    FROM full_table
ORDER BY score DESC
;