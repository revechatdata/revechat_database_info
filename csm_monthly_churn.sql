select * from (
select subscription_id , account_id as operator_code, package_type ,agent_count , start_date , end_date , subscription_duration as date_diff
,mrr 
from silver.billing_subscription_fact bs
where bs.subscription_id = bs.last_subscription_id 
and end_month = '2025-09'
and subscription_status = 'System-Payment'
) as tbl 
left join (
select v.usaccount , v.usrmailaddr  from vbuser v where v.usroleid =1
) as tbl2 on tbl.operator_code = tbl2.usaccount
