{{ config(materialized='view') }}

select  a.installment_id,
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
			when b.payment_date < a.due_date then 'ANTECIPADO'
			when b.payment_date = a.due_date then 'EM_DIA'
			when b.payment_date > a.due_date then 'EM_ATRASO'
			when b.payment_date is null then null
		end payment_behavior,
        case
			when b.payment_date is null then GREATEST(DATE '2026-12-31' - a.due_date, 0)
            else GREATEST(b.payment_date - a.due_date, 0)
		end days_late,
		case 
			when b.payment_id is not null then 'PAGA'
            when a.due_date < DATE '2026-12-31' then 'ATRASADA'
            else 'PENDENTE'
        end installment_status
from {{ref('stg_installments')}} a 
left join {{ref('stg_payments')}} b 
    on a.installment_id = b.installment_id