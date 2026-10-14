select  proposal_id, 
        count(*) qtd
from {{ ref('stg_contracts') }}
group by proposal_id
having count(*) > 1