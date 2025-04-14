SELECT 
    "movieId" as movie_id,
    "movieURL" as movie_url,
    cast("movieRank" as int) as movie_rank, 
    cast("movieYear" as int) as movie_year,
    "movieTitle" as movie_title,
    "critic_score" as critic_score,
    "audience_score" as audience_score
FROM {{ source('mlops_raw', 'movies') }}
