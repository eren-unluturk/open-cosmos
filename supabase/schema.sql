-- Open Cosmos: Supabase schema. Run once in the Supabase SQL editor (project "open-cosmos").
-- Safe to re-run.

-- 1. Catalog content. Anyone (the website, using the anon key) may READ. Nobody may write through the API
--    with the anon key; seeding uses the service key, which bypasses row-level security and is never deployed.
create table if not exists public.content (
  kind       text not null check (kind in ('entry', 'guide', 'lesson', 'problem', 'ui_overlay')),
  id         text not null,
  data       jsonb not null,
  updated_at timestamptz not null default now(),
  primary key (kind, id)
);

alter table public.content enable row level security;

drop policy if exists "content is public to read" on public.content;
create policy "content is public to read" on public.content
  for select to anon, authenticated using (true);
-- No insert / update / delete policies: with RLS on, those are denied for anon.

revoke all on public.content from anon, authenticated;
grant select on public.content to anon, authenticated;

-- 2. Feedback from grown-ups. The website may INSERT only. Nobody can read it through the API
--    (read it in the Supabase dashboard). Nothing identifies the sender: no name, email, IP or user id.
create table if not exists public.feedback (
  id         uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  kind       text check (kind in ('bug', 'translation', 'content', 'other')),
  message    text check (length(message) between 5 and 1000),
  page       text check (length(page) <= 200),
  lang       text check (lang in ('en', 'es', 'ar', 'hi', 'pt')),
  status     text default 'new'
);

alter table public.feedback enable row level security;

drop policy if exists "anyone may send feedback" on public.feedback;
create policy "anyone may send feedback" on public.feedback
  for insert to anon, authenticated with check (status = 'new');
-- No select / update / delete policies: denied for anon.

revoke all on public.feedback from anon, authenticated;
grant insert on public.feedback to anon, authenticated;
