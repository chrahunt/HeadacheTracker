USE headacheDevDB;

/* Clean up tables before populating. */
SET FOREIGN_KEY_CHECKS=0;
TRUNCATE TABLE headache_entries;
TRUNCATE TABLE users;
SET FOREIGN_KEY_CHECKS=1;

/* Set up users. */
INSERT INTO users (username, l_username, first_name, last_name, password_hash, salt) VALUES
('chris', LOWER('chris'), 'Chris', 'Almond', SHA2('password000000000000', 256), '000000000000'),
('seth', LOWER('seth'), 'Seth', 'Cashew', SHA2('password000000000000', 256), '000000000000'),
('bryan', LOWER('bryan'), 'Bryan', 'Peanut', SHA2('password000000000000', 256), '000000000000');

/* Get user IDs. */
SELECT id FROM users WHERE username = 'chris' INTO @chris_id;
SELECT id FROM users WHERE username = 'seth' INTO @seth_id;
SELECT id FROM users WHERE username = 'bryan' INTO @bryan_id;

INSERT INTO headache_entries (entry_start, entry_end, severity, user_id) VALUES 
('2014-03-01 02:00:00', '2014-03-01 03:00:00', 4, @chris_id),
('2014-03-02 23:45:00', '2014-03-03 03:00:00', 3, @chris_id),
('2014-03-04 12:45:00', '2014-03-04 15:00:00', 4, @chris_id),
('2014-01-04 09:45:00', '2014-01-04 12:00:00', 7, @chris_id),
('2014-02-01 02:00:00', '2014-02-01 03:00:00', 4, @seth_id),
('2014-02-02 23:45:00', '2014-02-03 03:00:00', 3, @seth_id),
('2014-02-04 12:45:00', '2014-02-04 15:00:00', 4, @seth_id),
('2014-01-04 09:45:00', '2014-01-04 12:00:00', 7, @seth_id),
('2014-01-01 02:00:00', '2014-01-01 03:00:00', 4, @bryan_id),
('2014-01-02 23:45:00', '2014-01-03 03:00:00', 3, @bryan_id),
('2014-01-04 09:45:00', '2014-01-04 12:00:00', 7, @bryan_id),
('2014-01-04 12:45:00', '2014-01-04 15:00:00', 4, @bryan_id);
