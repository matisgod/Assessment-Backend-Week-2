-- The government agency would like to see a combined view of information about its (volunteered) subjects. Write a query that will return information about subjects, 
-- and the species that they are - specifically including the columns:

-- Subject ID
-- Subject Name
-- Species Name
-- Date of Birth
-- Dates should be expressed in the YYYY-MM format.

-- Objects should be ordered by date of birth in descending order.

SELECT subject_id, subject_name, species_name,to_char(date_of_birth, 'YYYY-MM') as date_of_birth
    FROM subject
JOIN species 
    USING (species_id)
ORDER BY date_of_birth DESC
;