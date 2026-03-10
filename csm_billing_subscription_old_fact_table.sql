create table silver.billing_subscription_fact as 
select bs.id as subscription_id ,operator_code as account_id,
bp."name" as package_type
,agent_count,tmp_agent_count,
substring(to_timestamp(start_date/1000)::text,1,4) as start_year,
date(to_timestamp(start_date/1000)) as start_date,
substring(to_timestamp(start_date/1000)::text,1,7) as start_month,
substring(to_timestamp(end_date/1000)::text,1,4) as end_year,
date(to_timestamp(end_date/1000)) as end_date,
substring(to_timestamp(end_date/1000)::text,1,7) as end_month,
date(to_timestamp(end_date/1000))-date(to_timestamp(start_date/1000)) as subscription_duration,
case when status =1 then 'System-Payment' 
     when status =2 then 'Demo-Account'
     when (date(to_timestamp(end_date/1000))-date(to_timestamp(start_date/1000)))>14  and 
     status=2 then 'Demo-Extended'
     else 'Undefined' end as subscription_status,
status,created,tmp_balance,
tmp_start_date,tmp_end_date,balance,creator_id,
case when month_count =1 then 'Monthly'
     when month_count =12 then 'Yearly'
     when month_count =24 then '2-Yearly'
     else 'Undefined' end  as package_duration,
tmp_month_count,discount,tmp_discount,migration_status,used_coupon_id, 
case when addons_price>0 then 'Chatbot' else 'No-Chatbot' end as addons_status,
addons_price,customer_id,
case 
    when month_count = 1 then round((bp.monthly_rate_per_agent*agent_count)+addons_price-tmp_discount,2)::float
    when month_count = 12 then round((bp.monthly_rate_per_agent::numeric * agent_count::numeric)+(addons_price / 12)-(tmp_discount/12),2)
    when month_count = 24 then round((bp.monthly_rate_per_agent*agent_count)+(addons_price/24)-(tmp_discount/24),2)::float
end as mrr,
max(bs.id) over(partition by operator_code) as last_subscription_id,
agent_count-lag(agent_count,1) over(partition by operator_code order by bs.id asc) as agent_difference,
null::varchar(15) as rfm, 
0::smallint as is_internal
from billing_subscription bs 
inner join billing_package bp on bs.package_code = bp.code
;
