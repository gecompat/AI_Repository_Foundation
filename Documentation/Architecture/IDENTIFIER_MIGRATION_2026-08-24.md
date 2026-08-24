# Foundation Project Identifier Migration — 2026-08-24

Status: AUTHORITATIVE

## Decision and scope

The Foundation source project explicitly selects `MIGRATE_EXPLICIT` for its own planning identifiers. This migration applies the Foundation persistent-identity and Registration Authority rules to the Foundation repository itself.

- Active planning work items use `WI-<SEQUENCE>`.
- Durable decisions continue to use `DEC-<SEQUENCE>` because that convention already matches the Foundation default typed-reference model.
- Persistent machine identities are registered in `.ai/identity/registry.json`.
- Historical `FND-*` work-item references remain permanent aliases and are never reused.
- Version headings such as `v1.4`/`v1.5` are release/roadmap metadata, not artifact identities, and are therefore not converted into `WI-*` identifiers.
- Historical evidence/changelog text may retain the old alias where rewriting it would falsify history. Active planning, status, handover, dependencies, and future references use the preferred `WI-*` reference.

## Work-item mapping

| Historical alias | Preferred reference |
|---|---|
| `FND-001` | `WI-0001` |
| `FND-002` | `WI-0002` |
| `FND-003` | `WI-0003` |
| `FND-004` | `WI-0004` |
| `FND-005` | `WI-0005` |
| `FND-006` | `WI-0006` |
| `FND-007` | `WI-0007` |
| `FND-008` | `WI-0008` |
| `FND-009` | `WI-0009` |
| `FND-010` | `WI-0010` |
| `FND-011` | `WI-0011` |
| `FND-012` | `WI-0012` |

The semantic-upgrade applicability work initiated after this migration is registered directly as `WI-0013`; `FND-013` was never published as repository truth and is not a reusable alias.

## Decision identities

Existing `DEC-0001` through `DEC-0012` retain their human references. `DEC-0013` records this migration. All are assigned persistent machine UIDs in `.ai/identity/registry.json` without changing their historical human references.

## Registration Authority

For Foundation-project local sequential references, `.ai/identity/registry.json` is the canonical Registration Authority state. Humans and AI MUST allocate final Foundation-project `WI-*`, `DEC-*`, and other sequential references through this registry or an equivalent serialized operation over the same authority. Scanning Markdown for the highest visible number is not a valid allocator.

The registry's allocation mapping is authoritative for preferred human-reference-to-machine-UID resolution. This migration document is authoritative for the historical `FND-*` alias mapping.

## Validation and recovery

Migration is valid only when:

- every active `FND-*` backlog identifier is mapped exactly once to a `WI-*` reference;
- no preferred `WI-*`/`DEC-*` reference is duplicated;
- all registered references resolve to unique machine UIDs;
- active project governance points to the registry and this mapping;
- historical aliases remain resolvable and are never reassigned;
- the normal Foundation CI/identity validation remains green.

Recovery does not reuse old identifiers. If this migration is later superseded, preserve both this mapping and the machine UIDs and create a new explicit migration decision.
