select 	a.installment_id,
        a.contract_id,
        a.installment_number,
        a.due_date,
        a.installment_amount,
        b.payment_id,
        b.payment_date,
        b.principal_amount,
        b.interest_amount,
        b.fine_amount,
        b.total_paid_amount
from {{ref('stg_installments')}} a 
left join {{ref('stg_payments')}} b 
on a.installment_id = b.installment_id