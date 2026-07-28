-- Axis Lead Engine — Supabase reference schema
-- This is a REFERENCE COPY of the live schema in Supabase project
-- mjetglnmivwphxyzflsz ("axis-os-v2"). The tables already exist and
-- are live — do NOT re-run this file. It documents what's there so a
-- new session (or a fresh Supabase project) can rebuild it if needed.

create table if not exists leads (
  place_id              text primary key,
  business_name         text not null,
  category              text,
  city                  text,
  area                  text,
  address               text,

  phone                 text,
  phone_is_mobile       boolean,
  email                 text,
  website_url           text,
  instagram             text,
  facebook              text,
  maps_url              text,

  rating                numeric(2,1),
  reviews_count         integer,
  last_review_date      timestamptz,
  review_age_days       integer,
  reviews_last_90d      integer,
  last_post_age_days    integer,
  status                text,

  need_flag             text check (need_flag in
                          ('no_website','social_as_website','broken_site',
                           'not_mobile_friendly','ads_no_landing',
                           'booking_saas_only')),
  quality_score         integer default 0,

  phone_reachable       boolean,
  social_active         boolean,
  google_reviews_active boolean,
  whatsapp_verified     boolean,
  email_verified        boolean,     -- enrichment only, never gates
  linkedin_exists       boolean,     -- enrichment only, never gates

  fully_verified        boolean default false,
  verification_status   text default 'needs_review'
                          check (verification_status in ('verified','needs_review')),
  reason                text,

  demo_url              text,
  demo_slug             text,
  send_status           text,
  wa_message_id         text,
  replied               boolean default false,
  replied_at            timestamptz,
  outcome               text check (outcome in
                          ('won','lost','no_reply','not_interested')),

  date_found            date default current_date,
  created_at            timestamptz default now(),
  updated_at            timestamptz default now()
);

create table if not exists leads_discarded (
  place_id      text primary key,
  business_name text,
  gate_failed   text,
  city          text,
  category      text,
  date_checked  date default current_date
);

-- One-time harvest plan: one row per district x keyword. harvest.py
-- walks this once; the daily job never re-scrapes discovery.
create table if not exists harvest_queue (
  id            bigserial primary key,
  city          text not null default 'Riyadh',
  district      text not null,
  lat           numeric(9,6) not null,
  lng           numeric(9,6) not null,
  radius_m      integer not null default 3000,
  keyword       text not null,
  priority      integer not null default 5,
  status        text not null default 'pending'
                  check (status in ('pending','running','done','failed')),
  places_found  integer default 0,
  cost_usd      numeric(8,4) default 0,
  last_run_at   timestamptz,
  error         text,
  unique (city, district, keyword)
);

-- Every Apify run writes one row here. harvest.py checks this before
-- every single run and refuses to spend past MONTHLY_BUDGET_USD.
create table if not exists spend_log (
  id          bigserial primary key,
  run_id      text,
  purpose     text,          -- 'harvest' | 'test' | 'orphan_sync_timeout'
  places      integer default 0,
  reviews     integer default 0,
  images      integer default 0,
  cost_usd    numeric(8,4) default 0,
  created_at  timestamptz default now()
);

create index if not exists leads_status_idx  on leads (verification_status, date_found desc);
create index if not exists leads_sent_idx    on leads (send_status, date_found desc);
create index if not exists leads_outcome_idx on leads (outcome) where outcome is not null;
create index if not exists leads_phone_idx   on leads (phone);
create index if not exists leads_quality_idx on leads (quality_score desc);
create index if not exists hq_next_idx       on harvest_queue (status, priority, id);
create index if not exists spend_month_idx   on spend_log (created_at desc);

-- Views
create or replace view daily_ten as
select business_name, area, rating, reviews_count, need_flag,
       phone, demo_url, send_status, replied
from leads
where verification_status = 'verified' and date_found = current_date
order by rating desc nulls last limit 10;

create or replace view next_ten as
select place_id, business_name, area, quality_score,
       rating, reviews_count, phone,
       coalesce(website_url,'—') as current_web
from leads
where send_status is null and quality_score > 0 and phone is not null
order by quality_score desc, reviews_count desc
limit 10;

create or replace view funnel_30d as
select date_found,
       count(*) as processed,
       count(*) filter (where verification_status = 'verified') as verified,
       count(*) filter (where send_status = 'sent')            as sent,
       count(*) filter (where replied)                         as replied,
       count(*) filter (where outcome = 'won')                 as won
from leads
where date_found > current_date - 30
group by date_found order by date_found desc;

create or replace view rejection_breakdown as
select gate_failed, count(*) as n,
       round(100.0 * count(*) / nullif(sum(count(*)) over (), 0), 1) as pct
from leads_discarded group by gate_failed order by n desc;

create or replace view need_flag_performance as
select need_flag,
       count(*) as leads,
       count(*) filter (where replied) as replies,
       count(*) filter (where outcome = 'won') as won,
       round(100.0 * count(*) filter (where replied) / nullif(count(*),0), 1) as reply_rate
from leads where send_status = 'sent'
group by need_flag order by leads desc;

create or replace view spend_this_month as
select coalesce(sum(cost_usd),0)::numeric(8,4) as spent_usd,
       count(*) as runs, coalesce(sum(places),0) as places
from spend_log where created_at >= date_trunc('month', now());

-- Security: service-role key only, everywhere.
alter table leads            enable row level security;
alter table leads_discarded  enable row level security;
alter table harvest_queue    enable row level security;
alter table spend_log        enable row level security;
revoke all on leads, leads_discarded, harvest_queue, spend_log,
             daily_ten, next_ten, funnel_30d, rejection_breakdown,
             need_flag_performance, spend_this_month
       from anon, authenticated;
