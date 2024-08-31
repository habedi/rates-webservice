-- The function that returns the average daily prices for a given date range, source port set, destination port set
create or replace function get_average_daily_prices(
  from_date date,
  to_date date,
  source_port_set text[],
  destination_port_set text[],
  count_threshold integer -- Should be 3 based on task's requirements
)
  returns table
          (
            day           date,
            average_price numeric
          )
as
$$
begin
  return query
    with all_dates as (select generate_series(from_date, to_date, '1 day') as day)
    select ad.day::date,
           case
             when count(p.day) < count_threshold then null
             else avg(p.price)
             end as average_price
    from all_dates ad
           left join prices p on ad.day = p.day
      and p.orig_code = any (source_port_set)
      and p.dest_code = any (destination_port_set)
    group by ad.day
    order by ad.day;
end;
$$ language plpgsql;

-- Example usage
select *
from get_average_daily_prices(
  '2016-01-01'::date, -- from_date
  '2016-01-10'::date, -- to_date
  array ['CNSGH'], -- source_port_set
  (select array(select port_code from get_region_ports('north_europe_main'))), -- destination_port_set with subquery
  3 -- count_threshold (3 for this task)
     );