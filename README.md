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
