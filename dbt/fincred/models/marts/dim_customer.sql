select  customer_id
        ,company_name
        ,trade_name
        ,cnpj
        ,status
        ,created_at
        ,updated_at
from {{ref('stg_customers')}}