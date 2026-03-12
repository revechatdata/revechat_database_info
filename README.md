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

# intent Table Documentation

## Overview
The `intent` table stores chatbot intent definitions used in conversational automation.

Each record represents an intent within a chatbot flow. An intent typically contains a name, response message, and metadata related to the bot configuration. Intents are used to define how the chatbot responds to user inputs and are often connected within visual bot flows. The table also stores UI layout information used in the chatbot flow builder (such as node position and size).

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| ID | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each intent record. |
| intent_id | varchar(40) | Yes | NULL | Unique identifier for the intent used internally within the chatbot system. |
| name | varchar(200) | Yes | NULL | Name of the intent used for identification in the chatbot flow. |
| response | mediumtext | Yes | NULL | Default response message associated with the intent. |
| account_id | varchar(20) | Yes | NULL | Identifier of the account that owns the intent. |
| bot_id | bigint(20) | Yes | NULL | Identifier of the chatbot associated with the intent. |
| type | varchar(50) | Yes | NULL | Type of intent node (e.g., message, condition, action, etc.). |
| created_time | bigint(20) | Yes | NULL | Timestamp indicating when the intent was initially created (Unix epoch). |
| serialNo | int(11) | Yes | NULL | Serial number used to maintain ordering of intents. |
| is_deleted | tinyint(1) | Yes | 0 | Indicates whether the intent has been soft-deleted. |
| created | bigint(20) | Yes | NULL | Timestamp representing when the intent record was created. |
| updated | bigint(20) | Yes | NULL | Timestamp representing the last update to the intent record. |
| positionx | decimal(10,2) | Yes | NULL | X-coordinate position of the intent node in the chatbot visual flow builder. |
| positionY | decimal(10,2) | Yes | NULL | Y-coordinate position of the intent node in the chatbot visual flow builder. |
| width | decimal(10,2) | Yes | NULL | Width of the intent node in the chatbot flow editor UI. |
| height | decimal(10,2) | Yes | NULL | Height of the intent node in the chatbot flow editor UI. |
| version | bigint(20) | Yes | 0 | Version number used for tracking changes or updates to the intent. |
| is_updated | tinyint(1) | Yes | 1 | Indicates whether the intent has been updated since the last version. |
| note | longtext | Yes | NULL | Additional notes or metadata related to the intent. |
| flowId | bigint(20) | Yes | NULL | Identifier of the chatbot flow to which the intent belongs. |

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


# billing_subscription Table Documentation

## Table Overview

The `billing_subscription` table stores subscription and billing information for customer accounts.  
It tracks package details, pricing, discounts, billing periods, temporary migration data, tax, and subscription status.

This table is primarily used for subscription lifecycle management, billing calculations, and financial reporting.

---

## Table Structure

| Column Name | Data Type | Default | Nullable | Description |
|-------------|------------|----------|------------|-------------|
| id | bigint(20) | AUTO_INCREMENT | NO | Primary key |
| addons_price | double | NULL | YES | Price of add-ons applied to subscription |
| agent_count | int(11) | - | NO | Number of active agents in subscription |
| balance | double | NULL | YES | Current subscription balance |
| billing_currency | varchar(255) | NULL | YES | Currency used for billing |
| created | bigint(20) | - | NO | Subscription creation timestamp (epoch ms) |
| creator_id | bigint(20) | NULL | YES | User ID who created the subscription |
| customer_id | varchar(255) | NULL | YES | Customer identifier |
| discount | double | NULL | YES | Discount applied to subscription |
| end_date | bigint(20) | NULL | YES | Subscription end date (epoch ms) |
| migration_status | int(11) | NULL | YES | Migration status indicator |
| month_count | int(11) | NULL | YES | Subscription duration in months |
| operator_code | varchar(255) | - | NO | Account/operator identifier |
| package_code | int(11) | - | NO | Package identifier |
| payment_method_token | varchar(255) | NULL | YES | Payment method reference token |
| start_date | bigint(20) | - | NO | Subscription start date (epoch ms) |
| status | int(11) | - | NO | Subscription status code [2: 14 days Trail 1: Customer] | 
| tmp_agent_count | int(11) | - | NO | Temporary agent count (pending update) |
| tmp_balance | double | NULL | YES | Temporary balance |
| tmp_billing_currency | varchar(255) | NULL | YES | Temporary billing currency |
| tmp_discount | double | NULL | YES | Temporary discount |
| tmp_end_date | bigint(20) | NULL | YES | Temporary end date |
| tmp_month_count | int(11) | NULL | YES | Temporary subscription duration |
| tmp_package_code | int(11) | - | NO | Temporary package code |
| tmp_start_date | bigint(20) | NULL | YES | Temporary start date |
| used_coupon_id | bigint(20) | NULL | YES | Applied coupon ID |
| tax | double | 0 | YES | Tax amount applied |

---

## Time Format Notes

Timestamp fields (`created`, `start_date`, `end_date`, `tmp_start_date`, `tmp_end_date`) are stored in **epoch format (milliseconds)**.

---

## Functional Coverage

- Subscription Lifecycle Management
- Package & Agent Allocation
- Billing & Balance Tracking
- Discount & Coupon Handling
- Temporary Migration Handling
- Tax Calculation
- Subscription Status Monitoring

---


# billing_package Table Documentation

## Table Overview

The `billing_package` table stores subscription package details.  
Each package defines pricing per agent and acts as a reference for subscriptions in the `billing_subscription` table.

This table is primarily used for:
- Subscription pricing calculations
- Package management
- Revenue computation
- Billing configuration

---

## Table Structure

| Column Name | Data Type | Default | Nullable | Description |
|-------------|------------|----------|------------|-------------|
| id | bigint(20) | AUTO_INCREMENT | NO | Primary key |
| code | int(11) | - | NO | Unique package code (used in subscription table) |
| monthly_rate_per_agent | int(11) | - | NO | Monthly cost per agent |
| name | varchar(255) | - | NO | Package name |

Relationship logic:

```
billing_subscription.package_code = billing_package.code
```

### SQL to find out currently active clients 
```sql
SELECT 
    bs.id,
    bs.operator_code,
    bp.name as package_name,
    bs.agent_count,
    bs.addons_price,
    bs.balance,
    bs.billing_currency,
    bs.discount,
    bs.month_count,
    bs.status,
    bs.migration_status,
    bs.customer_id,
    bs.payment_method_token,
    bs.used_coupon_id,
-- 
    -- Formatted Date Columns
    FROM_UNIXTIME(bs.created / 1000)        AS created_datetime,
    FROM_UNIXTIME(bs.start_date / 1000)     AS start_datetime,
    FROM_UNIXTIME(bs.end_date / 1000)       AS end_datetime,
    FROM_UNIXTIME(bs.tmp_start_date / 1000) AS tmp_start_datetime,
    FROM_UNIXTIME(bs.tmp_end_date / 1000)   AS tmp_end_datetime,
-- 
    -- Temporary Fields
    bs.tmp_agent_count,
    bs.tmp_balance,
    bs.tmp_billing_currency,
    bs.tmp_discount,
    bs.tmp_month_count,
    bs.tmp_package_code
-- 
FROM billing_subscription bs
JOIN (
    SELECT operator_code, MAX(id) AS max_id
    FROM billing_subscription
    GROUP BY operator_code
) latest 
    ON bs.operator_code = latest.operator_code 
   AND bs.id = latest.max_id
-- 
JOIN billing_package bp ON bp.code = bs.package_code  
WHERE FROM_UNIXTIME(bs.end_date / 1000) >= CURDATE();
```


### SQL to find out currently active clients system calculated MRR

```sql

SELECT 
    bs2.operator_code,
    tbl_user.usrMailAddr,
    bp.name AS package_name,
    bs2.agent_count,
    bs2.tmp_discount,
    DATEDIFF(
        DATE(FROM_UNIXTIME(bs2.end_date / 1000)),
        DATE(FROM_UNIXTIME(bs2.start_date / 1000))
    ) AS last_subscription_duration,
    DATE(FROM_UNIXTIME(bs2.end_date / 1000)) AS end_date,
    CASE
        WHEN month_count = 1 THEN 
            ROUND(
                (bp.monthly_rate_per_agent * agent_count) 
                + addons_price 
                - tmp_discount, 
            2)
        WHEN month_count = 12 THEN 
            ROUND(
                (CAST(bp.monthly_rate_per_agent AS DECIMAL(10,2)) 
                * CAST(agent_count AS DECIMAL(10,2))) 
                + (addons_price / 12) 
                - (tmp_discount / 12), 
            2)
        WHEN month_count = 24 THEN 
            ROUND(
                (bp.monthly_rate_per_agent * agent_count) 
                + (addons_price / 24) 
                - (tmp_discount / 24), 
            2)
    END AS mrr
FROM (
    SELECT 
        bs.operator_code,
        MAX(id) AS mxid
    FROM revechat.billing_subscription bs
    GROUP BY bs.operator_code
) AS tbl
INNER JOIN revechat.billing_subscription bs2 
    ON bs2.id = tbl.mxid
INNER JOIN revechat.billing_package bp 
    ON bp.code = bs2.package_code
LEFT JOIN (
    SELECT 
        v.usAccount,
        v.usrMailAddr
    FROM revechat.vbuser v
    WHERE v.usRoleID = 1
) AS tbl_user 
    ON tbl_user.usAccount = bs2.operator_code
WHERE FROM_UNIXTIME(bs2.end_date / 1000) >= CURRENT_DATE()
AND DATEDIFF(
        DATE(FROM_UNIXTIME(bs2.end_date / 1000)),
        DATE(FROM_UNIXTIME(bs2.start_date / 1000))
) NOT IN (13, 14);
```


# nb_feature Table Documentation

## Overview
The `nb_feature` table stores feature definitions used in the system’s package or subscription configuration.  
Each record represents a feature that can be assigned to a package, optionally tracked, reset monthly, or configured as an add-on.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | int(11) | No | Auto Increment | Primary key. Unique identifier for each feature. |
| feature_name | varchar(100) | No | — | Human-readable name of the feature. |
| feature_type | enum('fixed','recurring') | No | — | Defines whether the feature is fixed or recurring. |
| code | varchar(50) | No | — | Unique system code for referencing the feature programmatically. |
| is_addon | tinyint(1) | No | 0 | Indicates whether the feature is an add-on (1 = Yes, 0 = No). |
| monthly_reset | tinyint(1) | No | 0 | Determines if the feature usage resets monthly (1 = Yes, 0 = No). |
| is_coupon_applicable | tinyint(1) | No | 1 | Specifies if coupons can be applied to this feature (1 = Yes, 0 = No). |
| created | bigint(20) | No | — | Creation timestamp (Unix epoch in milliseconds). |
| updated | bigint(20) | No | — | Last update timestamp (Unix epoch in milliseconds). |
| trackable | tinyint(1) | Yes | 0 | Indicates whether feature usage is tracked (1 = Yes, 0 = No). |

---

## Field Details

### feature_type
Defines the behavior of the feature:
- `fixed` → One-time or non-recurring feature
- `recurring` → Feature usage renews periodically (e.g., monthly)

### Boolean Flags
The following fields use boolean logic:

| Value | Meaning |
|------|--------|
| 1 | Enabled / True |
| 0 | Disabled / False |

Applicable fields:
- is_addon
- monthly_reset
- is_coupon_applicable
- trackable

# nb_billing_duration Table Documentation

## Overview
The `nb_billing_duration` table defines available subscription billing durations in the system.  
It supports trial periods, monthly plans, and yearly plans with optional discounts.

Each record represents a billing cycle configuration used in pricing or package definitions.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | int(11) | No | Auto Increment | Primary key. Unique identifier for billing duration. |
| duration_type | enum('trial','monthly','yearly') | No | — | Type of billing duration. |
| count | int(11) | No | 1 | Number of duration units (e.g., 3 months, 2 years). |
| discount_percentage | decimal(5,2) | No | 0.00 | Discount applied for this billing duration. |
| created | bigint(20) | No | — | Creation timestamp (Unix epoch in milliseconds). |
| updated | bigint(20) | No | — | Last update timestamp (Unix epoch in milliseconds). |

# nb_package Table Documentation

## Overview
The `nb_package` table stores subscription or product package definitions in the system.

Each record represents a unique package that can be assigned features, pricing, and billing durations.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | int(11) | No | Auto Increment | Primary key. Unique identifier for each package. |
| package_name | varchar(100) | No | — | Human-readable name of the package. |
| code | varchar(20) | No | — | Unique system code for referencing the package programmatically. |
| created | bigint(20) | No | — | Creation timestamp (Unix epoch in milliseconds). |
| updated | bigint(20) | No | — | Last update timestamp (Unix epoch in milliseconds). |



# nb_currency Table Documentation

## Overview
The `nb_currency` table stores supported currency definitions used for pricing, billing, and payment processing in the system.

Each record represents a currency with its code and display symbol.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | int(11) | No | Auto Increment | Primary key. Unique identifier for each currency. |
| name | varchar(50) | No | — | Full name of the currency (e.g., US Dollar). |
| code | varchar(3) | No | — | Standard 3-letter currency code (ISO format). |
| symbol | varchar(5) | No | — | Currency symbol used for display (e.g., $, ৳). |
| created | bigint(20) | No | — | Creation timestamp (Unix epoch in milliseconds). |
| updated | bigint(20) | No | — | Last update timestamp (Unix epoch in milliseconds). |


# nb_region Table Documentation

## Overview
The `nb_region` table stores geographic or business regions used for pricing, currency mapping, taxation, or package availability.

Each record represents a uniquely identifiable region within the system.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | int(11) | No | Auto Increment | Primary key. Unique identifier for each region. |
| region_name | varchar(100) | No | — | Human-readable name of the region. |
| code | varchar(10) | No | — | Unique system code representing the region. |
| created | bigint(20) | No | — | Creation timestamp (Unix epoch in milliseconds). |
| updated | bigint(20) | No | — | Last update timestamp (Unix epoch in milliseconds). |


# nb_package_base_price Table Documentation

## Overview
The `nb_package_base_price` table stores base pricing configurations for packages.

It defines the price of a package based on:
- Region
- Currency
- Billing duration

This table enables localized pricing strategies for subscription packages.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | int(11) | No | Auto Increment | Primary key. Unique identifier for the pricing record. |
| package_id | int(11) | No | — | Reference to the package being priced. |
| region_id | int(11) | No | — | Reference to the applicable region. |
| price | double | No | — | Base price of the package. |
| currency_id | int(11) | No | — | Reference to the currency used for pricing. |
| billing_duration_id | int(11) | No | — | Reference to the billing duration. |
| created | bigint(20) | No | — | Creation timestamp (Unix epoch in milliseconds). |
| updated | bigint(20) | No | — | Last update timestamp (Unix epoch in milliseconds). |


# nb_feature_unit_price Table Documentation

## Overview
The `nb_feature_unit_price` table stores unit-level pricing for individual features.

It allows feature pricing to vary based on:
- Package
- Region
- Currency

This table is primarily used for add-ons, usage-based features, or trackable feature billing.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | int(11) | No | Auto Increment | Primary key. Unique identifier for each feature price record. |
| package_id | int(11) | No | — | Reference to the package where the feature is available. |
| region_id | int(11) | No | — | Reference to the applicable region. |
| feature_id | int(11) | No | — | Reference to the feature being priced. |
| price | decimal(10,2) | No | — | Unit price of the feature. |
| currency_id | int(11) | No | — | Currency used for pricing. |
| created | bigint(20) | No | — | Creation timestamp (Unix epoch in milliseconds). |
| updated | bigint(20) | No | — | Last update timestamp (Unix epoch in milliseconds). |

---

## Relationships

| Column | References | Description |
|-------|-----------|-------------|
| package_id | nb_package.id | Associated package |
| region_id | nb_region.id | Applicable region |
| feature_id | nb_feature.id | Feature being priced |
| currency_id | nb_currency.id | Pricing currency |

---

## Pricing Logic
- Each feature can have different prices depending on region.
- Pricing is defined at the package + feature + region level.
- Supports usage-based billing and add-on feature monetization.

# nb_package_wise_capability Table Documentation

## Overview
The `nb_package_wise_capability` table defines feature availability and usage limits for each package.

It controls:
- Whether a feature is enabled for a package
- Whether the feature is included or optional
- Minimum and maximum usage limits

This table is central to package configuration and feature entitlement logic.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | int(11) | No | 0 | Unique identifier for the capability record. |
| package_id | int(11) | No | — | Reference to the package. |
| feature_id | int(11) | No | — | Reference to the feature. |
| minimum_cap | int(11) | No | 0 | Minimum allowed usage or allocation. |
| max_cap | int(11) | No | -1 | Maximum allowed usage or allocation (-1 indicates unlimited). |
| is_enabled | tinyint(1) | No | 1 | Indicates whether the feature is enabled for the package. |
| is_included | tinyint(1) | No | 0 | Indicates whether the feature is included by default in the package. |
| created | bigint(20) | No | — | Creation timestamp (Unix epoch in milliseconds). |
| updated | bigint(20) | No | — | Last update timestamp (Unix epoch in milliseconds). |

---

## Relationships

| Column | References | Description |
|-------|-----------|-------------|
| package_id | nb_package.id | Associated package |
| feature_id | nb_feature.id | Associated feature |

---

## Capability Logic

### Usage Limits
| Value | Meaning |
|------|--------|
| max_cap = -1 | Unlimited usage |
| minimum_cap = 0 | No guaranteed allocation |

### Feature Availability
| Field | Value | Meaning |
|------|------|--------|
| is_enabled | 1 | Feature is available in package |
| is_enabled | 0 | Feature is disabled |
| is_included | 1 | Included in base package price |
| is_included | 0 | Optional or add-on feature |



# nb_cart Table Documentation

## Overview
The `nb_cart` table stores shopping cart information for users.  

Each record represents a cart containing selected packages, features, add-ons, prices, and discounts. The `items` column stores all the details in JSON format.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for the cart. |
| account_id | varchar(100) | Yes | NULL | Optional account identifier for the user. |
| user_id | bigint(20) | No | — | Identifier of the user who owns the cart. |
| items | text | Yes | NULL | JSON storing all cart items, features, pricing, discounts, and add-ons. |
| status | varchar(20) | Yes | NULL | Current cart status (e.g., `active`, `completed`, `abandoned`). |
| created | bigint(20) | Yes | NULL | Cart creation timestamp (Unix epoch in milliseconds). |
| updated | bigint(20) | Yes | NULL | Last update timestamp (Unix epoch in milliseconds). |

---

## items Column JSON Structure

The `items` column stores the entire cart contents in a JSON format.  

### Sample JSON

```json
{
  "couponId": null,
  "couponDto": null,
  "billingDurationId": 1,
  "packageId": 3,
  "regionId": 1,
  "currencyId": 1,
  "features": [
    {"featureId": 126, "quantity": 3, "price": 0.0, "priceAfterDiscount": 0.0, "subscriptionPrice": 0.0, "subscriptionPriceAfterDiscount": 0.0},
    {"featureId": 128, "quantity": 4005, "price": 0.2, "priceAfterDiscount": 0.2, "subscriptionPrice": 0.2, "subscriptionPriceAfterDiscount": 0.2}
  ],
  "addonsFeatures": [
    {"featureId": 11, "quantity": 1, "price": 8.0, "priceAfterDiscount": 8.0, "subscriptionPrice": 8.0, "subscriptionPriceAfterDiscount": 8.0}
  ],
  "subtotal": 68.19,
  "subtotalForSubscriptionCycle": 68.19,
  "discountApplicableFeatureTotalPrices": null,
  "discountApplicableFeatureTotalPricesForSubscription": null,
  "fixedFeaturePrices": 0.0,
  "packagePrice": 60.19,
  "totalDiscount": 0.0,
  "totalDiscountDiscountForSubscriptionCycle": 0.0,
  "walletBalance": 0.0,
  "payableAmount": 68.19,
  "calculatedPackageBasePrice": 59.99
}
```

# access_info Table Documentation

## Overview
The `access_info` table stores authentication and installation details for Shopify stores that have installed the application.

It keeps information such as the store URL, access tokens, Shopify account details, subscription status, and installation/uninstallation timestamps. This table is mainly used to manage store authentication, track app installations, and monitor subscription status.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | int(11) | No | Auto Increment | Primary key. Unique identifier for each store record. |
| store_url | varchar(255) | No | — | Shopify store URL where the app is installed. |
| access_token | varchar(255) | No | — | Shopify API access token used for authenticated API calls. |
| install_date | varchar(255) | Yes | NULL | Date when the application was installed on the Shopify store. |
| hmac | varchar(255) | No | — | HMAC hash used to verify Shopify request authenticity. |
| access_code | varchar(255) | No | — | Authorization code received from Shopify during OAuth process. |
| shopify_username | varchar(255) | Yes | NULL | Name of the Shopify store owner or account user. |
| shopify_email | varchar(255) | Yes | NULL | Email address associated with the Shopify store account. |
| phone | varchar(50) | Yes | NULL | Contact phone number of the Shopify account user. |
| password | varchar(100) | Yes | NULL | Password associated with the account (if used for internal authentication). |
| subscription_id | varchar(100) | Yes | NULL | Identifier of the subscription associated with the store. |
| subscription_status | enum('active','inactive') | Yes | 'inactive' | Indicates whether the store's subscription is currently active or inactive. |
| uninstall_date | datetime | Yes | NULL | Date and time when the app was uninstalled from the Shopify store. |
| account_id | varchar(150) | Yes | NULL | Internal account identifier associated with the store. |
| widget_id | varchar(200) | Yes | NULL | Identifier for the widget linked with the store installation. |

---


# canned_response Table Documentation

## Overview
The `canned_response` table stores predefined responses (also known as canned messages) used by support agents during customer conversations.

These responses help agents quickly reply to common customer queries, improving response time and ensuring consistent communication. Each canned response can optionally belong to a department or category and may include attachments or HTML formatted content.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each canned response. |
| account_id | varchar(255) | Yes | NULL | Identifier of the account to which the canned response belongs. |
| canned_key | varchar(255) | Yes | NULL | Shortcut key or label used to quickly search or trigger the canned response. |
| canned_message | text | Yes | NULL | Plain text version of the canned response message. |
| department_id | bigint(20) | Yes | NULL | Identifier of the department associated with the canned response. |
| cannedMessageCategoryId | bigint(20) | No | -1 | Category identifier used to group similar canned responses. |
| attachments | mediumtext | Yes | NULL | Stores attachment metadata (such as files or media) associated with the canned response. |
| canned_message_html | text | Yes | NULL | HTML formatted version of the canned response message used for rich text responses. |

---

# trigger_instances Table Documentation

## Overview
The `trigger_instances` table stores configuration details for automated triggers used in the chat or engagement system.

Triggers are used to automatically send messages or display banners to visitors based on predefined conditions such as visitor behavior, time spent on a page, agent availability, or widget language. Each trigger belongs to an account and can be prioritized, activated, or configured with additional UI elements like banners and sub-headers.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each trigger instance. |
| name | varchar(200) | No | — | Name of the trigger used for internal identification. |
| message | varchar(500) | Yes | NULL | Message that will be sent or displayed when the trigger fires. |
| account_id | varchar(20) | No | — | Identifier of the account that owns the trigger. |
| active | tinyint(1) | No | — | Indicates whether the trigger is active (`1`) or inactive (`0`). |
| priority | int(11) | No | — | Determines the execution priority of the trigger when multiple triggers match conditions. |
| unique_visitor | tinyint(1) | Yes | 0 | Indicates whether the trigger should fire only once per unique visitor. |
| attr_widget_lang | varchar(10) | Yes | 'en' | Language attribute of the widget for which the trigger applies. |
| attr_text_color | varchar(100) | Yes | '#FFFFFF' | Text color used when displaying the trigger message. |
| agent_status | int(11) | Yes | 2 | Agent availability condition required for the trigger to fire (e.g., online, offline, or any status). |
| match_all_condition | tinyint(1) | Yes | 0 | Defines whether all conditions must match (`1`) or any condition can match (`0`). |
| banner_enabled | tinyint(1) | Yes | 0 | Indicates whether a banner should be displayed along with the trigger. |
| sub_header_enabled | tinyint(1) | Yes | 0 | Indicates whether a sub-header message is enabled for the trigger. |
| banner_attachments | longtext | Yes | NULL | Stores attachment information related to the trigger banner. |
| banner_image | varchar(128) | Yes | NULL | Path or filename of the banner image associated with the trigger. |
| sub_header_message | varchar(128) | Yes | NULL | Additional message displayed as a sub-header when the trigger fires. |
| time_to_trigger | int(11) | Yes | 0 | Delay time (usually in seconds) before the trigger is activated after conditions are met. |
| visitor_closed_trigger_firing_strategy | varchar(20) | Yes | 'INTERVAL' | Strategy used to determine when a trigger should fire again after a visitor closes it. |
| visitor_closed_trigger_firing_delay | int(11) | Yes | 43200 | Delay time before the trigger can fire again after being closed by the visitor (in seconds). |

---
# trigger_condition_values Table Documentation

## Overview
The `trigger_condition_values` table stores condition values associated with triggers.  
These conditions define the rules that must be satisfied for a trigger to fire.

Each record represents a specific condition linked to a trigger instance. The table typically works together with the `trigger_instances` table, allowing triggers to be executed based on various visitor attributes, behaviors, or system-defined rules.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | int(11) | No | Auto Increment | Primary key. Unique identifier for each trigger condition value record. |
| type_id | int(11) | No | — | Identifier representing the type of condition (e.g., URL match, visitor attribute, time on page, etc.). |
| field_values | mediumtext | Yes | NULL | Stores the value(s) associated with the condition. Often stored as serialized data or JSON containing multiple condition parameters. |
| trigger_id | int(11) | No | — | Identifier of the trigger instance this condition belongs to. |

---


# ticketinfoentity Table Documentation

## Overview
The `ticketinfoentity` table stores ticket-related information used in the customer support or helpdesk system.

Each record represents a ticket created within the system and contains references to identifiers used across different systems (such as relational databases and MongoDB). The table also stores metadata like creator, visitor, timestamps, and a serialized or JSON representation of the ticket data.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each ticket record. |
| accountId | varchar(20) | Yes | NULL | Identifier of the account associated with the ticket. |
| ticketMongoId | varchar(150) | Yes | NULL | Identifier of the ticket stored in MongoDB. |
| ticketId | varchar(100) | Yes | NULL | Human-readable or system-generated ticket ID used within the platform. |
| ticketUUID | varchar(150) | Yes | NULL | Universally unique identifier (UUID) for the ticket. |
| creatorId | bigint(20) | Yes | NULL | Identifier of the user or agent who created the ticket. |
| visitorId | bigint(20) | Yes | NULL | Identifier of the visitor or customer associated with the ticket. |
| created | bigint(20) | Yes | NULL | Timestamp representing when the ticket was created (typically Unix epoch). |
| updated | bigint(20) | Yes | NULL | Timestamp representing the last update to the ticket (typically Unix epoch). |
| ticketStr | longtext | Yes | NULL | Serialized or JSON representation of the full ticket data including details, messages, and metadata. |

---
##  Total Ticket Count Account wise
```sql
SELECT 
    accountId,
    COUNT(id) AS total_tickets
FROM ticketentity
WHERE isDeleted = 0 OR isDeleted IS NULL
GROUP BY accountId
ORDER BY total_tickets DESC;
```
##  Monthly Ticket Count Account wise
```sql
SELECT 
    accountId,
    DATE_FORMAT(FROM_UNIXTIME(created/1000), '%Y-%m') AS month,
    COUNT(id) AS tickets_created
FROM ticketentity
WHERE isDeleted = 0 OR isDeleted IS NULL
GROUP BY accountId, month
ORDER BY accountId, month;
```
##  Overdue Ticket Ratio
```sql
SELECT 
    accountId,
    COUNT(id) AS total_tickets,
    SUM(isOverDue) AS overdue_tickets,
    ROUND(SUM(isOverDue)/COUNT(id) * 100,2) AS overdue_percentage
FROM ticketentity
WHERE isDeleted = 0 OR isDeleted IS NULL
GROUP BY accountId;
```

# ticketconversationentity Table Documentation

## Overview
The `ticketconversationentity` table stores conversation messages associated with support tickets.

Each record represents a single message exchanged within a ticket thread. Messages may be sent by agents, customers, or the system and include metadata such as sender information, message type, visibility level, and email delivery status. This table allows the system to maintain the full conversation history for every support ticket.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each ticket conversation message. |
| created | bigint(20) | Yes | NULL | Timestamp indicating when the message was created (typically Unix epoch). |
| updated | bigint(20) | Yes | NULL | Timestamp indicating the last update to the message (typically Unix epoch). |
| mailSendingStatus | varchar(255) | Yes | NULL | Status of the email notification related to the message (e.g., sent, failed, pending). |
| message | longtext | Yes | NULL | The content of the message exchanged within the ticket conversation. |
| messageSender | varchar(255) | Yes | NULL | Identifier or role of the message sender (e.g., agent, visitor, system). |
| messageType | varchar(255) | Yes | NULL | Type of message such as comment, reply, note, or system-generated message. |
| messageVisibility | varchar(255) | Yes | NULL | Visibility level of the message (e.g., public to customer or internal note for agents). |
| ticketId | varchar(150) | Yes | NULL | Identifier of the ticket associated with this conversation message. |
| userId | bigint(20) | Yes | NULL | Identifier of the user or agent who sent the message. |
| messageId | varchar(150) | Yes | NULL | Unique identifier for the message within the conversation thread. |
| inReplyTo | varchar(150) | Yes | NULL | References the message ID that this message is replying to. |

---
# ticketentity Table Documentation

## Overview
The `ticketentity` table stores the primary information related to support tickets within the helpdesk system.

Each record represents a support ticket created by a visitor, agent, or system. The table maintains ticket metadata such as subject, description, status, priority, assigned agent, visitor information, timestamps, and associated communication references. It acts as the core table for managing ticket lifecycle and workflow within the support system.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each ticket record. |
| created | bigint(20) | Yes | NULL | Timestamp representing when the ticket was created (Unix epoch). |
| updated | bigint(20) | Yes | NULL | Timestamp representing the last update time of the ticket (Unix epoch). |
| accountId | varchar(50) | Yes | NULL | Identifier of the account associated with the ticket. |
| chatInfoId | bigint(20) | Yes | NULL | Identifier linking the ticket to a related chat session if created from chat. |
| description | longtext | Yes | NULL | Detailed description of the issue or request submitted in the ticket. |
| isDeleted | bit(1) | Yes | NULL | Indicates whether the ticket has been soft-deleted. |
| subject | varchar(255) | Yes | NULL | Title or subject of the ticket. |
| assignee_id | bigint(20) | Yes | NULL | Identifier of the agent assigned to handle the ticket. |
| status_id | bigint(20) | Yes | NULL | Identifier representing the current status of the ticket (e.g., open, pending, closed). |
| visitor_record_id | bigint(20) | No | — | Identifier of the visitor associated with the ticket. |
| isSpammed | bit(1) | Yes | NULL | Indicates whether the ticket has been marked as spam. |
| attachments | mediumtext | Yes | NULL | Stores metadata or references for files attached to the ticket. |
| confirmationEmailStatus | varchar(255) | No | — | Status indicating whether a confirmation email has been sent for the ticket. |
| hasNewMsg | bit(1) | Yes | NULL | Indicates whether there are new unread messages in the ticket. |
| creator_id | bigint(20) | Yes | NULL | Identifier of the user or system entity that created the ticket. |
| creationSource | varchar(255) | No | — | Source from which the ticket was created (e.g., email, chat, form). |
| ticketId | varchar(50) | No | — | Unique ticket identifier used within the system for referencing tickets. |
| mailMsgId | varchar(150) | Yes | NULL | Identifier of the email message associated with the ticket creation or update. |
| isAggregated | tinyint(1) | Yes | 0 | Indicates whether the ticket has been aggregated with other related tickets. |
| dueDate | bigint(20) | Yes | NULL | Timestamp indicating the due date for resolving the ticket. |
| isOverDue | tinyint(1) | Yes | 0 | Indicates whether the ticket has passed its due date. |
| priority_id | bigint(20) | Yes | NULL | Identifier representing the priority level of the ticket. |
| formId | bigint(20) | Yes | NULL | Identifier of the form used to create the ticket. |
| ticketUUID | varchar(150) | Yes | NULL | Universally unique identifier (UUID) for the ticket. |
| statusGroupId | bigint(20) | Yes | NULL | Identifier representing a grouped category of ticket statuses. |
| visitorName | varchar(255) | Yes | NULL | Name of the visitor who created or is associated with the ticket. |
| visitorEmail | varchar(255) | Yes | NULL | Email address of the visitor associated with the ticket. |

---


# ticketstatusentity Table Documentation

## Overview
The `ticketstatusentity` table defines the different statuses that a support ticket can have within the helpdesk system.

Each record represents a ticket status such as *Open*, *Pending*, *Resolved*, or *Closed*. The table also includes configuration details like status category, display color, notification settings, visitor visibility, SMS/email notifications, and grouping information. These statuses help manage the ticket lifecycle and workflow.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each ticket status. |
| created | bigint(20) | Yes | NULL | Timestamp indicating when the status record was created (Unix epoch). |
| updated | bigint(20) | Yes | NULL | Timestamp indicating the last update to the status record. |
| accountId | varchar(255) | Yes | NULL | Identifier of the account that owns this status configuration. |
| description | varchar(255) | Yes | NULL | Description of the ticket status. |
| statusName | varchar(255) | Yes | NULL | Internal name of the ticket status (e.g., Open, Closed, Pending). |
| cssClassName | varchar(255) | Yes | NULL | CSS class used for styling the status in the user interface. |
| colorCode | varchar(255) | Yes | NULL | Color code associated with the status for UI display purposes. |
| category | varchar(100) | Yes | NULL | Category that groups similar statuses together. |
| type | varchar(100) | Yes | NULL | Type classification of the ticket status. |
| visitorStatusName | varchar(100) | Yes | NULL | Status label displayed to visitors or customers. |
| showVisitor | tinyint(1) | Yes | 1 | Indicates whether the status is visible to visitors (`1`) or internal only (`0`). |
| notify | tinyint(1) | Yes | 0 | Indicates whether notifications should be sent when this status is applied. |
| notifyTo | varchar(255) | Yes | 'VISITOR' | Specifies the target of notifications (e.g., visitor, agent). |
| template_id | bigint(20) | Yes | NULL | Identifier of the email template associated with the status notification. |
| groupId | bigint(20) | Yes | NULL | Identifier referencing the ticket status group. |
| isDeleted | tinyint(1) | Yes | 0 | Indicates whether the status has been soft-deleted. |
| sortNo | int(11) | Yes | NULL | Sorting order used to display statuses in the UI. |
| isDefault | tinyint(1) | Yes | 0 | Indicates whether this status is the default status for new tickets. |
| notifyBySms | tinyint(1) | Yes | 0 | Indicates whether SMS notifications should be sent when this status is triggered. |
| fromNumber | varchar(100) | Yes | NULL | Sender phone number used for SMS notifications. |
| smsTemplateId | varchar(150) | Yes | NULL | Identifier of the SMS template used for status notification. |

---
# ticketstatusgroup Table Documentation

## Overview
The `ticketstatusgroup` table stores groups of ticket statuses used within the helpdesk system.

Status groups help organize multiple ticket statuses into logical categories, making it easier to manage workflows, reporting, and UI display. Each group can belong to an account and may be created by a specific user. Groups can also be marked as default or inactive depending on system configuration.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each ticket status group. |
| accountId | varchar(255) | Yes | NULL | Identifier of the account that owns the status group. |
| creatorId | bigint(20) | Yes | NULL | Identifier of the user who created the status group. |
| title | varchar(255) | No | — | Name or title of the ticket status group. |
| description | text | Yes | NULL | Description explaining the purpose of the status group. |
| status | tinyint(1) | Yes | 0 | Indicates whether the status group is active (`1`) or inactive (`0`). |
| isDefault | tinyint(1) | Yes | 0 | Indicates whether this status group is the default group. |
| created | bigint(20) | Yes | NULL | Timestamp representing when the status group was created (Unix epoch). |
| updated | bigint(20) | Yes | NULL | Timestamp representing the last update time of the status group. |
| isDeleted | tinyint(1) | Yes | 0 | Indicates whether the status group has been soft-deleted. |

---


# campaign Table Documentation

## Overview
The `campaign` table stores information related to marketing or messaging campaigns created within the system.

Each record represents a campaign used to send messages to a targeted audience segment. Campaigns can be associated with templates, contact lists, business accounts, and messaging channels such as WhatsApp or SMS. The table also tracks campaign status, scheduling details, audience size, and message content.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each campaign. |
| created | bigint(20) | Yes | NULL | Timestamp representing when the campaign was created (Unix epoch). |
| updated | bigint(20) | Yes | NULL | Timestamp representing the last update time of the campaign. |
| account_id | varchar(255) | Yes | NULL | Identifier of the account that owns the campaign. |
| title | varchar(255) | Yes | NULL | Name or title of the campaign. |
| template_id | varchar(255) | Yes | NULL | Identifier of the template used for the campaign message. |
| created_by | bigint(20) | Yes | NULL | Identifier of the user who created the campaign. |
| segment_id | bigint(20) | Yes | NULL | Identifier of the audience segment targeted by the campaign. |
| status | varchar(255) | No | 'INITIAL' | Current status of the campaign (e.g., INITIAL, SCHEDULED, RUNNING, COMPLETED). |
| start_time | bigint(20) | Yes | NULL | Scheduled start time of the campaign (Unix epoch). |
| campaign_type | varchar(255) | No | — | Type of campaign (e.g., broadcast, promotional, transactional). |
| business_account_id | varchar(255) | Yes | NULL | Identifier of the business account used for sending campaign messages. |
| message | longtext | Yes | NULL | Message content that will be sent as part of the campaign. |
| description | longtext | Yes | NULL | Additional description or notes about the campaign. |
| title_emoji | varchar(255) | Yes | NULL | Emoji associated with the campaign title for UI display. |
| contact_count | bigint(20) | Yes | NULL | Total number of contacts targeted in the campaign. |
| phone_number_id | varchar(255) | Yes | NULL | Identifier of the phone number used to send campaign messages. |
| contact_file_url | longtext | Yes | NULL | URL of the uploaded contact file used for campaign audience targeting. |
| audience_type | varchar(255) | No | 'UNKNOWN' | Type of audience used for the campaign (e.g., segment, uploaded contacts, unknown). |

---

# vbcontactsegment Table Documentation

## Overview
The `vbcontactsegment` table stores audience segmentation data used for targeted campaigns and messaging.

Each record represents a contact segment created within the system. Segments allow users to group contacts based on specific criteria such as attributes, behaviors, or custom filters. These segments are commonly used for marketing campaigns, automated messaging, and audience targeting.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each contact segment. |
| name | varchar(255) | No | — | Name of the contact segment used for identification. |
| created | bigint(20) | Yes | NULL | Timestamp indicating when the segment was created (Unix epoch). |
| updated | bigint(20) | Yes | NULL | Timestamp indicating the last update time of the segment. |
| accountId | varchar(255) | Yes | NULL | Identifier of the account that owns the contact segment. |
| segmentCriteria | longtext | Yes | NULL | Stores the criteria or filtering rules used to define the segment (often stored as JSON or serialized data). |
| columnList | longtext | Yes | NULL | List of contact fields or attributes used in the segment definition. |
| emoji | varchar(10) | Yes | NULL | Emoji associated with the segment for visual identification in the UI. |

---

# contactinfo Table Documentation

## Overview
The `contactinfo` table stores consolidated contact information for visitors within the system.

Each record represents a contact associated with a specific account and visitor. The table maintains metadata such as communication channel, timestamps, labels, and a set of dynamic attributes.  

All **custom attributes** related to contacts (such as name, email, phone number, company, tags, etc.) are stored inside the `attributes` column, typically in **JSON or serialized format**, allowing flexible storage of additional contact properties.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each contact record. |
| accountId | varchar(20) | No | — | Identifier of the account that owns the contact. |
| visitorId | bigint(20) | No | — | Identifier of the visitor associated with the contact. |
| lastVisitorRecordId | bigint(20) | No | — | Identifier referencing the most recent visitor record associated with this contact. |
| channelType | int(11) | No | — | Represents the communication channel type (e.g., chat, WhatsApp, email, etc.). |
| attributes | text | No | — | Stores all custom contact attributes (such as name, email, phone, company, etc.) in JSON or serialized format. |
| updated | bigint(20) | No | — | Timestamp representing the last update time of the contact record (Unix epoch). |
| lastContactedTimestamp | bigint(20) | Yes | NULL | Timestamp indicating the last time the contact was interacted with. |
| createdTimestamp | bigint(20) | Yes | 0 | Timestamp indicating when the contact record was initially created. |
| isAggregated | tinyint(1) | Yes | 0 | Indicates whether the contact record is aggregated from multiple visitor records. |
| labels | text | Yes | NULL | Stores labels or tags associated with the contact for categorization and filtering. |

---


## Notes

- The **`attributes` column** is the main storage for **custom contact attributes**.
- Attributes may include fields such as:
  - Name
  - Email
  - Phone
  - Company
  - Custom fields created by the account
- Since attributes are stored dynamically, the structure may vary across accounts depending on configured contact properties.

---


# copilot_setting Table Documentation

## Overview
The `copilot_setting` table stores configuration settings for the **Copilot AI assistant** used across different modules of the platform.

These settings define how Copilot features are enabled and used for:
- **Access control** (which agents can use Copilot and what knowledge bases are accessible)
- **Live chat assistance**
- **Ticket support assistance**

Each configuration is stored as **JSON data** in separate columns to allow flexible feature configuration per account.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each Copilot settings record. |
| accountId | varchar(50) | No | — | Identifier of the account associated with the Copilot settings. |
| access_setting | mediumtext | Yes | NULL | JSON configuration defining which agents can access Copilot and what knowledge bases they can use. |
| livechat_setting | mediumtext | Yes | NULL | JSON configuration defining Copilot features for live chat conversations. |
| ticket_setting | mediumtext | Yes | NULL | JSON configuration defining Copilot features for ticket conversations. |
| created | bigint(20) | Yes | NULL | Timestamp indicating when the settings record was created (Unix epoch). |
| updated | bigint(20) | Yes | NULL | Timestamp indicating the last update time of the settings record. |

---

# JSON Configuration Structure

## 1. Access Setting

Controls **which agents can use Copilot and which knowledge bases are accessible**.

### Sample Data
```json
{
  "isAllAgent": true,
  "allowedAgentIds": [8565705],
  "kbAccess": [
    {
      "deptId": -1,
      "kbIds": [717, 823]
    }
  ]
}
```

### Field Description

| Field | Type | Description |
|------|------|-------------|
| isAllAgent | boolean | Indicates whether Copilot is accessible to all agents in the account. |
| allowedAgentIds | array | List of agent IDs allowed to use Copilot when `isAllAgent` is false. |
| kbAccess | array | Defines which knowledge bases Copilot can access. |
| deptId | number | Department ID associated with the knowledge base access. |
| kbIds | array | List of knowledge base IDs accessible for Copilot responses. |

---

## 2. Live Chat Setting

Controls **AI assistance features during live chat conversations**.

### Sample Data
```json
{
  "chatSummaryAfterChatClose": true,
  "chatSummaryOnChatTransfer": true,
  "replySuggestion": true,
  "translation": true,
  "smartRewrite": true,
  "sentiment": {
    "status": true,
    "sentimentData": {
      "disappointed": {"type":"DISAPPOINTED","min":0,"max":25},
      "neutral": {"type":"NEUTRAL","min":16,"max":50},
      "good": {"type":"GOOD","min":51,"max":75},
      "satisfied": {"type":"SATISFIED","min":76,"max":100}
    }
  }
}
```

### Field Description

| Field | Type | Description |
|------|------|-------------|
| chatSummaryAfterChatClose | boolean | Enables automatic chat summary generation after a chat session ends. |
| chatSummaryOnChatTransfer | boolean | Generates chat summary when the conversation is transferred to another agent. |
| replySuggestion | boolean | Enables AI-powered reply suggestions for agents. |
| translation | boolean | Enables automatic message translation for multilingual conversations. |
| smartRewrite | boolean | Allows agents to rewrite responses using AI assistance. |
| sentiment.status | boolean | Enables sentiment analysis for chat messages. |
| sentiment.sentimentData | object | Defines sentiment score ranges used to categorize customer sentiment. |

### Sentiment Categories

| Sentiment | Score Range |
|----------|-------------|
| DISAPPOINTED | 0 – 25 |
| NEUTRAL | 16 – 50 |
| GOOD | 51 – 75 |
| SATISFIED | 76 – 100 |

---

## 3. Ticket Setting

Controls **AI assistance features during ticket-based support conversations**.

### Sample Data
```json
{
  "chatSummaryAfterChatClose": true,
  "chatSummaryOnChatTransfer": true,
  "replySuggestion": true,
  "translation": true,
  "smartRewrite": true,
  "sentiment": {
    "status": true,
    "sentimentData": {
      "disappointed": {"type":"DISAPPOINTED","min":0,"max":25},
      "neutral": {"type":"NEUTRAL","min":16,"max":50},
      "good": {"type":"GOOD","min":51,"max":75},
      "satisfied": {"type":"SATISFIED","min":76,"max":100}
    }
  }
}
```

### Features Enabled for Ticketing

- AI **reply suggestions for agents**
- AI **translation of ticket messages**
- AI **smart rewrite of responses**
- **Automatic ticket conversation summaries**
- **Customer sentiment analysis**

---

## Notes

- JSON structures allow flexible configuration without modifying the database schema.
- Copilot settings are stored **per account**, enabling customized AI assistance configurations.
- Sentiment scoring helps agents understand **customer mood and urgency** during conversations.

---

# copilot_conversation Table Documentation

## Overview
The `copilot_conversation` table stores session-level information for conversations between an **agent and the Copilot AI assistant**.

Each record represents a Copilot interaction session initiated by an agent. The table tracks which agent started the session, which account it belongs to, and the current status of the conversation. These sessions are used to manage the lifecycle of AI-assisted interactions.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| ID | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each Copilot conversation session. |
| accountId | varchar(20) | Yes | NULL | Identifier of the account associated with the Copilot conversation. |
| agentId | bigint(20) | No | — | Identifier of the agent who initiated the Copilot conversation. |
| status | varchar(50) | No | — | Current status of the Copilot conversation session. |
| created | bigint(20) | Yes | NULL | Timestamp indicating when the conversation session was created (Unix epoch). |
| updated | bigint(20) | Yes | NULL | Timestamp indicating the last update time of the conversation session. |

---

## Status Values

| Status | Description |
|------|-------------|
| RUNNING | The Copilot conversation session is currently active. |
| ENDED | The Copilot conversation session has been closed or completed. |

---

## Notes

- Each record represents a **single Copilot session for an agent**.
- A session typically starts when an agent begins interacting with Copilot and ends when the session is closed.
- Conversation messages related to the session may be stored in a separate table linked to this conversation ID.

---

# copilot_message Table Documentation

## Overview
The `copilot_message` table stores individual messages exchanged during **Copilot AI interactions**.

Each record represents a message generated or processed within a Copilot-assisted session. Messages are typically associated with an agent and may also be linked to a specific chat or conversation context. This table helps track AI-generated suggestions, prompts, and agent inputs during Copilot usage.

The actual message payload is stored in the **`msg` column in JSON format**, which contains metadata about the request, the AI model used, the query, and conversation identifiers.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| id | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each Copilot message record. |
| accountId | varchar(20) | Yes | NULL | Identifier of the account associated with the Copilot interaction. |
| agentId | bigint(20) | Yes | NULL | Identifier of the agent involved in the Copilot interaction. |
| chatId | bigint(20) | Yes | NULL | Identifier of the chat session associated with the Copilot message. |
| messageId | varchar(190) | Yes | NULL | Unique identifier for the message used for tracking or correlation. |
| msg | mediumtext | Yes | NULL | JSON payload containing the Copilot request or message data. |
| created | bigint(20) | Yes | NULL | Timestamp indicating when the message was created (Unix epoch). |
| updated | bigint(20) | Yes | NULL | Timestamp indicating the last update time of the message. |

---

# JSON Structure of `msg`

The `msg` column stores a **JSON object containing the Copilot request metadata and user query**.

## Sample Data

```json
{
  "ftype": 0,
  "ttype": 1,
  "account": "3319570",
  "body": {
    "llm_model": "llama-2-7b-chat",
    "account_id": "3319570",
    "question": "tell me about the post paid plans",
    "user_id": "gold31.rabby@gmail.com",
    "kb_ids": "493",
    "bot_id": "9663"
  },
  "messageId": "c51c44da-065a-4f54-925f-d14a762c0f85",
  "agentId": "gold31.rabby@gmail.com",
  "timestamp": 1754797646429,
  "chatId": 1
}
```

---

## JSON Field Description

| Field | Type | Description |
|------|------|-------------|
| ftype | number | Message format type identifier used internally by the system. |
| ttype | number | Target or message type used by the Copilot messaging system. |
| account | string | Identifier of the account associated with the request. |
| body | object | Main request payload containing AI query details. |
| body.llm_model | string | Name of the large language model used to process the request. |
| body.account_id | string | Account identifier for the request. |
| body.question | string | The question or prompt sent to the Copilot AI. |
| body.user_id | string | Identifier of the user or agent making the request. |
| body.kb_ids | string | Knowledge base IDs used to retrieve context for answering the query. |
| body.bot_id | string | Identifier of the chatbot associated with the request. |
| messageId | string | Unique identifier for the message instance. |
| agentId | string | Identifier of the agent sending the query to Copilot. |
| timestamp | number | Timestamp when the message request was created (Unix epoch in milliseconds). |
| chatId | number | Identifier of the chat session associated with the Copilot request. |

---

## Notes

- The `msg` column stores **dynamic AI request data**, which allows flexible integration with different AI models and services.
- The **`body` object** contains the main AI query parameters.
- `kb_ids` indicates the **knowledge bases used for retrieval-augmented generation (RAG)** when answering the query.
- The system may store both **agent prompts and AI-generated responses** in this table.

---

# widgetattribute Table Documentation

## Overview
The `widgetattribute` table stores configuration settings and UI customization options for the **live chat widget** used on websites.

Each record represents a widget configuration associated with a specific account. The table controls the widget’s appearance, behavior, forms, surveys, banners, social icons, office hours, and other customization settings used in the chat interface.

Many fields store **JSON or serialized configuration data**, allowing flexible customization of widget behavior without requiring schema changes.

---

## Table Structure

| Column Name | Data Type | Nullable | Default | Description |
|------------|-----------|----------|---------|-------------|
| ID | bigint(20) | No | Auto Increment | Primary key. Unique identifier for each widget configuration. |
| account_id | varchar(20) | Yes | NULL | Identifier of the account associated with the widget configuration. |
| attr_invitation_banner_online | text | Yes | NULL | Configuration for the invitation banner shown when agents are online. |
| attr_invitation_banner_offline | text | Yes | NULL | Configuration for the invitation banner shown when agents are offline. |
| attr_chat_window | text | Yes | NULL | Settings related to the chat window interface. |
| attr_post_survey_form | mediumtext | Yes | NULL | Configuration for the post-chat survey form displayed after conversations end. |
| attr_theme_color | varchar(20) | Yes | '#0058BF' | Primary theme color used in the chat widget UI. |
| attr_greetings_form | varchar(2048) | No | Default JSON | Configuration for the greeting form displayed when the widget is opened. |
| attr_social_icon_twitter | char(1) | Yes | '1' | Indicates whether the Twitter social icon is enabled in the widget. |
| attr_social_icon_facebook | char(1) | Yes | '1' | Indicates whether the Facebook social icon is enabled in the widget. |
| attr_banner_position | char(1) | Yes | '2' | Position of the widget banner on the webpage. |
| attr_window_size | char(1) | Yes | '2' | Defines the size of the chat window. |
| attr_eyecatcher_image_gallery | varchar(50) | Yes | NULL | Identifier of the eyecatcher image used for the widget launcher. |
| general_settings | varchar(1024) | Yes | NULL | General configuration settings for the widget. |
| urlId | varchar(100) | No | '-1' | Identifier associated with a specific website or URL configuration. |
| attr_theme_name | varchar(100) | Yes | 'modern-theme' | Name of the UI theme used for the widget. |
| mobile_trigger | varchar(8) | Yes | NULL | Defines how the widget trigger behaves on mobile devices. |
| attr_record_info | varchar(255) | Yes | NULL | Stores metadata related to widget records or configuration. |
| attr_office_hours | longtext | Yes | NULL | Configuration defining office hours and agent availability. |
| attr_widget_lang | varchar(10) | Yes | 'en' | Default language used by the widget interface. |
| attr_text_color | varchar(100) | Yes | '#FFFFFF' | Text color used in widget UI elements. |
| is_white_label | tinyint(4) | Yes | 0 | Indicates whether white-label branding is enabled. |
| chat_button_shape | varchar(100) | Yes | 'circle' | Shape of the chat launch button (e.g., circle, square). |
| attr_launching_window_offline | mediumtext | Yes | NULL | Configuration for the widget launching window when agents are offline. |
| attr_launching_window_online | mediumtext | Yes | NULL | Configuration for the widget launching window when agents are online. |
| attr_missed_chat | mediumtext | Yes | NULL | Settings related to missed chat notifications. |
| attr_queued_offline | mediumtext | Yes | NULL | Configuration for queued chats when agents are offline. |
| attr_widget_home | text | Yes | NULL | Configuration for the widget home interface. |
| widgetuuid | varchar(50) | Yes | 'default' | Unique identifier for the widget instance. |
| attr_forms | text | Yes | NULL | Configuration data for forms used within the widget. |
| web_push_settings | text | Yes | NULL | Settings related to web push notifications for the widget. |

---

## Indexes

| Index Name | Columns | Type | Description |
|-----------|--------|------|-------------|
| PRIMARY | (ID) | BTREE | Primary key ensuring unique identification of each widget configuration. |
| account_id | (account_id) | BTREE | Optimizes queries retrieving widget configurations by account. |

---

## Notes

- Many configuration fields store **JSON or serialized UI settings**.
- The table centralizes **all widget customization and behavior settings**.
- Supports configuration for:
  - Widget UI themes
  - Greeting forms
  - Chat invitation banners
  - Post-chat surveys
  - Social media icons
  - Office hours and availability
  - Mobile widget behavior
  - Push notification settings
- Each account can have **multiple widget configurations** depending on different websites or widget instances.

---


# vbsession Table Documentation

## Overview
The `vbsession` table stores **agent session activity records** for an account.  
Each record represents a **login session of a user (typically an agent)** within the system.

The table tracks **when a user starts and ends a session**, the **account they belong to**, and any **reason associated with the session event** (such as logout reason, disconnection, etc.).

This table is commonly used for:

- Agent availability tracking
- Session duration analysis
- Workforce activity monitoring
- Operational reporting

---

## Table Information

| Property | Value |
|--------|------|
| Engine | InnoDB |
| Charset | utf8mb4 |
| Collation | utf8mb4_unicode_ci |
| Primary Key | `ID` |
| Auto Increment | Yes |

---

## Column Definitions

| Column | Type | Nullable | Description |
|------|------|------|-------------|
| `ID` | bigint(20) | No | Unique identifier for each session record |
| `userID` | bigint(20) | No | Unique identifier of the user (agent) |
| `userType` | smallint(6) | Yes | Type of user (e.g., agent, admin, etc.) |
| `vbAccount` | varchar(20) | Yes | Account identifier associated with the session |
| `start_session` | decimal(18,0) | Yes | Session start timestamp (epoch format) |
| `end_session` | decimal(18,0) | Yes | Session end timestamp (epoch format) |
| `reason` | text | Yes | Optional description of the session termination reason |

---

## Timestamp Fields

Both `start_session` and `end_session` are stored as **epoch timestamps** in decimal format.

Example conversion in SQL:

```sql
SELECT
    DATE(FROM_UNIXTIME(start_session/1000)) AS login_date,
    COUNT(*) AS total_logins,
    COUNT(DISTINCT userID) AS unique_users_logged_in
FROM vbsession
WHERE vbAccount = 'YOUR_ACCOUNT_ID'
GROUP BY DATE(FROM_UNIXTIME(start_session/1000))
ORDER BY DATE(FROM_UNIXTIME(start_session/1000));
