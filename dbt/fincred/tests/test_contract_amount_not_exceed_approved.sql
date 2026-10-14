select  contract_id,
        contracted_amount,
        approved_amount,
        contracted_amount - approved_amount
from {{ ref('stg_contracts') }} a
inner join {{ ref('stg_proposals') }} b on a.proposal_id = b.proposal_id
where contracted_amount - approved_amount > 0