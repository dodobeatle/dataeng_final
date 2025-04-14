SELECT
    "quote" as quote,
    CAST("score" as float) as score,
    CAST("rating" as float) as rating,
    "userId" as user_id,
    "movieId" as movie_id,
    "reviewId" as review_id,
    "userRealm" as user_realm,
    CAST("isVerified" as boolean) as is_verified,
    CAST("hasSpoilers" as boolean) as has_spoilers,
    CAST("creationDate" as date) as creation_date,
    CAST("hasProfanity" as boolean) as has_profanity,
    CAST("isSuperReviewer" as boolean) as is_super_reviewer,
    "userDisplayName" as user_display_name

FROM {{ source('mlops_raw', 'user_reviews') }}
