# Example: Transplant a Dashboard into an Existing SaaS

```text
/reeper:import github.com/example/open-dashboard
Bring its reporting dashboard into this Next.js app. Keep our Supabase auth,
existing Postgres schema, Stripe entitlements, shadcn components, and Vercel deployment.
```

Reeper should automatically establish:

- target-preserving transplant mode
- source auth, billing, and deployment are replacement candidates
- dashboard queries and visualization behavior are adaptation/reimplementation candidates
- source schema changes require explicit mapping

A likely interview sequence asks only unresolved material questions, such as:

1. whether historical source data must be imported
2. whether source chart behavior or exact visual fidelity matters more
3. whether reports are available to all paid users or a specific entitlement
4. whether rollout uses a feature flag and how rollback works

After answers, the contract might specify:

- reimplement queries against target schema
- retain source chart behavior but use target shadcn/Tailwind components
- use target Supabase sessions and Stripe entitlement middleware
- ship behind `reporting_v2` feature flag
- preserve source attribution for adapted algorithms
