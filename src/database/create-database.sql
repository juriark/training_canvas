-- Dummy Setup - replace with .sh file to run alembic migrations
CREATE TABLE project (
	id SERIAL PRIMARY key,
	project_name character varying(255) not NULL
);

INSERT INTO project (id, project_name) VALUES
(1, 'initial_training_using_sketch_dataset');