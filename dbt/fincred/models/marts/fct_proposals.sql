select  proposal_id,
        credit_request_id, 
        approved_amount,
        interest_rate,
        interest_period,
        fees_amount,
        proposal_date,
        expiration_date,
        status
from {{ ref('stg_proposals')}}