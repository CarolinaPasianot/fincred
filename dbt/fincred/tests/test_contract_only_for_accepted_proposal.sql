select  a.proposal_id, 
        b.contract_id,
        a.status
from {{ ref('stg_proposals') }} a 
inner join {{ ref('stg_contracts') }} b on a.proposal_id = b.proposal_id
where a.status <> 'ACEITA'