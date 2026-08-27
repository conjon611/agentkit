---
"@coinbase/agentkit": patch
---

Fixed analytics failures surfacing as unhandled promise rejections, which could crash the process on wallet provider initialization and action invocation
