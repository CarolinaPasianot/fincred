select  credit_request_id, 
        count(*) qtd
from {{ ref('stg_proposals') }}
group by credit_request_id
having count(*) > 1