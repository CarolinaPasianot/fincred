select  contract_id,
        contracted_amount,
        approved_amount,
        contracted_amount - approved_amount
from {{ ref('fct_contracts') }}
where contracted_amount - approved_amount > 0