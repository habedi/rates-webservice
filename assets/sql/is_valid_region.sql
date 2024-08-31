-- This function checks if a region with the given slug exists in the regions table
create or replace function is_valid_region(region_slug text)
  returns boolean as
$$
begin
  return exists (select 1 from regions where slug = region_slug);
end;
$$
  language plpgsql;

-- Example usage:
select is_valid_region('baltic');