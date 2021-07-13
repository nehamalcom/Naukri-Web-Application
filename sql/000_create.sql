DROP TABLE IF EXISTS openings;
DROP TABLE IF EXISTS job_status;
DROP TABLE IF EXISTS crawl_status;

CREATE TABLE crawl_status (
  crawled_on timestamp
);

CREATE TABLE job_status (
  id serial primary key,
  name text,
  terminal boolean
);

INSERT INTO job_status (name, terminal) VALUES ('crawled', FALSE);
INSERT INTO job_status (name, terminal) VALUES ('applied', FALSE);
INSERT INTO job_status (name, terminal) VALUES ('ignored', FALSE);
INSERT INTO job_status (name, terminal) VALUES ('selected', FALSE);
INSERT INTO job_status (name, terminal) VALUES ('rejected', FALSE);

CREATE TABLE openings (
  id serial primary key,
  title text,
  job_id text,
  company_name text,
  jd_url text,
  jd_text text,
  status serial references job_status(id),
  crawled_on date
);
