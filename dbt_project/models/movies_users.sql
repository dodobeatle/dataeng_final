SELECT * FROM {{ ref('user_reviews') }} ur
INNER JOIN {{ ref('movies') }} using(movie_id)