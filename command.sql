INSERT INTO info_categories (category, req) 
    VALUES ('Additional Information', TRUE);

INSERT INTO info_categories (category, descr, req) 
    VALUES ('Password', 'you will need your password when you edit information for this pet', TRUE);

SELECT * FROM info_categories;