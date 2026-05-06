with staging as (
    select * from {{ ref('stg_exchange_rates') }}
),

latest as (
    select
        rate_date,
        base_currency,
        jpy_rate,
        sgd_rate,
        idr_rate,
        usd_rate,
        fetched_at,
        row_number() over (
            partition by rate_date
            order by fetched_at desc
        ) as row_num
    from staging
),

final as (
    select
        rate_date,
        base_currency,
        jpy_rate,
        sgd_rate,
        idr_rate,
        usd_rate,
        fetched_at
    from latest
    where row_num = 1
)

select * from final
