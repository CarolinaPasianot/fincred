-- depends_on: {{ ref('vw_installments_current') }}

select *
from {{ ref('vw_installments_current') }}
where (
    installment_status = 'ATRASADA'
    and due_date >= DATE '2026-12-31'
)
or (
    installment_status = 'PENDENTE'
    and due_date < DATE '2026-12-31'
)
