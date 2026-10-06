select  proposal_id, 
        count(*) qtd
from {{ ref('fct_contracts') }}
group by proposal_id
having count(*) > 1