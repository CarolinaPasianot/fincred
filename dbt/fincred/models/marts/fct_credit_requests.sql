select 
		credit_request_id
		,customer_id
		,requested_amount
		,credit_score
		,score_consulted_at
		,status
		,rejection_reason
		,created_at
		,analysis_completed_at
		,extract(epoch from (analysis_completed_at - created_at)) / 60 processing_time_minutes
		,case 
			when status = 'APROVADA' then true
			else false
		end is_approved
		,case 
			when status = 'REJEITADA' then true
			else false
		end is_rejected
from {{ref('stg_credit_requests')}}