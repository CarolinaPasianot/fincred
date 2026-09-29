select  bureau_score_id
        ,cnpj
        ,score
        ,consulted_at
from {{source('fincred_raw', 'bureau_scores')}}