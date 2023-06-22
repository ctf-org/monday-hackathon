/*
 * create landing layer where files from json stored
 */
CREATE SCHEMA IF NOT EXISTS monday_lnd;
SET search_path TO monday_lnd;

-- table for users
DROP TABLE IF EXISTS monday_lnd.lnd_users;
CREATE TABLE monday_lnd.lnd_users(data jsonb);
COPY monday_lnd.lnd_users FROM '/data/users_formatted.json';
--select * from monday_lnd.lnd_users

-- table for boards
DROP TABLE IF EXISTS monday_lnd.lnd_boards;
CREATE TABLE monday_lnd.lnd_boards(data jsonb);
COPY monday_lnd.lnd_boards FROM '/data/boards_formatted.json';
--SELECT * FROM monday_lnd.lnd_boards;

-- table for tasks
DROP TABLE IF EXISTS monday_lnd.lnd_tasks;
CREATE TABLE monday_lnd.lnd_tasks(data jsonb);
COPY monday_lnd.lnd_tasks FROM '/data/tasks_formatted.json';

-- table for times
DROP TABLE IF EXISTS monday_lnd.lnd_times;
CREATE TABLE monday_lnd.lnd_times(data jsonb);
COPY monday_lnd.lnd_times FROM '/data/times_formatted.json';
--SELECT * FROM monday_lnd.lnd_times;

CREATE SCHEMA IF NOT EXISTS monday_src;
--SET search_path TO monday_src;

----------------------------------------------------------------
DROP TABLE IF EXISTS monday_src.users;
CREATE TABLE monday_src.users(
  id 		integer PRIMARY KEY,
  username 	varchar,
  email 	varchar,
  role 		varchar,
  update_dt timestamp DEFAULT current_date
);

INSERT INTO monday_src.users (id, username, email)
	SELECT CAST(DATA->>'id' AS integer), 
		DATA->>'name', 
		DATA->>'email' 
	FROM monday_lnd.lnd_users;
-- SELECT * FROM monday_src.users u ;


-----------------------------------------------------------------------
DROP TABLE IF EXISTS monday_src.boards;
CREATE TABLE monday_src.boards(
  id 		integer PRIMARY KEY,
  board_name varchar,
  creator 	integer,
  update_dt timestamp DEFAULT current_date
);

INSERT INTO monday_src.boards (id, board_name, creator)
	SELECT 
		CAST(DATA->>'id' AS integer), 
		DATA->>'name', 
		CAST((DATA->>'creator')::jsonb->>'id' AS integer)
	FROM monday_lnd.lnd_boards
	WHERE DATA->>'type' = 'board';

-----------------------------------------------------------------------
DROP TABLE IF EXISTS monday_src.tasks;
CREATE TABLE monday_src.tasks(
  id integer PRIMARY KEY,
  task_name varchar,
  board_id integer,
  create_dt timestamp DEFAULT current_date,
  update_dt timestamp DEFAULT current_date
);


INSERT INTO monday_src.tasks (id, task_name, create_dt, board_id)
	SELECT 
		CAST(DATA->>'task_id' AS integer), 
		DATA->>'task_name', 
		(DATA->>'created_at')::timestamp,
		(DATA->>'board_id')::integer
	FROM monday_lnd.lnd_tasks;


-- table with working times
DROP TABLE IF EXISTS monday_src.time_tracking;
CREATE TABLE IF NOT EXISTS monday_src.time_tracking(
  id integer PRIMARY KEY,
  task_id integer,
  board_id integer,
  started_at timestamp,
  ended_at timestamp,
  started_user_id integer,
  ended_user_id integer,
  status varchar,
  created_at timestamp,
  updated_at timestamp
  -- FOREIGN KEY ("started_user_id") 	REFERENCES "users" ("id"),
  -- FOREIGN KEY ("ended_user_id") 	REFERENCES "users" ("id"),
  -- FOREIGN KEY ("task_id") 			REFERENCES "tasks" ("id")
);
-- TRUNCATE monday_src.time_tracking;

INSERT INTO monday_src.time_tracking 
	(id, 
	task_id, 
	started_user_id, 
	ended_user_id, 
	started_at, 
	ended_at,
	created_at,
	updated_at,
	board_id)
	SELECT 
		(DATA->>'id')::integer,
		(DATA->>'project_id')::integer,
		(DATA->>'started_user_id')::integer,
		(DATA->>'ended_user_id')::integer,
		(DATA->>'started_at')::timestamp,
		(DATA->>'ended_at')::timestamp,
		(DATA->>'created_at')::timestamp,
		(DATA->>'updated_at')::timestamp,
		(DATA->>'board_id')::integer 
	FROM monday_lnd.lnd_times
;
