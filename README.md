# REVE Chat Database Info

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

# vbbotinfo Table Documentation

## Table Overview

The `vbbotinfo` table stores chatbot configuration details including bot identity, metadata, language settings, channel enablement, ML configuration, UI positioning, and lifecycle status.

This table acts as the primary configuration registry for bots under different accounts.

---

## Table Structure

| Column Name | Data Type | Default | Nullable | Description |
|-------------|------------|----------|------------|-------------|
| id | bigint(20) | AUTO_INCREMENT | NO | Primary key |
| vbAccount | varchar(20) | NULL | YES | Account identifier |
| botId | varchar(200) | NULL | YES | Unique bot identifier |
| botName | varchar(200) | NULL | YES | Internal bot name |
| botBody | longtext | NULL | YES | Bot flow definition / configuration body |
| last_update | decimal(20,0) | NULL | YES | Last update timestamp (epoch ms) |
| avatar_name | varchar(100) | NULL | YES | Bot avatar name |
| is_social_channel_enabled | tinyint(4) | NULL | YES | Social channel enable flag |
| sampleBot | int(11) | 0 | YES | Indicates if bot is sample bot |
| displayName | varchar(255) | NULL | YES | Public display name of the bot |
| tagLine | varchar(255) | NULL | YES | Bot tagline |
| trigger_event | text | NULL | YES | Trigger event configuration |
| is_web_channel_enabled | tinyint(4) | NULL | YES | Web channel enable flag |
| isDraft | int(11) | 0 | YES | Draft status flag |
| fallback_settings | text | NULL | YES | Fallback configuration settings |
| google_login | text | NULL | YES | Google login integration settings |
| bot_accuracy_level | double(3,2) | 0.50 | YES | ML accuracy threshold |
| greeting_message | text | NULL | YES | Bot greeting message |
| language_message | text | NULL | YES | Language selection message |
| is_bot_enabled | tinyint(4) | 1 | YES | Bot active status flag |
| enabledSocialChannels | varchar(250) | NULL | YES | List of enabled social channels |
| created | bigint(20) | NULL | YES | Creation timestamp (epoch ms) |
| updated | bigint(20) | NULL | YES | Last update timestamp (epoch ms) |
| is_sample_new | int(11) | NULL | YES | New sample bot indicator |
| botMetaInfo_ID | bigint(20) | NULL | YES | Bot meta information reference ID |
| is_deleted | bit(1) | - | NO | Soft delete flag |
| ml_model_file_name | text | NULL | YES | ML model file name |
| description | varchar(255) | NULL | YES | Bot description |
| supported_language | varchar(200) | NULL | YES | Supported languages list |
| webpage_settings | text | NULL | YES | Web widget configuration |
| is_mobile_sdk_channel_enabled | tinyint(4) | 0 | YES | Mobile SDK channel enable flag |
| is_knowledgebase_connected | tinyint(4) | 0 | YES | Knowledgebase integration flag |
| build_with | varchar(20) | CUSTOM | YES | Bot build type (CUSTOM / AI / etc.) |
| positionX | decimal(10,2) | NULL | YES | UI X-axis position |
| positionY | decimal(10,2) | NULL | YES | UI Y-axis position |
| startNodeId | bigint(20) | NULL | YES | Starting node ID of bot flow |
| languageCode | varchar(100) | en | YES | Default language code |
| version | bigint(20) | 0 | YES | Bot version number |
| is_updated | tinyint(1) | 1 | YES | Indicates if bot is updated |

---

## Time Format Notes

Timestamp columns (`created`, `updated`, `last_update`) are stored in **epoch format (milliseconds)**.

Example conversion in MySQL:

```sql
SELECT FROM_UNIXTIME(created / 1000)
FROM vbbotinfo;
```

---

## Functional Coverage

- Bot Identity & Metadata
- Channel Enablement (Web, Social, Mobile SDK)
- ML Model Configuration
- Greeting & Fallback Management
- Draft & Version Control
- Language & Localization Settings
- Knowledgebase Integration
- UI Positioning
- Soft Delete & Lifecycle Management

---


# bot_conversations Table Documentation

## Table Overview

The `bot_conversations` table stores aggregated chatbot conversation data per visitor session.  
It includes conversation metadata, engagement metrics, fallback tracking, sentiment, handover status, and billing information.

This table is typically used for analytics, reporting, and bot performance monitoring.

---

## Table Structure

| Column Name | Data Type | Default | Nullable | Description |
|-------------|------------|----------|------------|-------------|
| id | bigint(20) | AUTO_INCREMENT | NO | Primary key |
| visitor_id | bigint(20) | - | NO | Visitor identifier |
| message | longtext | - | NO | Full aggregated conversation message/body |
| account | varchar(15) | - | NO | Account identifier |
| timestamp | bigint(20) | - | NO | Conversation creation timestamp (epoch ms) |
| channelType | tinyint(1) | NULL | YES | Channel type identifier |
| isAggregated | tinyint(1) | 0 | YES | Aggregation status flag |
| vsRecordId | bigint(20) | NULL | YES | Visitor session record ID |
| botId | bigint(20) | NULL | YES | Bot identifier |
| numberOfMessage | bigint(20) | NULL | YES | Total number of messages in conversation |
| startTime | bigint(20) | 0 | YES | Conversation start time (epoch ms) |
| endTime | bigint(20) | 0 | YES | Conversation end time (epoch ms) |
| endedBy | int(11) | 0 | YES | Indicates who ended the conversation |
| fallbackCount | int(11) | 0 | YES | Number of fallback responses triggered |
| openEndedQueryCount | int(11) | 0 | YES | Count of open-ended user queries |
| is_aggregated_analytics | int(11) | 0 | YES | Analytics aggregation flag |
| isHumanHandover | tinyint(1) | 0 | YES | Indicates bot-to-human handover |
| completedGoalCount | int(11) | 0 | YES | Number of successfully completed goals |
| sentiment | varchar(50) | NULL | YES | Conversation sentiment analysis result |
| is_billed | tinyint(1) | 0 | NO | Billing status flag |

---

## Time Format Notes

All timestamp-related fields (`timestamp`, `startTime`, `endTime`) are stored in **epoch format (milliseconds)**.


## Functional Coverage

- Bot Conversation Storage
- Conversation Aggregation
- Performance Analytics
- Fallback Monitoring
- Open-Ended Query Tracking
- Goal Completion Tracking
- Sentiment Analysis
- Human Handover Tracking
- Billing Monitoring

---

# vbsingle_message_bot Table Documentation

## Table Overview

The `vbsingle_message_bot` table stores individual bot message records exchanged during bot conversations.  
It captures message content, metadata, delivery status, and visitor linkage.

This table is primarily used for bot-level message tracking and analytics.

---

## Table Structure

| Column Name | Data Type | Default | Nullable | Description |
|-------------|------------|----------|------------|-------------|
| id | bigint(20) | AUTO_INCREMENT | NO | Primary key |
| created | bigint(20) | NULL | YES | Message creation timestamp (epoch ms) |
| updated | bigint(20) | NULL | YES | Last update timestamp (epoch ms) |
| botId | bigint(20) | NULL | YES | Bot identifier |
| botChatId | bigint(20) | NULL | YES | Bot conversation/chat ID reference |
| msg | mediumtext | NULL | YES | Bot message content |
| visitorId | bigint(20) | NULL | YES | Visitor identifier |
| messageId | varchar(190) | NULL | YES | External or unique message identifier |
| deliveryStatus | varchar(20) | NULL | YES | Delivery status (sent, delivered, read, failed, etc.) |

---

## Time Format Notes

Timestamp fields (`created`, `updated`) are stored in **epoch format (milliseconds)**.

---

## Functional Coverage

- Bot Message Storage
- Visitor-Bot Interaction Tracking
- Message Delivery Monitoring
- Conversation-level Message Linking
- Bot Analytics Support

---

## Related Tables

- `bot_conversations` → Aggregated conversation data
- `vbbotinfo` → Bot configuration details
- `channellistentity` → Channel mapping (if applicable)

---




### Account-wise Bot Conversation Count
```sql
SELECT 
    account,
    COUNT(*) AS conversation_count
FROM bot_conversations
GROUP BY account
ORDER BY conversation_count DESC;
```

### Day-wise Conversation Count for a Specific Account
```sql
SELECT 
    DATE(FROM_UNIXTIME(timestamp / 1000)) AS conversation_date,
    COUNT(*) AS conversation_count
FROM bot_conversations
WHERE account = 'YOUR_ACCOUNT_ID'
GROUP BY DATE(FROM_UNIXTIME(timestamp / 1000))
ORDER BY conversation_date ASC;
```

### Channel-wise Conversation Count
```sql
SELECT 
    c.channel_name,
    COUNT(b.id) AS conversation_count
FROM bot_conversations b
LEFT JOIN channellistentity c
    ON b.channelType = c.channel_code and c.service_name = 'chatbot'
GROUP BY c.channel_name
ORDER BY conversation_count DESC;
```



# vbapisettings Table Documentation

## Table Overview

The `vbapisettings` table stores API configuration settings for accounts.  
It manages API definitions, publishing state, testing status, metadata, and configuration payload.

This table is typically used for Live Chat API, Bot API, or other integration configurations.

---

## Table Structure

| Column Name | Data Type | Default | Nullable | Description |
|-------------|------------|----------|------------|-------------|
| id | bigint(20) | AUTO_INCREMENT | NO | Primary key |
| name | varchar(255) | - | NO | API configuration name |
| created | bigint(20) | NULL | YES | Creation timestamp (epoch ms) |
| updated | bigint(20) | NULL | YES | Last update timestamp (epoch ms) |
| createdBy | bigint(20) | NULL | YES | User ID who created the configuration |
| updatedBy | bigint(20) | NULL | YES | User ID who last updated the configuration |
| accountId | varchar(255) | NULL | YES | Account identifier |
| description | longtext | NULL | YES | Description of the API configuration |
| isPublished | bit(1) | 0 | YES | Indicates if API configuration is published |
| isDrafted | bit(1) | 0 | YES | Indicates if API configuration is in draft state |
| data | longtext | NULL | YES | API configuration payload (JSON or structured data) |
| isTested | bit(1) | 0 | YES | Indicates if API configuration has been tested |
| type | varchar(100) | LIVECHAT | YES | API type (e.g., LIVECHAT, BOT, etc.) |

---

## Time Format Notes

Timestamp fields (`created`, `updated`) are stored in **epoch format (milliseconds)**.

---

## Functional Coverage

- API Configuration Management
- Draft & Publish Lifecycle Control
- Testing Status Tracking
- Account-level API Segmentation
- Live Chat / Bot API Integration Settings
- Metadata & Version Tracking

---

## Related Modules

- Live Chat Integration
- Bot Integration
- External API Connectivity
- Account Configuration Management

---

### Total API Count for a Specific Account
```sql
SELECT 
    accountId,
    COUNT(*) AS api_count
FROM vbapisettings
WHERE accountId = 'YOUR_ACCOUNT_ID'
GROUP BY accountId;
```

### Only Published APIs Count
```sql
SELECT 
    accountId,
    COUNT(*) AS published_api_count
FROM vbapisettings
WHERE accountId = 'YOUR_ACCOUNT_ID'
  AND isPublished = 1
GROUP BY accountId;
```

### Only Draft APIs Count
```sql
SELECT 
    accountId,
    COUNT(*) AS draft_api_count
FROM vbapisettings
WHERE accountId = 'YOUR_ACCOUNT_ID'
  AND isDrafted = 1
GROUP BY accountId;
```


# vbscriptsettings Table Documentation

## Table Overview

The `vbscriptsettings` table stores script configuration settings for accounts.  
It manages script definitions, publishing state, draft state, testing status, metadata, and script payload configuration.

This table is typically used for automation scripts, workflow scripts, or account-level scripting configurations.

---

## Table Structure

| Column Name | Data Type | Default | Nullable | Description |
|-------------|------------|----------|------------|-------------|
| id | bigint(20) | AUTO_INCREMENT | NO | Primary key |
| name | varchar(255) | - | NO | Script configuration name |
| created | bigint(20) | NULL | YES | Creation timestamp (epoch ms) |
| updated | bigint(20) | NULL | YES | Last update timestamp (epoch ms) |
| createdBy | bigint(20) | NULL | YES | User ID who created the script |
| updatedBy | bigint(20) | NULL | YES | User ID who last updated the script |
| accountId | varchar(255) | NULL | YES | Account identifier |
| description | longtext | NULL | YES | Description of the script configuration |
| isPublished | bit(1) | 0 | YES | Indicates if the script is published |
| isDrafted | bit(1) | 0 | YES | Indicates if the script is in draft state |
| data | longtext | NULL | YES | Script configuration payload (JSON or structured data) |
| isTested | bit(1) | 0 | YES | Indicates if the script has been tested |

---

## Time Format Notes

Timestamp fields (`created`, `updated`) are stored in **epoch format (milliseconds)**.

---

## Functional Coverage

- Script Configuration Management
- Draft & Publish Lifecycle Control
- Testing Status Tracking
- Account-level Script Segmentation

---

## Related Modules

- API Settings (`vbapisettings`)
- Bot Configuration (`vbbotinfo`)
- Live Chat / Automation Engine
- Account Configuration Management

---

### Total Script Count for a Specific Account
```sql
SELECT 
    accountId,
    COUNT(*) AS script_count
FROM vbscriptsettings
WHERE accountId = 'YOUR_ACCOUNT_ID'
GROUP BY accountId;
```

### Published Script Count
```sql
SELECT 
    accountId,
    COUNT(*) AS published_script_count
FROM vbscriptsettings
WHERE accountId = 'YOUR_ACCOUNT_ID'
  AND isPublished = 1
GROUP BY accountId;
```

### Draft Script Count
```sql
SELECT 
    accountId,
    COUNT(*) AS draft_script_count
FROM vbscriptsettings
WHERE accountId = 'YOUR_ACCOUNT_ID'
  AND isDrafted = b'1'
GROUP BY accountId;
```
