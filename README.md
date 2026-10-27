# Atlas History — three-layer prototype

Python 3.10+ with SQLite FTS5. No third-party packages or network calls.

1. **Archive:** durable local records and full-text lookup with original IDs.
2. **Retrieval:** source-cited context packets for a separately connected chatbot.
3. **Learning loop:** explicit per-message consent, heuristic redaction, human
   review, then approved training candidates. Future model versions can use those
   candidates after independent evaluation; they still retrieve from layer 1.

## Run

Extract this folder, open a terminal inside it, and run:

```sh
python3 -m unittest -v
python3 atlas.py import /path/to/conversations.json
python3 atlas.py search "salmon"
python3 atlas.py context "What did I say about salmon?"
```

The import is a one-time bridge from an existing export. After import, search the
database directly without exporting again. It imports text from all supplied
branches and deduplicates by conversation/node ID. Attachments are not imported.
Future chatbot integrations should call Archive.add for each new message before
responding. Archive.context returns a JSON packet; connect your preferred model
separately. This prototype itself does not generate chatbot responses.

For a message ID returned by search:

```sh
python3 atlas.py consent 'CONVERSATION:NODE' yes
python3 atlas.py stage 'CONVERSATION:NODE'
# Read the staged text, remove remaining identifying/confidential material,
# and save the reviewed text to reviewed.txt. Use the returned feedback ID:
python3 atlas.py review FEEDBACK_ID reviewed.txt
python3 atlas.py feedback
python3 atlas.py consent 'CONVERSATION:NODE' no
python3 atlas.py delete 'CONVERSATION:NODE'
```

## Boundaries and next engineering work

- This is a local, single-user CLI, not an OpenAI integration or hosted product.
- It cannot recover missing/deleted records, reconstruct a training corpus, or
  establish whether a specific conversation trained a model. Training does not
  require deleting source records; model weights are not a searchable archive.
- No historical corpus is bundled. Training from 1200 BCE is neither implemented
  nor required for retrieval. Any future corpus needs lawful sourcing and provenance.
- It does not measure IQ or rank people. Chat performance and improvement are
  affected by assistance, opportunity, task difficulty, language, and other factors.
  A school assessment would need consent, validated tasks, fairness evaluation,
  and professional psychometric validation before intelligence claims.
- Redaction is heuristic, NOT guaranteed anonymization. Names, rare facts and
  indirect identifiers may remain. The internal consent linkage is deliberately
  retained to support revocation; the system does not erase accountability.
- No actual retraining or automatic promotion occurs. Evaluate privacy leakage,
  memorization, quality and regressions before releasing any trained model.
- Revocation removes queued records, not already exported copies or learned
  weights. Deletion is logical, not forensic erasure; backups must be managed too.
- The database is plaintext, protected only by local OS access controls. Use an
  encrypted disk and secure backups. Do not expose this CLI as a network service.
  A hosted version needs authentication, tenant isolation, encryption/key
  management, audit logs, retention rules, and deletion across replicas/backups.
- Source text is labeled untrusted in the context packet, but model integrations
  still need prompt-injection defenses. Do not give retrieved text tool authority.
- Access controls and provenance support confidentiality; this code does not
  grant patents, copyright protection, ownership, or guarantee legal protection.

## Public description

“A proposed three-layer AI architecture combining a private searchable history,
a retrieval-connected assistant, and a consent-based, reviewed learning loop.”

This is a prototype and proposal, not evidence of novelty or a solved IQ test.
Share a synthetic-data demo and architecture with retrieval/privacy engineers.
For school use, seek an educational measurement researcher and school privacy
lead. For missing ChatGPT history, use OpenAI Help Center support. Consider
getting IP advice before publishing details you hope to protect.
