with source as (
    select * from `de-pipeline-demo-495506.exchange_rates.daily_rates`
),

renamed as (
    select
        fetched_at                          as fetched_at,
        base_currency                       as base_currency,
        cast(date as date)                  as rate_date,
        cast(jpy as float64)                as jpy_rate,
        cast(sgd as float64)                as sgd_rate,
        cast(idr as float64)                as idr_rate,
        cast(usd as float64)                as usd_rate
    from source
)

select * from renamed
