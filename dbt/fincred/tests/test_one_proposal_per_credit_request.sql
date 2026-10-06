select  credit_request_id, 
        count(*) qtd
from {{ ref('fct_proposals') }}
group by credit_request_id
having count(*) > 1