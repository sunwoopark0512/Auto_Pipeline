CREATE OR REPLACE FUNCTION anon_event() RETURNS trigger AS $$
BEGIN
  NEW.meta = jsonb_set(NEW.meta, '{email}', '"***"');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_anon
BEFORE INSERT ON event_log
FOR EACH ROW EXECUTE PROCEDURE anon_event();
