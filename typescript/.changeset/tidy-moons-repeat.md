---
"@coinbase/agentkit": patch
---

Improved type safety of the EVM wallet providers by typing `signTypedData` with viem's `TypedDataDefinition` and `waitForTransactionReceipt` with viem's `TransactionReceipt` instead of `any`
