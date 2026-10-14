{{ config(materialized='view') }}

with parcelas as (
    select  contract_id,
            COUNT(installment_id) qt_installment_total,
            SUM(case
                    when installment_status = 'PAGA' then 1
                    else 0
                end) qt_installment_paid,
            COALESCE(SUM(installment_amount),0) total_installment_amount,
            COALESCE(SUM(case 
                            when installment_status in ('PENDENTE', 'ATRASADA') then installment_amount
                            else 0
                        end),0) open_installment_amount,
            COALESCE(SUM(principal_amount),0) principal_amount,
            COALESCE(SUM(interest_amount),0) interest_amount,
            COALESCE(SUM(fine_amount),0) fine_amount,
            COALESCE(SUM(total_paid_amount),0) total_paid_amount,
            MAX(case
                    when installment_status = 'ATRASADA' then days_late
                    else 0
                end) max_days_late

    from {{ref('vw_installments_current')}}
    group by contract_id

)

select  a.contract_id,
        b.qt_installment_total, 
        b.qt_installment_paid, 
        b.total_installment_amount,
        b.open_installment_amount,
        b.principal_amount,
        b.interest_amount,
        b.fine_amount,
        b.total_paid_amount,
        b.max_days_late days_late,
        case
            when b.max_days_late > 90 then 'INADIMPLENTE'
            when b.open_installment_amount > 0 and b.max_days_late between 1 and 90 then 'ATRASADA'
            when b.open_installment_amount = 0 then 'EM_DIA'
            else 'EM_DIA'
        end contract_situation
from {{ref('stg_contracts')}} a 
inner join parcelas b on a.contract_id = b.contract_id