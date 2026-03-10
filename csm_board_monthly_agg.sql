drop table silver.account_wise_emails;
create table silver.account_wise_emails as
select id as user_id, usaccount , usrmailaddr 
from vbuser v 
where usroleid =1;




select distinct sf.account_id from silver.billing_subscription_fact sf where sf.subscription_id= last_subscription_id and end_date>=current_date

drop table account_wise_chatrequest_3months;
create table account_wise_chatrequest_3months as 
select c.account_id as vbaccount , 
count(case when c.date_id>= '2025-07-01' and c.date_id< '2025-08-01' then 1 end) as jul,
count(case when c.date_id>= '2025-08-01' and c.date_id< '2025-09-01' then 1 end) as aug,
count(case when c.date_id>= '2025-09-01' and c.date_id< '2025-10-01' then 1 end) as sep
from silver.chatfact c 
where c.account_id::varchar(20) in ( select distinct sf.account_id 
from silver.billing_subscription_fact sf 
where sf.subscription_id= last_subscription_id and end_date>=current_date)
group by 1;



select * from silver.chatfact c 
where c.frt_breach 



select * from account_wise_frt_breach_3months;

drop table account_wise_frt_breach_3months;
create table account_wise_frt_breach_3months as 
select c.account_id as vbaccount , 
count(case when c.date_id>= '2025-07-01' and c.date_id< '2025-08-01' then 1 end) as jul,
count(case when c.date_id>= '2025-08-01' and c.date_id< '2025-09-01' then 1 end) as aug,
count(case when c.date_id>= '2025-09-01' and c.date_id< '2025-10-01' then 1 end) as sep
from silver.chatfact c 
where c.frt_breach =1
and c.account_id::varchar(20) in ( select distinct sf.account_id 
from silver.billing_subscription_fact sf 
where sf.subscription_id= last_subscription_id and end_date>=current_date)
group by 1;


select * from account_wise_ert_breach_3months;

drop table account_wise_ert_breach_3months;
create table account_wise_ert_breach_3months as 
select c.account_id as vbaccount , 
count(case when c.date_id>= '2025-07-01' and c.date_id< '2025-08-01' then 1 end) as jul,
count(case when c.date_id>= '2025-08-01' and c.date_id< '2025-09-01' then 1 end) as aug,
count(case when c.date_id>= '2025-09-01' and c.date_id< '2025-10-01' then 1 end) as sep
from silver.chatfact c 
where c.ert_breach =1
and c.account_id::varchar(20) in ( select distinct sf.account_id 
from silver.billing_subscription_fact sf 
where sf.subscription_id= last_subscription_id and end_date>=current_date)
group by 1;
