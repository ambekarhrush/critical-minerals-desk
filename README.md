# Element — Critical Minerals Desk

A local rare-earth research workspace. Compare dated issuer disclosures, inspect gaps and stress a hypothetical NdPr project. Initial coverage: Mountain Pass, Nolans and Eneabba.

## Run

```sh
uv sync --extra dev
cd frontend && npm ci && npm run build
cd ..
uv run uvicorn app.main:app --host 127.0.0.1 --port 8002
```

Open http://127.0.0.1:8002. No API key required. Data are curated source snapshots, not a live price feed. Every project links to its issuer source. Scenario inputs are hypothetical USD assumptions, not issuer guidance or equity valuation. The calculation excludes tax, royalties, working capital, sustaining capex, financing and by-products.

## First release

- Search and filter a focused project universe; select projects for comparison.
- Preserve the distinction between actual output, planned capacity and unknown output.
- Inspect source dates, investment questions and evidence gaps.
- Calculate a transparent pre-tax operating cash-flow NPV and price sensitivity.
- Export the evidence records and calculated scenario as JSON.

## Next releases

Automated filing ingestion, wider company coverage, IEA/USGS supply datasets, source-validated DeepSeek reports and historical changes. These are not yet implemented. No opaque project credibility scores are assigned.

## Verification

`uv run pytest` tests financial units, discounting, delays and invalid inputs. `cd frontend && npm run build` validates the client build.
