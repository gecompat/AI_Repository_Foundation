# Data Privacy and Confidentiality

Status: AUTHORITATIVE — REQUIRED

Before every file write, commit, push, export, package, upload, external transfer, or other mutation, inspect the relevant input and planned output.

If real personal, user, customer, company, organization, environment-related, or proprietary internal information is present, possible, or cannot be ruled out: **stop before any mutation or transfer and ask the user how to proceed.**

This includes personal data; internal business/customer data; real host, server, database, account, user-path, URL, endpoint, inventory, or capacity details; logs, traces, screenshots, exports, backups, production data; private documents/architecture; credentials, tokens, passwords, keys, certificates, and connection strings.

Secrets never enter version control, examples, logs, issues, PRs, or documentation. If exposed, stop distribution, report the exposure, and require rotation/revocation as appropriate.

Use synthetic, generated, public-domain, or explicitly redistributable data by default. Real diagnostic data may be inspected locally when authorized, but does not automatically become repository evidence. Review and anonymize it before any transfer. Automated scanning supports this gate but cannot replace semantic review.