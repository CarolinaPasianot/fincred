select  a.proposal_id, 
        b.contract_id,
        a.status
from {{ ref('fct_proposals') }} a 
inner join {{ ref('fct_contracts') }} b on a.proposal_id = b.proposal_id
where a.status <> 'ACEITA'