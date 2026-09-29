select  installment_id
        ,contract_id
        ,installment_number
        ,due_date
        ,installment_amount
from {{source('fincred_raw', 'installments')}}