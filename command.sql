CREATE FUNCTION get_table_columns(tname text, sname text DEFAULT 'public')
RETURNS TABLE (column_name text) AS $$
BEGIN
    RETURN QUERY EXECUTE format('
        SELECT column_name::text
        FROM information_schema.columns
        WHERE table_schema = %L AND table_name = %L;
    ', sname, tname);
END;
$$ LANGUAGE plpgsql;