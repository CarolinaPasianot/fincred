select  credit_request_id
        ,customer_id
        ,requested_amount
        ,credit_score
        ,score_consulted_at
        ,status
        ,rejection_reason
        ,created_at
        ,analysis_completed_at
from {{source('fincred_raw', 'credit_requests')}}
