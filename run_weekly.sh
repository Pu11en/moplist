#!/bin/bash
# The whole factory, one command. Steps 1-5. Delivery (6) is deliberately separate
# so you never blast emails by accident.
set -euo pipefail
cd "$(dirname "$0")"
AS_OF="${1:-$(date +%F)}"
CITIES="${CITIES:-NEW BRAUNFELS}"

echo "=== MopList, week of $AS_OF ==="
python3 src/step1_source.py --cities "$CITIES" --days 30 --as-of "$AS_OF"
python3 src/step2_filter.py  --as-of "$AS_OF"
python3 src/step3_verify.py  --as-of "$AS_OF"
python3 src/step4_score.py   --as-of "$AS_OF"
python3 src/step5_package.py --as-of "$AS_OF"
echo "=== done. review data/delivered/ before sending anything ==="
