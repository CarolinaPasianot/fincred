select  contract_id
        ,proposal_id
        ,contract_date
        ,contracted_amount
        ,interest_rate
        ,interest_period
        ,fees_amount
        ,installment_count
        ,start_date
        ,end_date
from {{source('fincred_raw', 'contracts')}}