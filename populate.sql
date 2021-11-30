-- populate.sql
-- Everything in this script should be Data Manipulation Language (DML), no data definition.
-- Run ONCE to create and refresh database from scratch.
-- -- TODO:: According to our TA: 
--      "You will need to include more data tuples in your database in phase 3.
--       A good number would be around 100, or maybe 10 for certain tables that 
--       are difficult to insert tuples. You may synthesize some randomly sampled
--       data in the data creation process, it does not necessarily need to be meaningful,
--       but you should have a good amount of them to demo in phase 3, so that your application
--       works like an application that returns or processes over a good amount of data."

.mode csv
.import csv/users.csv users