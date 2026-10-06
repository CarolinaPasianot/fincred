-- depends_on: {{ ref('vw_installments_current') }}

select *
from {{ref('vw_installments_current')}}
where (installment_status = 'ATRASADA' and due_date >= CURRENT_DATE)
or
(installment_status = 'PENDENTE' and due_date < CURRENT_DATE)