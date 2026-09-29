select  customer_id
        ,company_name 
        ,trade_name 
        ,cnpj
        ,email
        ,phone
        ,contact_name
        ,status
        ,created_at
        ,updated_at
from {{source('fincred_raw','customers')}}
