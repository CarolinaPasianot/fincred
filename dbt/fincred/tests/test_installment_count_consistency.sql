select 	a.contract_id, 
		a.installment_count,  
		COUNT(b.installment_id) qtd_installment 
from {{ ref('fct_contracts') }} a
inner join  {{ ref('fct_installments') }} b on a.contract_id = b.contract_id 
group by a.contract_id, 
		a.installment_count 
having COUNT(b.installment_id) <> a.installment_count