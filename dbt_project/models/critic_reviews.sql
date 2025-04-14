SELECT
    "quote" as quote,
    CAST("isFresh" as boolean) as is_fresh,
    CAST("isRtUrl" as boolean) as is_rt_url,
    "movieId" as movie_id,
    CAST("isRotten" as boolean) as is_rotten,
    CAST("reviewId" as int) as review_id,
    "reviewUrl" as review_url,
    "criticName" as critic_name,
    CAST("isTopCritic" as boolean) as is_top_critic,
    "reviewState" as review_state,
    CAST("creationDate" as date)as creation_date,
    "criticPageUrl" as critic_page_url,
    "originalScore" as original_score,
    "publicationUrl" as publication_url,
    "scoreSentiment" as score_sentiment,
    "publicationName" as publication_name
FROM {{ source('mlops_raw', 'critic_reviews') }}