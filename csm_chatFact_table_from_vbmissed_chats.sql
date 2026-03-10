CREATE TABLE silver.ChatFact (
    chat_id BIGINT        ,          -- surrogate key
    account_id INT NOT NULL,              -- account (FK to AccountDim)
    agent_id INT,                        -- assigned agent (FK to AgentDim)
    visitor_id INT,                      -- assigned visitor
    department_id INT,                   -- department (FK to DeptDim)
    sla_id INT,                          -- SLA reference

    -- Time Stamps
    request_time TIMESTAMP,                 -- chatrequesttime
    response_time TIMESTAMP,                -- chatresponsetime
    assigned_time TIMESTAMP,                -- chatassignedtime
    conversation_start_time TIMESTAMP,      -- vsconversationstarttime
    conversation_end_time TIMESTAMP,        -- vsconversationendtime
    drop_time TIMESTAMP,                    -- chatdroptime
    close_remark_time TIMESTAMP,            -- chatcloseremark if timestamped

    -- Durations (Derived)
    wait_time_sec NUMERIC,                  -- request_time → response_time
    conversation_duration_sec NUMERIC,      -- start → end
    response_duration_sec NUMERIC,          -- avg response time
    queue_duration_sec NUMERIC,             -- queued to picked
    total_response_time_sec NUMERIC,        -- totalresponsetime

    -- Metrics / Flags
    is_missed SMALLINT,
    is_transferred SMALLINT,
    is_triggered SMALLINT,
    is_human_handover SMALLINT,
    is_queued SMALLINT,
    is_out_of_business_hour SMALLINT,
    is_deleted SMALLINT,

    -- Performance Indicators
    frt_breach SMALLINT,
    ert_breach SMALLINT,

    -- Chat Metadata
    chat_status TEXT,
    chat_request_type TEXT,
    channel_type TEXT,
    chat_ended_by TEXT,
    sentiment TEXT,
    snooze_duration NUMERIC,
    message_count INT,
    subject TEXT,

    -- Date Dimension keys (optional for analysis)
    date_id DATE,
    day_of_week SMALLINT,
    hour_of_day smallint,
    day_name VARCHAR(20)
);



select * from vbmissedchats;




INSERT INTO silver.ChatFact (
    chat_id,
    account_id,
    agent_id,
    visitor_id,
    department_id,
    sla_id,
    request_time,
    response_time,
    assigned_time,
    conversation_start_time,
    conversation_end_time,
    drop_time,
    close_remark_time,
    wait_time_sec,
    conversation_duration_sec,
    response_duration_sec,
    queue_duration_sec,
    total_response_time_sec,
    is_missed,
    is_transferred,
    is_triggered,
    is_human_handover,
    is_queued,
    is_out_of_business_hour,
    is_deleted,
    frt_breach,
    ert_breach,
    chat_status,
    chat_request_type,
    channel_type,
    chat_ended_by,
    sentiment,
    snooze_duration,
    message_count,
    subject,
    date_id,
    day_of_week,
    hour_of_day,
    day_name
)
SELECT
    id AS chat_id,
    vbaccount::INT AS account_id,
    assignedagentid::INT AS agent_id,
    assignedvisitorid::INT AS visitor_id,
    departmentid::INT AS department_id,
    slaid::INT AS sla_id,
    --
    TO_TIMESTAMP(chatrequesttime/1000) AS request_time,
    TO_TIMESTAMP(chatresponsetime/1000) AS response_time,
    TO_TIMESTAMP(chatassignedtime/1000) AS assigned_time,
    TO_TIMESTAMP(vsconversationstarttime/1000) AS conversation_start_time,
    TO_TIMESTAMP(vsconversationendtime/1000) AS conversation_end_time,
    TO_TIMESTAMP(chatdroptime/1000) AS drop_time,
    NULL AS close_remark_time, 
    -- populate if you have a timestamp for chatcloseremark
    EXTRACT(EPOCH FROM (TO_TIMESTAMP(chatresponsetime/1000) - TO_TIMESTAMP(chatrequesttime/1000))) AS wait_time_sec,
    EXTRACT(EPOCH FROM (TO_TIMESTAMP(vsconversationendtime/1000) - TO_TIMESTAMP(vsconversationstarttime/1000))) AS conversation_duration_sec,
    avgresponsetime AS response_duration_sec,
    EXTRACT(EPOCH FROM (TO_TIMESTAMP(queuepoptime/1000) - TO_TIMESTAMP(chatrequesttime/1000))) AS queue_duration_sec,
    totalresponsetime AS total_response_time_sec,
    --
    ismissed::SMALLINT AS is_missed,
    istransferred AS is_transferred,
    istriggered::SMALLINT AS is_triggered,
    ishumanhandover::SMALLINT AS is_human_handover,
    isqueued AS is_queued,
    isoutofbusinesshour AS is_out_of_business_hour,
    isdeleted::SMALLINT AS is_deleted,
    --
    frt_breach AS frt_breach,
    ert_breach AS ert_breach,
    --
    chatstatus AS chat_status,
    chatrequesttype AS chat_request_type,
    channeltype AS channel_type,
    vschatendedby AS chat_ended_by,
    sentiment,
    snoozeduration,
    messagecountforresponsetime AS message_count,
    subject,
    --
    TO_TIMESTAMP(chatrequesttime/1000)::DATE AS date_id,
    EXTRACT(DOW FROM TO_TIMESTAMP(chatrequesttime/1000))::SMALLINT AS day_of_week,
    EXTRACT(HOUR FROM TO_TIMESTAMP(chatrequesttime/1000))::SMALLINT AS hour_of_day,
    TRIM(TO_CHAR(TO_TIMESTAMP(chatrequesttime/1000), 'Day')) AS day_name
FROM vbmissedchats
where id > 22698974;
