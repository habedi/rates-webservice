-- Create a B-tree index on the day column of the prices table to speed up queries that filter by day
-- It will be very handy when the number of rows in the prices table grows
create index if not exists idx_day on prices (day);