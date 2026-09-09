# Contributing

Read `AGENTS.md` before work. Classify relevant data and its intended destination before mutation or transfer; stop only under the conditions in `Documentation/Standards/DATA_PRIVACY_AND_CONFIDENTIALITY.md`. Use a focused branch and pull request by default; keep commits coherent and factual.

For a change:

1. state scope and affected contracts;
2. avoid unrelated cleanup and governance duplication;
3. record material durable decisions;
4. run `python tools/foundation_validator.py`;
5. add targeted validation appropriate to the change;
6. report unexecuted checks truthfully;
7. update status/handover when continuation facts change.

New dependencies, copied third-party material, capabilities, or adapters require the reviews defined under `Documentation/Standards/`. By contributing, you agree that your contribution is provided under this repository's MIT license.
