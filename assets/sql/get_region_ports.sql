-- Function to get all ports within a region and its children recursively (using a recursive CTE)
-- Note this is a (pure) SQL function not a PL/pgSQL function; I think it's easier for the database engine to optimize
create or replace function get_region_ports(region_slug text)
  returns table
          (
            port_code text
          )
as
$$
with recursive
  regionhierarchy as (
    -- Anchor query: Get ports directly belonging to the given region
    select code
    from ports
    where parent_slug = region_slug
    union all
    -- Recursive query: Get ports belonging to the child regions of the given region
    select p.code
    from ports p
           join regions r on p.parent_slug = r.slug
           join regionhierarchy rh on r.parent_slug = rh.code),
  childregions as (
    -- Find all direct child regions of the given region
    select slug
    from regions
    where parent_slug = region_slug
    union all
    -- Recursive query: Find all child regions of the child regions found so far
    select r.slug
    from regions r
           join childregions cr on r.parent_slug = cr.slug)
-- Select all ports within the given region and its children
select code
from ports
where parent_slug in (select slug from childregions)
   or parent_slug = region_slug;
$$
  language sql;

-- Example usage:
select get_region_ports('baltic');