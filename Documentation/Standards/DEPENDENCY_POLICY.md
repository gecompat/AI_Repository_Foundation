# Dependency and External Service Policy

Status: AUTHORITATIVE

Adopt a dependency, tool, model, or service only when its benefit justifies maintenance, security, licensing, cost, privacy, reproducibility, network, and lock-in impact.

Review in this order: existing project capability, existing local tool, standard platform/library, added local dependency, free external service, paid external service. This is a review order, not a ban on a better maintained external solution. Avoid both dependency sprawl and needless reinvention.

Pin or lock versions when appropriate; avoid uncontrolled `latest` for critical workflows. Prefer project-local, isolated, virtualized, or containerized installation over system-wide changes. Make network use and data transfer explicit, minimize data, define timeout/cancellation/failure behavior, and prevent partial inconsistent mutation. Document fallback and exit strategy when material.