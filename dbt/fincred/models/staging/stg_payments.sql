select  payment_id
        ,installment_id
        ,payment_date
        ,principal_amount
        ,interest_amount
        ,fine_amount
        ,total_paid_amount
from {{source('fincred_raw', 'payments')}}