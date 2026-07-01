from __future__ import annotations

import argparse
import json
from pathlib import Path

from causal_model.common_mode_canonical_panels import (
    certify_common_mode_collapse,
    certify_site_bundle_resilience,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-replication", type=int, default=6)
    parser.add_argument("--max-sites", type=int, default=5)
    parser.add_argument("--max-replicates-per-site", type=int, default=4)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if min(args.max_replication, args.max_sites, args.max_replicates_per_site) < 1:
        raise ValueError("all maxima must be positive")

    collapse_rows = []
    for replication in range(1, args.max_replication + 1):
        certificate = certify_common_mode_collapse(replication)
        collapse_rows.append({
            "replication": replication,
            "independent_cell_tolerance": certificate.independent_profile.loss_tolerance,
            "common_mode_tolerance": certificate.common_profile.mode_tolerance,
            "removed_cell_count": len(certificate.one_mode_failure.removed_cells),
            "verified": certificate.verify(),
        })

    site_rows = []
    for site_count in range(1, args.max_sites + 1):
        for replicates_per_site in range(1, args.max_replicates_per_site + 1):
            certificate = certify_site_bundle_resilience(site_count, replicates_per_site)
            site_rows.append({
                "site_count": site_count,
                "replicates_per_site": replicates_per_site,
                "raw_cell_count": site_count * replicates_per_site,
                "independent_cell_tolerance": certificate.independent_profile.loss_tolerance,
                "common_mode_tolerance": certificate.common_profile.mode_tolerance,
                "verified": certificate.verify(),
            })

    report = {
        "theorem_domain": "finite canonical panels with declared common-mode failure domains",
        "collapse_rows": collapse_rows,
        "site_rows": site_rows,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
