-- Function to check if a given port code is valid (exists in the ports table)
create or replace function is_valid_port(port_code text)
  returns boolean as
$$
begin
  return exists (select 1 from ports where code = port_code);
end;
$$
  language plpgsql;

-- Example usage
select is_valid_port('a_fake_port_code');