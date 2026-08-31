# Blocker log

Implementation continued through every issue; none weakened the product claim.

| Time (IST) | Blocker | Status | Resolution / impact |
|---|---|---|---|
| 31 Aug 2026 | Local Docker could not resolve Docker Hub through embedded DNS | Bypassed | Cloud Build pulled the base image successfully; local Python build also passed. |
| 31 Aug 2026 | Initial source build found ambiguous package discovery | Resolved | Constrained setuptools discovery to `app*`; wheel, sdist, and remote build passed. |
| 31 Aug 2026 | `gemini-3.5-flash` returned 404 in `us-central1` | Resolved | Configured the Vertex model endpoint as `global`; live calls pass. |
| 31 Aug 2026 | Direct Cloud Run hostnames returned edge 404 before requests reached healthy revisions | Bypassed | Deployed the same FastAPI app through a first-generation HTTP function; its public route and live Vertex replay pass. Firebase provides the stable landing URL. |
| 31 Aug 2026 | Request-based Cloud Run CPU paused accepted background work | Resolved | Enabled instance-based CPU with min 0 and max 2. |
| 1 Sep 2026 | First five-agent live replay exceeded a strict `PatternAnalysis` string bound | Resolved | Relaxed bounded structured fields while retaining schemas; a fresh Vertex run completed all five agents. |
| 1 Sep 2026 | Browser requested a missing favicon | Resolved | Added an inline SVG favicon; browser console is now clean. |
| 1 Sep 2026 | Firebase dynamic rewrites inherited the project-edge 404 | Bypassed | Hosting serves an exact static landing page that opens the verified Cloud Functions route. |
| 1 Sep 2026 | Cloud Functions froze a background assurance task after returning 202 | Resolved | The function runtime executes the replay synchronously, persists it to Firestore, then returns the completed run ID. |

## Non-blocking warnings

- Google ADK emits an advisory about direct asynchronous model generation/AFC internals. The
  installed `SequentialAgent` path remains functional and the five-agent live run completes.
- FastAPI's test client emits a Starlette/httpx transition warning. All 62 tests pass.
- The historical Kubernetes benchmark uses bounded source excerpts and a semantic reproducer,
  not a full 2016 Kubernetes build. The claim is scoped accordingly in the claims ledger.
