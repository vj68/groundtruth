# Blocker log

Implementation continued through every issue; none changed the product claim.

| Time (IST) | Blocker | Status | Resolution / impact |
|---|---|---|---|
| 31 Aug 2026 | Local Docker could not resolve `registry-1.docker.io` through its embedded DNS | Bypassed | Google Cloud Build pulled the base image successfully; local Python package build also passed. |
| 31 Aug 2026 | First remote image build found ambiguous flat-layout package discovery | Resolved | Constrained setuptools discovery to `app*`; wheel, sdist, and remote container build passed. |
| 31 Aug 2026 | `gemini-3.5-flash` returned 404 in `us-central1` | Resolved | Google lists PayGo availability on `global`, `us`, and `eu`; configured Vertex model location as `global`. Real three-agent call passed. |
| 31 Aug 2026 | New Cloud Run hostnames initially returned Google edge 404 despite healthy revisions and public invoker bindings | Monitoring | No request reached revision logs. The immutable image was also deployed to `asia-south1` and produced the identical edge response, isolating this to project-wide hostname registration/propagation. Both regions are capped at 0–2 instances. |

Warnings from dependencies are non-blocking: ADK 2.8 deprecates legacy `SequentialAgent` in
favor of a newer Workflow API, and FastAPI's test client emits a Starlette/httpx transition
warning. The installed, tested APIs remain functional for this submission.
