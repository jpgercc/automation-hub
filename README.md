# Automation Hub
A personal vault of automation experiments grouped by intent — from boot-time helpers to monitored alerts and voice‑triggered workflows. The root README now focuses on the handful of automations that are more involved while leaving the smaller scripts in their folders unchanged.

## Purpose
Provide a single place to explore automation scripts that can be adapted for system initialization, messaging, finance monitoring, audiovisual helpers and web scraping.

## Testing
No automated test suite exists yet. Verify each automation manually:
- Run the Gmail responder and ensure the OAuth consent flow completes.
- Execute the stock monitor with a sample `config.json` entry to see console logs and `alert_log.json` updates.
- Trigger a voice command while `voice_control` is running to confirm the target script fires.
- Point the HTML searcher at a known page and follow the prompts to see summary output and optional export.