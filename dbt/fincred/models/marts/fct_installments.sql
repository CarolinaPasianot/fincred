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
        b.total_paid_amount, 
		case  
			when payment_date < due_date then 'ANTECIPADO'
			when payment_date = due_date then 'EM_DIA'
			when payment_date > due_date then 'EM_ATRASO'
			when payment_date is null then null
		end payment_behavior,
		case
			when payment_date is null and CURRENT_DATE - due_date <= 0 then 0 
            when payment_date is null and CURRENT_DATE - due_date > 0 then CURRENT_DATE - due_date
			when payment_date - due_date > 0 then payment_date - due_date
			when payment_date - due_date <= 0 then 0
		end as days_late,
		case 
			when payment_id is null and due_date < CURRENT_DATE then 'ATRASADA'
			when payment_id is null and due_date >= CURRENT_DATE then 'PENDENTE'
			when payment_id is not null then 'PAGA'
        end installment_status
from {{ref('stg_installments')}} a 
left join {{ref('stg_payments')}} b 
on a.installment_id = b.installment_id