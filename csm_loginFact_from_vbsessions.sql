CREATE TABLE silver.LoginFact (
    login_id BIGSERIAL,        -- surrogate key
    account_id BIGINT NOT NULL,            -- from vbaccount
    agent_id BIGINT NOT NULL,              -- from userid
    start_time TIMESTAMP NOT NULL,         -- converted from unix
    end_time TIMESTAMP,                    -- converted from unix
    duration_minutes NUMERIC,              -- derived
    date_id DATE NOT NULL,                 -- YYYY-MM-DD from start_time
    day_of_week INT,                       -- 0=Sunday, 1=Monday...
    hour_of_day INT,                       -- 0–23
    day_name VARCHAR(20)                   -- e.g., Monday, Tuesday...
);


INSERT INTO silver.LoginFact (
    account_id,
    agent_id,
    start_time,
    end_time,
    duration_minutes,
    date_id,
    day_of_week,
    hour_of_day,
    day_name
)
SELECT
    CAST(vbaccount AS BIGINT) AS account_id,
    CAST(userid AS BIGINT) AS agent_id,
    TO_TIMESTAMP(start_session/1000)::TIMESTAMP AS start_time,
    TO_TIMESTAMP(end_session/1000)::TIMESTAMP AS end_time,
    EXTRACT(EPOCH FROM (TO_TIMESTAMP(end_session/1000) - TO_TIMESTAMP(start_session/1000))) / 60 AS duration_minutes,
    TO_TIMESTAMP(start_session/1000)::DATE AS date_id,
    EXTRACT(DOW FROM TO_TIMESTAMP(start_session/1000))::INT AS day_of_week,
    EXTRACT(HOUR FROM TO_TIMESTAMP(start_session/1000))::INT AS hour_of_day,
    TRIM(TO_CHAR(TO_TIMESTAMP(start_session/1000), 'Day')) AS day_name
FROM vbsession v
where v.id >10426344;
