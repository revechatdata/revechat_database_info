# revechat_database_info

# vbuser Table Documentation

## Overview
The `vbuser` table stores user account information, authentication details, profile data, status flags, and system access permissions.

---

## Table Structure

| Column Name | Data Type | Default | Nullable | Description |
|-------------|-----------|----------|----------|-------------|
| ID | bigint(20) | AUTO_INCREMENT | No | Primary key. Unique identifier for each user. |
| usAccount | varchar(20) | NULL | Yes | Username or login account name. |
| usSha1Password | varchar(50) | NULL | Yes | SHA1 encrypted password. |
| usPassword | varchar(50) | NULL | Yes | Legacy or plain password storage (not recommended). |
| usRoleID | decimal(18,0) | NULL | Yes | Role identifier defining user permissions. |
| usrMailAddr | varchar(50) | — | No | User email address. |
| usrMailServer | varchar(50) | NULL | Yes | Associated mail server. |
| usDesignation | varchar(100) | NULL | Yes | User job title or designation. |
| usAddress | varchar(255) | NULL | Yes | User physical or mailing address. |
| usPhoneNo | varchar(100) | NULL | Yes | User contact phone number. |
| usAdditionalInfo | varchar(255) | NULL | Yes | Additional information about the user. |
| usAccCreateTime | timestamp | CURRENT_TIMESTAMP | No | Account creation timestamp. |
| usOnlineStatus | int(11) | 0 | Yes | Online status (0 = Offline, 1 = Online). |
| usProfileStatus | smallint(6) | 1 | Yes | Profile status flag. |
| usLastLoginTime | decimal(18,0) | NULL | Yes | Last login timestamp (Unix epoch). |
| usLastLogoutTime | decimal(18,0) | NULL | Yes | Last logout timestamp (Unix epoch). |
| usAccountStatus | int(11) | 1 | Yes | Account status (1 = Active, 0 = Disabled). |
| usLastName | varchar(100) | NULL | Yes | User last name. |
| usFirstName | varchar(100) | NULL | Yes | User first name. |
| usConcurrentChat | int(11) | 0 | Yes | Maximum concurrent chats allowed. |
| isPasswordChanged | smallint(1) | 0 | Yes | Indicates if password was changed (0 = No, 1 = Yes). |
| row_updateTime | decimal(20,0) | 0 | Yes | Last row update timestamp (Unix epoch). |
| isActive | smallint(6) | 1 | Yes | Indicates if the user is active. |
| usUserStatus | smallint(1) | 0 | Yes | Additional user status flag. |
| isOnboardingDone | tinyint(1) | 1 | Yes | Onboarding completion flag (0 = No, 1 = Yes). |
| usProfilePictureURL | varchar(100) | NULL | Yes | URL of the profile picture. |
| created | bigint(20) | NULL | Yes | Record creation timestamp (Unix epoch). |
| updated | bigint(20) | NULL | Yes | Record last update timestamp (Unix epoch). |
| hasBotAccess | tinyint(1) | 1 | Yes | Bot feature access flag (1 = Enabled). |
| hasBillingAccess | tinyint(1) | 1 | Yes | Billing feature access flag (1 = Enabled). |

---

## Notes

- Timestamps are stored as Unix epoch values.
- Plain password storage is not recommended for production systems.
- Consider indexing frequently queried fields like `usAccount`, `usrMailAddr`, and `usRoleID`.


### Retrive user information using account id
```sql
SELECT 
    ID,
    usAccount,
    usrMailAddr,
    usPassword,
    CASE 
        WHEN usRoleID = 1 THEN 'Super Admin'
        WHEN usRoleID = 2 THEN 'Admin'
        WHEN usRoleID = 3 THEN 'Agent'
        ELSE 'Custom Role'
    END AS role_name,
    usAccountStatus,
    isActive
FROM vbuser as v
WHERE usAccount = {{place your account id here}};
```


### Retrive user information using email address

```sql
SELECT 
    ID,
    usAccount,
    usrMailAddr,
    usPassword,
    CASE 
        WHEN usRoleID = 1 THEN 'Super Admin'
        WHEN usRoleID = 2 THEN 'Admin'
        WHEN usRoleID = 3 THEN 'Agent'
        ELSE 'Custom Role'
    END AS role_name,
    usAccountStatus,
    isActive
FROM vbuser as v
WHERE usrMailAddr like '%place your email address here%';
```

### Retrive livechat information using account id

```sql
select * from vbmissedchats;
```
# vbmissedchats Table Documentation

## Table Overview

The `vbmissedchats` table stores information about missed chat sessions, including assignment details, timestamps, SLA metrics, response times, queue information, sentiment analysis, and billing status.

---

## Table Structure

| Column Name | Data Type | Default | Nullable | Description |
|-------------|------------|----------|------------|-------------|
| ID | bigint(20) | AUTO_INCREMENT | NO | Primary key |
| vbAccount | varchar(20) | NULL | YES | Account identifier |
| assignedAgentID | bigint(20) | - | NO | Assigned agent ID |
| assignedVisitorID | bigint(20) | - | NO | Assigned visitor ID |
| vsRecordID | bigint(20) | NULL | YES | Visitor session record ID |
| chatStatus | int(11) | NULL | YES | Chat status code |
| dateTimeStamp | decimal(20,0) | - | NO | Chat record timestamp (epoch) |
| chatRequestTime | decimal(20,0) | - | NO | Chat request time (epoch) |
| chatResponseTime | decimal(20,0) | - | NO | Chat response time (epoch) |
| isMissed | char(1) | '1' | NO | Indicates if chat was missed (1 = Yes) |
| chatRequestType | char(1) | '1' | NO | Type of chat request |
| isTransferred | int(11) | -1 | YES | Transfer status |
| channelType | smallint(6) | 0 | YES | Channel type (Web, WhatsApp, etc.) |
| departmentId | bigint(20) | 0 | YES | Department ID |
| isTriggered | char(1) | '0' | YES | Whether chat was trigger-based |
| isHumanHandover | char(1) | '0' | YES | Indicates bot-to-human handover |
| chatTag | varchar(255) | 'Unreplied' | YES | Chat tag |
| subject | varchar(255) | '' | YES | Chat subject |
| vsChatEndedBy | tinyint(1) | -1 | YES | Who ended the chat |
| vsConversationStartTime | bigint(20) | 0 | YES | Conversation start time |
| vsConversationEndTime | bigint(20) | 0 | YES | Conversation end time |
| isQueued | tinyint(4) | 0 | YES | Whether chat was queued |
| queuePopTime | bigint(20) | 0 | YES | Queue pop time |
| chatDropTime | bigint(20) | 0 | YES | Chat drop time |
| firstResponseTime | bigint(20) | NULL | YES | First response time (ms) |
| avgResponseTime | bigint(20) | NULL | YES | Average response time (ms) |
| isAggregated | tinyint(1) | 0 | YES | Aggregation flag |
| is_agent_chat_processed | tinyint(1) | 0 | YES | Agent chat processed flag |
| last_aggregation_timestamp | decimal(20,0) | 0 | YES | Last aggregation timestamp |
| isOutOfBusinessHour | tinyint(1) | -1 | YES | Out-of-business-hour indicator |
| chatCloseRemark | text | NULL | YES | Closing remarks |
| totalResponseTime | bigint(20) | 0 | YES | Total response time (ms) |
| messageCountForResponseTime | int(11) | 0 | YES | Message count used for response time |
| frt_breach | tinyint(1) | 0 | YES | First response time SLA breach flag |
| ert_breach | tinyint(1) | 0 | YES | Every response time SLA breach flag |
| slaId | bigint(20) | 0 | YES | SLA ID |
| chatAssignedTime | bigint(20) | 0 | YES | Chat assigned timestamp |
| initialResponseTime | bigint(20) | NULL | YES | Initial response time |
| isDeleted | char(1) | '0' | YES | Soft delete flag |
| sentiment | varchar(50) | NULL | YES | Chat sentiment |
| snoozeDuration | bigint(20) | NULL | YES | Snooze duration (ms) |
| is_billed | tinyint(1) | 0 | NO | Billing status flag |

---

## Time Format Notes

Most time-related columns store **epoch timestamps in milliseconds**.


### Retrive Account-wise Chat Request Count

```sql
SELECT 
    COUNT(*) AS chatreq_count
FROM vbmissedchats
WHERE vbAccount = 'your_account_id_here'
;
```

### Retrive Account-wise Chat Request Count

```sql
SELECT 
    DATE(FROM_UNIXTIME(chatRequestTime / 1000)) AS chat_date,
    COUNT(*) AS chatreq_count
FROM vbmissedchats
WHERE vbAccount = 'YOUR_ACCOUNT_ID'
GROUP BY DATE(FROM_UNIXTIME(chatRequestTime / 1000))
ORDER BY chat_date ASC;
```

### Day-wise Count with Date Range Filter

```sql
SELECT 
    DATE(FROM_UNIXTIME(chatRequestTime / 1000)) AS chat_date,
    COUNT(*) AS chatreq_count
FROM vbmissedchats
WHERE vbAccount = 'YOUR_ACCOUNT_ID'
AND FROM_UNIXTIME(chatRequestTime / 1000) 
    BETWEEN '2026-02-01' AND '2026-02-28'
GROUP BY DATE(FROM_UNIXTIME(chatRequestTime / 1000))
ORDER BY chat_date ASC;
```

### Retrive FRT Breach Count for an Account

```sql
SELECT 
    vbAccount,
    COUNT(*) AS frt_breach_count
FROM vbmissedchats
WHERE vbAccount = 'YOUR_ACCOUNT_ID'
  AND frt_breach = 1
GROUP BY vbAccount;
```
-- Add Date Filter (If Needed) 
```sql
AND FROM_UNIXTIME(chatRequestTime / 1000)
    BETWEEN '2026-02-01' AND '2026-02-28'
```


### Retrive ERT Breach Count for an Account

```sql
SELECT 
    vbAccount,
    COUNT(*) AS frt_breach_count
FROM vbmissedchats
WHERE vbAccount = 'YOUR_ACCOUNT_ID'
  AND ert_breach = 1
GROUP BY vbAccount;
```
-- Add Date Filter (If Needed) 
```sql
AND FROM_UNIXTIME(chatRequestTime / 1000)
    BETWEEN '2026-02-01' AND '2026-02-28'
```

### Channel-wise Chat Request Count for a Specific Account

```sql
SELECT 
    channelType,
    COUNT(*) AS chatreq_count
FROM vbmissedchats
WHERE vbAccount = 'YOUR_ACCOUNT_ID'
GROUP BY channelType
ORDER BY chatreq_count DESC;
```

-- If you want to map channelType numbers to readable names (Web, WhatsApp, Facebook, etc.)

```sql
SELECT 
    c.channel_name,
    COUNT(v.ID) AS chatreq_count
FROM vbmissedchats v
LEFT JOIN channellistentity c 
    ON v.channelType = c.channel_code and c.service_name = 'livechat'
GROUP BY c.channel_name
ORDER BY chatreq_count DESC;
```

# vbsingle_message Table Documentation

## Table Overview

The `vbsingle_message` table stores individual chat messages exchanged between agents and visitors.  
It contains message metadata, delivery status, timestamps, and message content.

---

## Table Structure

| Column Name   | Data Type     | Default | Nullable | Description |
|---------------|--------------|----------|------------|-------------|
| id | bigint(20) | AUTO_INCREMENT | NO | Primary key |
| created | bigint(20) | NULL | YES | Message creation timestamp (epoch ms) |
| updated | bigint(20) | NULL | YES | Message last update timestamp (epoch ms) |
| agentId | bigint(20) | NULL | YES | Agent ID who sent the message |
| chatInfoId | bigint(20) | NULL | YES | Related chat/session ID |
| messageType | varchar(255) | NULL | YES | Type of message (text, image, file, etc.) |
| msg | mediumtext | NULL | YES | Message content |
| visitorId | bigint(20) | NULL | YES | Visitor ID who sent/received message |
| messageId | varchar(190) | NULL | YES | Unique external message identifier |
| deliveryStatus | varchar(20) | NULL | YES | Delivery status (sent, delivered, read, failed, etc.) |

---

## Time Format Notes

All timestamp columns (`created`, `updated`) are stored in **epoch format (milliseconds)**.

---

## Functional Coverage

- Agent & Visitor Messaging
- Message Tracking
- Delivery Status Monitoring
- Message Type Classification
- Session-based Message Linking

---

