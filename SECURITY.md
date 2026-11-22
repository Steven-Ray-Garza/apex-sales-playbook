# Security, Privacy, and Compliance Policy

## Data Handling & Repository Hygiene

1. **Zero PII in Version Control:** Never commit real customer names, phone numbers, email addresses, recordings, or raw call transcripts to Git. Keep raw transcripts exclusively inside the gitignored `transcripts/` directory.
2. **Zero Third-Party Copyrighted Material:** Keep private books, paid training documents, or third-party transcripts strictly inside the gitignored `sources/` directory.
3. **Zero Secrets or Credentials:** Never commit API keys, tokens, `.env` files, or private keys.
4. **Automated Enforcement:** Every push and pull request is scanned by `.github/workflows/ci.yml` for forbidden extensions (`.pdf`, `.docx`, `.gdoc`, `.env`), tracked private folders, third-party trademark/copyright leaks, hardcoded local paths, API keys, SSNs, and unredacted phone numbers.

## Legal & Regulatory Compliance Reminders

Operators deploying workflows from this repository remain solely responsible for verifying compliance with applicable law in their jurisdiction, including:

- **Labor & Classification:** W-2 vs. 1099 classification, FLSA/state overtime, meal/rest breaks, and inside-vs-outside sales exemptions.
- **Telecom & Messaging:** TCPA, state mini-TCPA rules, documented Prior Express Written Consent (PEWC), A2P 10DLC carrier registration, and STIR/SHAKEN attestation.
- **Advertising & Payments:** FTC Endorsement Guides (typicality disclosures), transparent written fee/cancellation terms, and truthful guarantee disclosures.

## Reporting Issues

If you discover a security bug, secret leak, or calculation defect, open a private security advisory or contact the repository owner directly.
