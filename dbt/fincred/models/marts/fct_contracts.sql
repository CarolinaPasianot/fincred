select 	a.proposal_id,
		b.contract_id,
		a.approved_amount,
		a.interest_rate,
		a.interest_period,
		a.fees_amount,
		a.proposal_date,
		a.expiration_date,
		a.status,
		b.contracted_amount,
		b.contract_date,
		b.installment_count,
		b.start_date,
		b.end_date
from {{ ref('stg_proposals') }} a 
inner join {{ ref('stg_contracts') }} b on a.proposal_id = b.proposal_id