from __future__ import annotations

import json
import traceback
from pathlib import Path

from causal_model.extension_compression_noncommutation import (
    certify_addressable_product_lower_bound,
    certify_closed_context_factorization,
    certify_relay_tree_sharpness,
)


rows = []
for name, thunk in (
    ("product", lambda: certify_addressable_product_lower_bound(3, (2, 4, 5))),
    ("closed_factorization", lambda: certify_closed_context_factorization(3, (2, 4, 8))),
    *((f"relay_{m}", lambda m=m: certify_relay_tree_sharpness(m)) for m in range(1, 5)),
):
    try:
        certificate = thunk()
        rows.append({"name": name, "ok": certificate.verify()})
    except Exception as error:
        rows.append({"name": name, "ok": False, "error": repr(error), "traceback": traceback.format_exc()})

Path("artifacts").mkdir(exist_ok=True)
Path("artifacts/noncommutation_diagnostic.json").write_text(json.dumps(rows, indent=2) + "\n")
