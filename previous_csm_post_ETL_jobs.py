import mysql.connector
from mysql.connector import Error
import pandas as pd
import sqlalchemy
import numpy as np
import json
from datetime import date



today = date.today()







try:
    connection_dwh = mysql.connector.connect(host='170...139',
                                         database='analytics',
                                         user='create_user_test',
                                         password='',
                                             port=3856)
    if connection_dwh.is_connected():
        db_Info = connection_dwh.get_server_info()
        print("Connected to MySQL(RC-DWH) Server version ", db_Info)
        dwh_cursor = connection_dwh.cursor()
        database_username = 'create_user_test'
        database_password = '$#'
        database_ip = '170..139'
        database_name = 'analytics'
        database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                                       format(database_username, database_password,
                                                              database_ip, database_name))
except Error as e:
    print("Error while connecting to MySQL(RC-DWH)", e)


report_date  = str(date.today())




dwh_cursor = connection_dwh.cursor()





csm= '''
drop table if exists analytics.first_commercial_date;
'''

print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm= '''
create table analytics.first_commercial_date as 
select bs2.operator_code , date(from_unixtime(start_date/1000)) as convertdate 
from (
select operator_code, min(id) as minid
from analytics.billing_subscription bs 
where 1=1
and status =1
group by 1
) as tbl 
inner join analytics.billing_subscription bs2 on bs2.id = tbl.minid 
;
'''


print(csm)


dwh_cursor.execute(csm)

connection_dwh.commit()











csm= '''
drop table if exists analytics.dashboard_csm_last_30d_offchat_counts;
'''

print(csm)



dwh_cursor.execute(csm)

connection_dwh.commit()


csm='''
create table analytics.dashboard_csm_last_30d_offchat_counts as 
select v.vbAccount as acc , count(1) as offline_msg 
from analytics.vbofflinemessage v 
where 1=1
and from_unixtime(v.vbReceivedTime/1000)>= current_date() -interval 30 day 
group by 1;
'''


print(csm)


dwh_cursor.execute(csm)

connection_dwh.commit()





csm= '''
drop table if exists analytics.dashboard_csm_last_30d_chats_and_missed_chat_pct;
'''

print(csm)


dwh_cursor.execute(csm)

connection_dwh.commit()









csm= '''
drop table if exists analytics.clients_lifetime_value;
'''

dwh_cursor.execute(csm)

connection_dwh.commit()


csm='''

create table analytics.clients_lifetime_value as 
select operator_code as optr_code , coalesce(sum(amount),0) as cltv 
from analytics.billing_transaction bt 
where 1=1
and bt.vendor not like '%down%'
and bt.payment_id is not null 
and length(bt.payment_id)>0
group by 1;

'''

print(csm)


dwh_cursor.execute(csm)

connection_dwh.commit()












csm= '''
drop table if exists analytics.clients_website_traffic_in_30d;
'''

print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm='''

create table analytics.clients_website_traffic_in_30d as 
select vbAccount , floor(avg(unique_visitors)) as unique_visitors
from analytics.vbvisitoranalytics v 
where 1=1
and from_unixtime(vbdate/1000)>= current_date() - interval 30 day 
group by 1;

'''

print(csm)


dwh_cursor.execute(csm)

connection_dwh.commit()





csm= '''
drop table if exists analytics.bot_conversations_count_by_accounts;
'''

dwh_cursor.execute(csm)

connection_dwh.commit()


csm='''
create table analytics.bot_conversations_count_by_accounts as 
select account , count(id) as bc 
from analytics.bot_conversations bc 
where 1=1
and from_unixtime(bc.`timestamp`/1000)>= current_date() - interval 30 day
group by 1;

'''

print(csm)


dwh_cursor.execute(csm)

connection_dwh.commit()



csm= '''
drop table if exists analytics.dashboard_csm_last_30d_chat_counts;
'''

dwh_cursor.execute(csm)

connection_dwh.commit()


csm='''
create table analytics.dashboard_csm_last_30d_chat_counts as 
select v.vbAccount , count(1) as cnt 
from analytics.vbmissedchats v 
where 1=1
and from_unixtime(v.chatRequestTime/1000)>= current_date() - interval 30 day
group by 1;

'''

print(csm)


dwh_cursor.execute(csm)

connection_dwh.commit()



csm= '''
drop table if exists analytics.dashboard_csm_last_30d_chats_and_missed_chat_pct;
'''

dwh_cursor.execute(csm)

connection_dwh.commit()


csm='''

create table analytics.dashboard_csm_last_30d_chats_and_missed_chat_pct as 
select vbAccount , count(case when isMissed=1 then 1 end) as missed_chat , count(1) as total_chat, round(coalesce(count(case when isMissed=1 then 1 end)/count(1),0),2)*100 as missed_chat_pct
from analytics.vbmissedchats v 
where 1=1
and from_unixtime(v.chatRequestTime/1000)>= current_date() - interval 30 day
group by 1;

'''

dwh_cursor.execute(csm)

connection_dwh.commit()



csm = '''
drop table if exists analytics.current_customer_base ;
'''

dwh_cursor.execute(csm)

connection_dwh.commit()



csm = '''
create table analytics.current_customer_base as 
select bs2.operator_code , bs2.agent_count , bs2.package_code ,bs2.addons_price ,bs2.tmp_discount as discount ,
date(from_unixtime(bs2.end_date/1000)) as end_date , bs2.id as latest_subs_id
from (
select operator_code , max(id) as mxid 
from analytics.billing_subscription bs 
where 1=1
and status =1
group by 1
) as tbl 
inner join analytics.billing_subscription bs2 on bs2.id = tbl.mxid 
where 1=1
and from_unixtime(bs2.end_date/1000)>= current_date() 
;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()





csm = '''
drop table if exists analytics.dashboard_clients_last_followup;
'''

dwh_cursor.execute(csm)

connection_dwh.commit()


csm ='''
create table analytics.dashboard_clients_last_followup as 
select bsc.followupId as account_id, bsc.`date` as last_followup, bsc.comments 
from (
select  followupId ,max(id) as mxid 
from analytics.backend_sales_comments bsc 
group by 1
) as tbl 
inner join analytics.backend_sales_comments bsc on bsc.id = tbl.mxid 
;
'''
print(csm)



dwh_cursor.execute(csm)

connection_dwh.commit()

















csm = '''
drop table if exists analytics.avoid_internal_account_ids;
'''

dwh_cursor.execute(csm)

connection_dwh.commit()


csm ='''
create table analytics.avoid_internal_account_ids as 
select distinct cd.usAccount from analytics.avoid_internal_mails as im 
inner join analytics.vbuser as cd on cd.usrMailAddr = im.mailaddr;

'''

print(csm)


dwh_cursor.execute(csm)

connection_dwh.commit()










csm = '''
drop table if exists analytics.users_superadmin_creation_date;
'''

dwh_cursor.execute(csm)

connection_dwh.commit()


csm ='''
create table analytics.users_superadmin_creation_date as 
select v2.usAccount , v2.usrMailAddr , date(v2.usAccCreateTime) as registration_date, 
coalesce(concat(usFirstName, ' ', usLastName),'') as full_name  from (
select usAccount , min(usAccCreateTime) as usAccCreateTime from analytics.vbuser v 
group by 1
) as tbl 
inner join analytics.vbuser v2 on v2.usAccount = tbl.usAccount and v2.usAccCreateTime = tbl.usAccCreateTime
;
'''

print(csm)


dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
            drop table if exists analytics.dashboard_csm_lost_customer_login_info;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()







csm = ''' 
create table analytics.dashboard_csm_lost_customer_login_info as
select operator_code , package_code , agent_count , date(from_unixtime(end_date/1000)) as expired_on, v.id as session_id,
date(from_unixtime(v.start_session/1000)) as after_expired_login_date, current_date() as report_date from (
select bs2.* from (
select operator_code, max(id) as mx_subs_id from analytics.billing_subscription bs 
where 1=1
and bs.status =1
group by 1) as tmp
inner join analytics.billing_subscription bs2 on bs2.id = tmp.mx_subs_id
where 1=1
and from_unixtime(end_date/1000) <= current_date() ) as tbl
inner join analytics.vbsession v on v.vbAccount = tbl.operator_code
where 1=1
and tbl.end_date < v.start_session;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()



dwh_cursor = connection_dwh.cursor()
csm = ''' 
            drop table if exists analytics.dashboard_csm_chat_type;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()

dwh_cursor = connection_dwh.cursor()
csm = ''' 
create table analytics.dashboard_csm_chat_type as 
select tmp.operator_code, v.chatRequestTime as msg_time, v.id , case when v.isMissed =1 then 'Missed Message' else 'Served Message' end as chat_type
from (
select distinct operator_code from analytics.current_customer_base
) as tmp
inner join analytics.vbmissedchats v on v.vbAccount = tmp.operator_code
where 1=1
and date(from_unixtime(v.chatRequestTime/1000)) >= current_date() - interval 30 day 
and date(from_unixtime(v.chatRequestTime/1000)) < current_date()
;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
            alter table analytics.dashboard_csm_chat_type modify column chat_type varchar(100);
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
           insert into analytics.dashboard_csm_chat_type
select tmp.operator_code, v.vbReceivedTime as msg_time , v.id , 'Offline Message' as chat_type
from (
select distinct operator_code from analytics.current_customer_base
) as tmp
inner join analytics.vbofflinemessage v on v.vbAccount = tmp.operator_code
where 1=1
and date(from_unixtime(v.vbReceivedTime/1000)) >= current_date() - interval 30 day 
and date(from_unixtime(v.vbReceivedTime/1000)) < current_date();
	
	
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()



csm = '''
delete from analytics.dashboard_csm_chat_type where 1=1
and operator_code in (select usAccount from analytics.avoid_internal_account_ids )
;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
            drop table if exists analytics.dashboard_csm_subscription_ended;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
create table analytics.dashboard_csm_subscription_ended as 
select bs2.operator_code ,
bp.name as package,
bs2.agent_count as Licence ,
case when bs2.month_count=1 then 'M'
	when bs2.month_count=12 then 'Y'
	when bs2.month_count =24 then '2Y' end as model,
	upper(bs2.billing_currency) as  currency,
	bp.monthly_rate_per_agent as agent_rate,
	bp.monthly_rate_per_agent*bs2.agent_count as total_agent_cost,
	bs2.addons_price ,
	bs2.discount,
case when bs2.month_count = 1 then round((bp.monthly_rate_per_agent*bs2.agent_count)+bs2.addons_price-bs2.tmp_discount,2)
	 when bs2.month_count = 12 then round((bp.monthly_rate_per_agent*bs2.agent_count)+(bs2.addons_price/12)-(bs2.tmp_discount/12),2)
	 when bs2.month_count = 24 then round((bp.monthly_rate_per_agent*bs2.agent_count)+(bs2.addons_price/24)-(bs2.tmp_discount/24),2) end mrr,
date(from_unixtime(bs2.end_date/1000)) as subscription_end,
datediff(date(from_unixtime(bs2.end_date/1000)),current_date()) as expired_within,
current_date() as report_date 
from (
select operator_code , max(id) as mx_subs_id
from analytics.billing_subscription bs 
where 1=1
and status =1
group by 1
) as tbl 
inner join analytics.billing_subscription bs2 on bs2.id = tbl.mx_subs_id
inner join analytics.billing_package bp on bp.code = bs2.package_code
where 1=1
and from_unixtime(bs2.end_date/1000)>= current_date() ;


'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
            drop table if exists analytics.dashboard_customer_success_manager_user_wise_login_info;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()



csm = ''' 
create table analytics.dashboard_customer_success_manager_user_wise_login_info as 
select tbl.* from (
select v.usAccount as operator_code , case when usRoleID =1 then 'Super Admin' 
						  when usRoleID =2 then 'Admin'
						  when usRoleID =3 then 'Agent' end user_type,
	   v.usrMailAddr as email,
	   concat(usFirstName,' ', usLastName) as FullName ,
	   case when length(coalesce(v.usPhoneNo,'Not Available'))= 0 then 'Not Available' else coalesce(v.usPhoneNo,'Not Available') end as Phone,
	   datediff(current_date(),date(from_unixtime(v.usLastLoginTime/1000))) as LastLogin
from analytics.vbuser v 
where 1=1
and isActive =1
and usUserStatus =0) as tbl
inner join (
select distinct operator_code as account_id from analytics.current_customer_base
) as tbl1 on tbl1.account_id = tbl.operator_code;

'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()

csm = ''' 
            drop table analytics.dashboard_customer_success_manager_user_inactive_pct;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
            create table analytics.dashboard_customer_success_manager_user_inactive_pct as 
select bs2.operator_code , bp.name as package_using ,
bs2.agent_count as num_of_seats,coalesce(last_login.users_login_in_last7days,0) as users_login_in_last7days,
(bs2.agent_count-coalesce(last_login.users_login_in_last7days,0))/bs2.agent_count*100 as inactive_user_last_7days_pct, current_date() as report_date
from (
select operator_code , max(id) as mx_subs_id
from analytics.billing_subscription bs 
where 1=1
and status =1
group by 1
) as tbl 
inner join analytics.billing_subscription bs2 on bs2.id = tbl.mx_subs_id
inner join analytics.billing_package bp on bp.code = bs2.package_code 
left join (
select usAccount ,count(distinct id) as users_login_in_last7days from analytics.vbuser v
where 1=1
and v.isActive =1
and v.usUserStatus = 0
and from_unixtime(usLastLoginTime/1000)>= current_date() - interval 7 day
group by 1
) as last_login on last_login.usAccount = bs2.operator_code 
where 1=1
and from_unixtime(bs2.end_date/1000)>= current_date() 
order by 5 desc;
	
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
            drop table if exists analytics.dashboard_customer_success_manager_chat_downward;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
           
create table analytics.dashboard_customer_success_manager_chat_downward as 
select *, current_date as report_date from (
select tbl90.operator_code, tbl90.active_day_in_90days as active_chatday_in_90days,tbl90.avg_chat_per_active_day_in_90days as avg_chat_per_chatactive_day_in_90days,
coalesce(tbl15.active_day_in_15days,0) as active_chatday_in_15days ,
coalesce(tbl15.avg_chat_per_active_day_in_15days,0) as avg_chat_per_chat_active_day_in_15days,
coalesce(tbl30.active_day_in_30days,0) as active_chatday_in_30days ,
coalesce(tbl30.avg_chat_per_active_day_in_30days,0) as avg_chat_per_chat_active_day_in_30days,
coalesce(round(((coalesce(tbl90.avg_chat_per_active_day_in_90days,0)-coalesce(tbl15.avg_chat_per_active_day_in_15days,0))/coalesce(tbl90.avg_chat_per_active_day_in_90days,0))*100,2),100) as avg_chat_in15days_reduced_percentage,
coalesce(round(((coalesce(tbl90.avg_chat_per_active_day_in_90days,0)-coalesce(tbl30.avg_chat_per_active_day_in_30days,0))/coalesce(tbl90.avg_chat_per_active_day_in_90days,0))*100,2),100) as avg_chat_in30days_reduced_percentage
from (
select operator_code , count(distinct active_day) as active_day_in_90days, 
coalesce(round(sum(chatreq)/ count(distinct active_day),0),0) as avg_chat_per_active_day_in_90days
from (
select operator_code , date(from_unixtime(v.chatRequestTime/1000)) as active_day ,count(v.id) as chatreq from (
select distinct operator_code as operator_code from analytics.current_customer_base) as tmp
left join analytics.vbmissedchats v on v.vbAccount = tmp.operator_code and from_unixtime(v.chatRequestTime/1000) >= curdate()-interval 90 day and from_unixtime(v.chatRequestTime/1000) < curdate()
where 1=1
group by 1,2) as tbl2
group by 1
) as tbl90
left join (
select operator_code , count(distinct active_day) as active_day_in_15days, 
coalesce(round(sum(chatreq)/ count(distinct active_day),0),0) as avg_chat_per_active_day_in_15days
from (
select operator_code , date(from_unixtime(v.chatRequestTime/1000)) as active_day ,count(v.id) as chatreq from (
select distinct operator_code as operator_code from analytics.current_customer_base) as tmp
left join analytics.vbmissedchats v on v.vbAccount = tmp.operator_code and from_unixtime(v.chatRequestTime/1000) >= curdate()-interval 15 day and from_unixtime(v.chatRequestTime/1000) < curdate()
where 1=1
group by 1,2) as tbl2
group by 1) as tbl15 on tbl90.operator_code = tbl15.operator_code
left join (
select operator_code , count(distinct active_day) as active_day_in_30days, 
coalesce(round(sum(chatreq)/ count(distinct active_day),0),0) as avg_chat_per_active_day_in_30days
from (
select operator_code , date(from_unixtime(v.chatRequestTime/1000)) as active_day ,count(v.id) as chatreq from (
select distinct operator_code as operator_code from analytics.current_customer_base) as tmp
left join analytics.vbmissedchats v on v.vbAccount = tmp.operator_code and from_unixtime(v.chatRequestTime/1000) >= curdate()-interval 30 day and from_unixtime(v.chatRequestTime/1000) < curdate()
where 1=1
group by 1,2) as tbl2
group by 1) as tbl30 on tbl90.operator_code = tbl30.operator_code
) as final_table
where 1=1
and (avg_chat_in15days_reduced_percentage > 0 or avg_chat_in30days_reduced_percentage > 0)
order by avg_chat_in15days_reduced_percentage desc, avg_chat_per_chatactive_day_in_90days desc, active_chatday_in_90days desc;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
            drop table if exists analytics.dashboard_customer_success_manager_chat_upward;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()

csm = ''' 
           create table analytics.dashboard_customer_success_manager_chat_upward as 
select *, current_date as report_date from (
select tbl90.operator_code, tbl90.active_day_in_90days as active_chatday_in_90days,tbl90.avg_chat_per_active_day_in_90days as avg_chat_per_chatactive_day_in_90days,
coalesce(tbl15.active_day_in_15days,0) as active_chatday_in_15days ,
coalesce(tbl15.avg_chat_per_active_day_in_15days,0) as avg_chat_per_chat_active_day_in_15days,
coalesce(tbl30.active_day_in_30days,0) as active_chatday_in_30days ,
coalesce(tbl30.avg_chat_per_active_day_in_30days,0) as avg_chat_per_chat_active_day_in_30days,
coalesce(round(((coalesce(tbl90.avg_chat_per_active_day_in_90days,0)-coalesce(tbl15.avg_chat_per_active_day_in_15days,0))/coalesce(tbl90.avg_chat_per_active_day_in_90days,0))*100,2),100) as avg_chat_in15days_reduced_percentage,
coalesce(round(((coalesce(tbl90.avg_chat_per_active_day_in_90days,0)-coalesce(tbl30.avg_chat_per_active_day_in_30days,0))/coalesce(tbl90.avg_chat_per_active_day_in_90days,0))*100,2),100) as avg_chat_in30days_reduced_percentage
from (
select operator_code , count(distinct active_day) as active_day_in_90days, 
coalesce(round(sum(chatreq)/ count(distinct active_day),0),0) as avg_chat_per_active_day_in_90days
from (
select operator_code , date(from_unixtime(v.chatRequestTime/1000)) as active_day ,count(v.id) as chatreq from (
select distinct operator_code as operator_code from analytics.current_customer_base) as tmp
left join analytics.vbmissedchats v on v.vbAccount = tmp.operator_code and from_unixtime(v.chatRequestTime/1000) >= curdate()-interval 90 day and from_unixtime(v.chatRequestTime/1000) < curdate()
where 1=1
group by 1,2) as tbl2
group by 1
) as tbl90
left join (
select operator_code , count(distinct active_day) as active_day_in_15days, 
coalesce(round(sum(chatreq)/ count(distinct active_day),0),0) as avg_chat_per_active_day_in_15days
from (
select operator_code , date(from_unixtime(v.chatRequestTime/1000)) as active_day ,count(v.id) as chatreq from (
select distinct operator_code as operator_code from analytics.current_customer_base) as tmp
left join analytics.vbmissedchats v on v.vbAccount = tmp.operator_code and from_unixtime(v.chatRequestTime/1000) >= curdate()-interval 15 day and from_unixtime(v.chatRequestTime/1000) < curdate()
where 1=1
group by 1,2) as tbl2
group by 1) as tbl15 on tbl90.operator_code = tbl15.operator_code
left join (
select operator_code , count(distinct active_day) as active_day_in_30days, 
coalesce(round(sum(chatreq)/ count(distinct active_day),0),0) as avg_chat_per_active_day_in_30days
from (
select operator_code , date(from_unixtime(v.chatRequestTime/1000)) as active_day ,count(v.id) as chatreq from (
select distinct operator_code as operator_code from analytics.current_customer_base) as tmp
left join analytics.vbmissedchats v on v.vbAccount = tmp.operator_code and from_unixtime(v.chatRequestTime/1000) >= curdate()-interval 30 day and from_unixtime(v.chatRequestTime/1000) < curdate()
where 1=1
group by 1,2) as tbl2
group by 1) as tbl30 on tbl90.operator_code = tbl30.operator_code
) as final_table
where 1=1
and (avg_chat_in15days_reduced_percentage <= 0 or avg_chat_in30days_reduced_percentage <= 0)
order by avg_chat_in15days_reduced_percentage desc, avg_chat_per_chatactive_day_in_90days desc, active_chatday_in_90days desc;

'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
            drop table analytics.customers_on_the_way_of_churn;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()



csm = ''' 
            create table analytics.customers_on_the_way_of_churn as 
            select tmp1.operator_code, tmp1.user_type, tmp1.email, tmp1.fullname, tmp1.phone, tmp1.lastlogin, current_date() as report_date
            from (
            select tmp.operator_code from analytics.dashboard_customer_success_manager_user_inactive_pct as tmp
            left join analytics.dashboard_customer_success_manager_chat_downward as cd on tmp.operator_code = cd.operator_code
            where 1=1
            and tmp.inactive_user_last_7days_pct >=75
            and (cd.avg_chat_in15days_reduced_percentage >= 75 or cd.avg_chat_in15days_reduced_percentage is null)
            ) as tbl 
            inner join analytics.dashboard_customer_success_manager_user_wise_login_info as tmp1 on tmp1.operator_code = tbl.operator_code;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
            drop table if exists analytics.customers_logged_in_last15d;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()

csm = ''' 
           create table analytics.customers_logged_in_last15d as 
           select distinct operator_code from analytics.customers_on_the_way_of_churn co
           where 1=1
           and lastlogin <= 15
           ;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = ''' 
            delete from analytics.customers_on_the_way_of_churn where operator_code in(
            select operator_code from analytics.customers_logged_in_last15d
            );
'''


print(csm)

dwh_cursor.execute(csm)



csm = ''' 
            drop table if exists analytics.customers_on_the_way_of_churn_can_be_recurring;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()

csm = ''' 
            create table analytics.customers_on_the_way_of_churn_can_be_recurring as 
select grp_tbl.operator_code,grp_tbl.msg_received,(grp_tbl.msg_received/sum_tbl.total_message)*100 as weight_avg , current_date() as report_date from (
select 1 as join_key, ct.operator_code, count(distinct id) as msg_received from 
(
select distinct operator_code 
from analytics.customers_on_the_way_of_churn) as tmp 
inner join analytics.dashboard_csm_chat_type as ct on ct.operator_code = tmp.operator_code and ct.chat_type like '%offline%'
group by 1,2
) as grp_tbl 
inner join 
(
select 1 as join_key, count(distinct id) as total_message from 
(
select distinct operator_code 
from analytics.customers_on_the_way_of_churn) as tmp 
inner join analytics.dashboard_csm_chat_type as ct on ct.operator_code = tmp.operator_code and ct.chat_type like '%offline%'
) as sum_tbl on grp_tbl.join_key = sum_tbl.join_key
;
'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()



csm = '''
drop table if exists analytics.recent_churn_list;
'''

print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()




csm = '''
create table analytics.recent_churn_list as 
select tbl1.*,cd.usrMailAddr as mail , cd.registration_date, lf.last_followup , lf.comments from (
select bs2.operator_code ,bp.name ,bs2.month_count ,bs2.agent_count , bs2.addons_price, bs2.tmp_discount ,
case when bs2.month_count = 1 then round((bp.monthly_rate_per_agent*bs2.agent_count)+bs2.addons_price-bs2.tmp_discount,2)
	 when bs2.month_count = 12 then round((bp.monthly_rate_per_agent*bs2.agent_count)+(bs2.addons_price/12)-(bs2.tmp_discount/12),2)
	 when bs2.month_count = 24 then round((bp.monthly_rate_per_agent*bs2.agent_count)+(bs2.addons_price/24)-(bs2.tmp_discount/24),2) end mrr,
date(from_unixtime(bs2.end_date/1000)) as end_date, datediff(current_date(), date(from_unixtime(bs2.end_date/1000))) as lost_in_days 
from (
select operator_code , max(id) as mxid 
from analytics.billing_subscription bs 
where 1=1
and status =1
group by 1) as tbl 
inner join analytics.billing_subscription bs2 on bs2.id = tbl.mxid 
inner join analytics.billing_package bp on bp.code = bs2.package_code 
where 1=1
and from_unixtime(bs2.end_date/1000) < current_date()  
and from_unixtime(bs2.end_date/1000) >= current_date() - interval 30 day
) as tbl1 
inner join analytics.users_superadmin_creation_date as cd on cd.usAccount = tbl1.operator_code 
left join analytics.dashboard_clients_last_followup as lf on lf.account_id = tbl1.operator_code
;
'''

print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()





csm = '''
drop table analytics.dashboard_csm_subscription_ended_this_year;
'''

print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()




csm = '''
create table analytics.dashboard_csm_subscription_ended_this_year
select bs2.operator_code ,
bp.name as package,
bs2.agent_count as Licence ,
case when bs2.month_count=1 then 'M'
	when bs2.month_count=12 then 'Y'
	when bs2.month_count =24 then '2Y' end as model,
	upper(bs2.billing_currency) as  currency,
	bp.monthly_rate_per_agent as agent_rate,
	bp.monthly_rate_per_agent*bs2.agent_count as total_agent_cost,
	bs2.addons_price ,
	bs2.discount,
case when bs2.month_count = 1 then round((bp.monthly_rate_per_agent*bs2.agent_count)+bs2.addons_price-bs2.tmp_discount,2)
	 when bs2.month_count = 12 then round((bp.monthly_rate_per_agent*bs2.agent_count)+(bs2.addons_price/12)-(bs2.tmp_discount/12),2)
	 when bs2.month_count = 24 then round((bp.monthly_rate_per_agent*bs2.agent_count)+(bs2.addons_price/24)-(bs2.tmp_discount/24),2) end mrr,
date(from_unixtime(bs2.end_date/1000)) as subscription_end,
datediff(date(from_unixtime(bs2.end_date/1000)),current_date()) as expired_within,
current_date() as report_date 
from (
select operator_code , max(id) as mx_subs_id
from analytics.billing_subscription bs 
where 1=1
and status =1
group by 1
) as tbl 
inner join analytics.billing_subscription bs2 on bs2.id = tbl.mx_subs_id
inner join analytics.billing_package bp on bp.code = bs2.package_code
where 1=1
and from_unixtime(bs2.end_date/1000) < current_date() 
and year(from_unixtime(bs2.end_date/1000)) = year(current_date());

'''

print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()



csm = '''
delete from analytics.renewable_contact_queue
where 1=1
and report_date = current_date() ;

'''
print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = '''


insert into analytics.renewable_contact_queue 
select 
*, 
case 
    when ed.model = 'M' 
		and datediff(current_date() , lf.last_followup) > 20 
		and datediff(current_date() , cd.registration_date) <= 60 and coalesce(ltv.cltv) >= 50 then '2. New Monthly Client (No Contact in Last 3-Week)'
	when ed.model = 'Y' 
		and datediff(ed.subscription_end ,current_date() ) <= 14 then '3. Yearly Client (Subscription end within 14D)'
	when ed.model = 'Y' 
		and datediff(ed.subscription_end ,current_date() ) > 14 then '5. Yearly Client (Subscription end within this month)'
	when ed.model = '2Y' 
		and datediff(ed.subscription_end ,current_date() ) <= 14 then '4. 2-Yearly Client (Subscription end within 14D)'
	when ed.model = 'M' 
		and datediff(current_date() , lf.last_followup) > 30
		and datediff(current_date() , cd.registration_date) > 60 then '6. Old Monthly Client (No Contact in last 30D)'
	when ed.model = 'M' 
		and datediff(current_date() , lf.last_followup) <= 30 
		and datediff(current_date() , cd.registration_date) > 60 then '7. Old Monthly Client (Contact made in last 30D)'
	when datediff(current_date(), ed.subscription_end) = 0 then '1. Highest Priority for today'
	else '8. Less Priority Right Now' 
		end as priority_queue,datediff(current_date() , lf.last_followup) as last_contact  , 
        coalesce(cp.total_chat,0) as chat_30d,
        coalesce(cp.missed_chat_pct,0) as missed_chat_pct_30d,
        coalesce(off.offline_msg,0) as offline_msg_30d,
   case 
 	when (coalesce(cp.total_chat,0)>= 1000 or coalesce(off.offline_msg,0) >= 100 ) and coalesce(cp.missed_chat_pct,0)>= 20  and ed.addons_price = 0 then 'Chatbot Recommended' 
 	when coalesce(cp.total_chat,0)= 0 and coalesce(off.offline_msg,0) >= 50 and ed.addons_price = 0 then 'Chatbot Recommended' 
 	else '---' end as suggestions
from analytics.dashboard_csm_subscription_ended as ed
inner join analytics.users_superadmin_creation_date as cd on cd.usAccount = ed.operator_code 
left join analytics.dashboard_clients_last_followup as lf on lf.account_id = ed.operator_code 
left join analytics.avoid_internal_mails as im on im.mailaddr = cd.usrMailAddr 
left join analytics.clients_lifetime_value as ltv on ltv.optr_code = ed.operator_code
left join analytics.dashboard_csm_last_30d_chats_and_missed_chat_pct as cp on cp.vbAccount = ed.operator_code
left join analytics.dashboard_csm_last_30d_offchat_counts as off on off.acc= ed.operator_code
where 1=1
and im.mailaddr is null
and year(ed.subscription_end) = year(current_date()) 
and month(ed.subscription_end) = month(current_date()) 
;



'''


print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()



csm = '''

insert into analytics.customers_at_risk_most_priority_history 
select * from analytics.customers_at_risk_most_priority;

'''
print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()






csm = '''
drop table if exists analytics.customers_at_risk_most_priority;
'''
print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = '''
create table analytics.customers_at_risk_most_priority as
select wc.*, cd.convertdate ,dc.package , dc.expired_within , dc.mrr , dc.addons_price , dc.model , lf.last_followup as last_contact, lf.comments 
from analytics.customers_on_the_way_of_churn as wc
inner join analytics.dashboard_csm_subscription_ended as dc on wc.operator_code = dc.operator_code 
left join analytics.dashboard_clients_last_followup as lf on lf.account_id = wc.operator_code 
left join analytics.first_commercial_date as cd on cd.operator_code = wc.operator_code 
where 1=1
and expired_within <=30 and model in ('Y','2Y')
union all 
select wc.*, cd.convertdate , dc.package , dc.expired_within , dc.mrr , dc.addons_price , dc.model , lf.last_followup as last_contact, lf.comments 
from analytics.customers_on_the_way_of_churn as wc
inner join analytics.dashboard_csm_subscription_ended as dc on wc.operator_code = dc.operator_code 
left join analytics.dashboard_clients_last_followup as lf on lf.account_id = wc.operator_code
left join analytics.first_commercial_date as cd on cd.operator_code = wc.operator_code 
where 1=1
and expired_within <=7 and model in ('M')
order by mrr desc, expired_within asc;
'''
print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = '''
drop table analytics.customer_success_manager_performance_evaluate_9aug;
'''

print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()


csm = '''
create table analytics.customer_success_manager_performance_evaluate_9aug as
select ed.*, v2.country as country, ad.super_admin_email,ad.users_email,ad.super_admin_phone,ad.users_phones,sed.model ,
sed.subscription_end , sed.mrr , lf.last_followup as last_contact, lf.comments as crm_notes
from analytics.customer_success_manager_chat_downward_performance_evaluate ed
inner join analytics.users_superadmin_creation_date as cd on cd.usAccount = ed.operator_code 
left join analytics.avoid_internal_mails as im on im.mailaddr = cd.usrMailAddr 
left join analytics.vbclientinfo v2 on v2.clAccount = ed.operator_code
left join analytics.csm_accounts_details as ad on ad.usAccount =ed.operator_code
left join analytics.dashboard_csm_subscription_ended as sed on sed.operator_code = ed.operator_code
left join analytics.dashboard_clients_last_followup as lf on lf.account_id = ed.operator_code
where 1=1
and im.mailaddr is null;
'''

print(csm)

dwh_cursor.execute(csm)

connection_dwh.commit()



csm ='''
drop table if exists analytics.customer_success_manager_performance_evaluate_after_9aug_daily;
'''
dwh_cursor.execute(csm)

connection_dwh.commit()



csm = '''
create table analytics.customer_success_manager_performance_evaluate_after_9aug_daily as 
select ed.*, v2.country as country, ad.super_admin_email,ad.users_email,ad.super_admin_phone,ad.users_phones,sed.model ,
sed.subscription_end , sed.mrr , lf.last_followup as last_contact, lf.comments as crm_notes
from analytics.dashboard_customer_success_manager_chat_downward ed
inner join analytics.users_superadmin_creation_date as cd on cd.usAccount = ed.operator_code 
left join analytics.avoid_internal_mails as im on im.mailaddr = cd.usrMailAddr 
left join analytics.vbclientinfo v2 on v2.clAccount = ed.operator_code
left join analytics.csm_accounts_details as ad on ad.usAccount =ed.operator_code
left join analytics.dashboard_csm_subscription_ended as sed on sed.operator_code = ed.operator_code
left join analytics.dashboard_clients_last_followup as lf on lf.account_id = ed.operator_code
where 1=1
and im.mailaddr is null;
'''

dwh_cursor.execute(csm)

connection_dwh.commit()



csm = '''
drop table if exists analytics.csm_downward_clients_chat_in_xdays;
'''


dwh_cursor.execute(csm)

connection_dwh.commit()


csm = '''
create table analytics.csm_downward_clients_chat_in_xdays as
select ed.operator_code, datediff(current_date(), ed.report_date) as x , 
count(distinct date(from_unixtime(v.chatRequestTime/1000))) as total_chatday_in_xdays,
count(v.id) as chat_in_xdays, coalesce(count(v.id)/count(distinct date(from_unixtime(v.chatRequestTime/1000))),0) as avg_chat_in_xdays
from analytics.customer_success_manager_performance_evaluate_9aug as ed 
left join analytics.vbmissedchats v on v.vbAccount = ed.operator_code and date(from_unixtime(v.chatRequestTime/1000)) > ed.report_date 
where 1=1
group by 1,2;

'''



dwh_cursor.execute(csm)

connection_dwh.commit()



dwh_monitor = '''
        insert into analytics.dwh_backend_jobs(script_name,section_name,run_date) values ('csm.py','Clients Analytics',current_timestamp() + interval 6 hour);
        '''
dwh_cursor.execute(dwh_monitor)
connection_dwh.commit()

connection_dwh.close()


    ##################### End Page Visiting Part-2 ##################


