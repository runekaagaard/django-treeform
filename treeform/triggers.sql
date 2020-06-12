CREATE TRIGGER treeform_version_view_movie_schema 
    AFTER UPDATE 
    ON movies_director
BEGIN
    INSERT INTO treeform_schemaversion (`schema`, `version`, `object_id`)
        VALUES("view_movie_schema", OLD.version+1, NEW.id) 
        ON CONFLICT(id)
            SET version=OLD.version;
END;

