-- depends_on: {{ ref('fct_installments') }}

select *
from {{ref('fct_installments')}}
where (installment_status = 'ATRASADA' and due_date >= CURRENT_DATE)
or
(installment_status = 'PENDENTE' and due_date < CURRENT_DATE)