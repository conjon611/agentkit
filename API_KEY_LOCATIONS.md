# API Key Locations in AgentKit Repository

This document provides a comprehensive overview of all API key occurrences in the AgentKit repository.

## Summary

This repository contains references to API keys in three main categories:
1. **Hardcoded Default Keys** - Development/testing keys that are publicly documented
2. **Environment Variable References** - References to API keys that should be provided via environment variables
3. **Template/Example Files** - Placeholder files for users to fill in their own keys

**⚠️ IMPORTANT: No actual private/secret API keys were found hardcoded in the repository.**

---

## 1. Hardcoded API Key (Public Development Key)

### Allora Network Default API Key

**Key Value:** `UP-4151d0cc489a44a7aa5cd7ef`

This is explicitly documented as a **public, development-only key** for testing purposes.

**Locations:**

#### Python Implementation
- **File:** `python/coinbase-agentkit/coinbase_agentkit/action_providers/allora/allora_action_provider.py`
- **Line:** 63
- **Context:**
  ```python
  # This is a public, development only key and should be used for testing purposes only.
  # It might be changed or revoked in the future. It is also subject to limits and usage policies.
  default_api_key = "UP-4151d0cc489a44a7aa5cd7ef"
  ```

#### TypeScript Implementation
- **File:** `typescript/agentkit/src/action-providers/allora/alloraActionProvider.ts`
- **Line:** 32
- **Context:**
  ```typescript
  // This is a public, development only key and should be used for testing purposes only.
  // It might be changed or revoked in the future. It is also subject to limits and usage policies.
  const DEFAULT_API_KEY = "UP-4151d0cc489a44a7aa5cd7ef";
  ```

**Note:** This key is safe to remain in the codebase as it's intended for public testing/development use.

---

## 2. Environment Variable References

The following API keys are referenced throughout the codebase and should be provided via environment variables:

### CDP (Coinbase Developer Platform) API Keys
- **CDP_API_KEY_NAME** - The name of the CDP API key
- **CDP_API_KEY_PRIVATE_KEY** - The private key for CDP API authentication

**Referenced in:**
- All chatbot examples (TypeScript and Python)
- Wallet providers
- CDP action providers
- MCP server templates
- create-onchain-agent templates

### OpenAI API Key
- **OPENAI_API_KEY** - Authentication for OpenAI services

**Referenced in:**
- All chatbot examples
- Framework extension examples
- Documentation and README files

### Social Platform API Keys

#### Twitter/X API Key
- **TWITTER_API_KEY** - Twitter/X API authentication

**Referenced in:**
- `typescript/agentkit/src/action-providers/twitter/`
- `python/coinbase-agentkit/coinbase_agentkit/action_providers/twitter/`
- Twitter chatbot examples

#### Neynar API Key (Farcaster)
- **NEYNAR_API_KEY** - Neynar API for Farcaster integration

**Referenced in:**
- `typescript/agentkit/src/action-providers/farcaster/`
- Farcaster chatbot examples

### Third-Party Service API Keys

#### OpenSea API Key
- **OPENSEA_API_KEY** - OpenSea marketplace API

**Referenced in:**
- `typescript/agentkit/src/action-providers/opensea/`
- CDP chatbot examples with OpenSea integration

#### Alchemy API Key
- **ALCHEMY_API_KEY** - Alchemy blockchain API

**Referenced in:**
- `typescript/agentkit/src/action-providers/alchemy/`

#### Hyperbolic Labs API Key
- **HYPERBOLIC_API_KEY** - Hyperbolic Labs services

**Referenced in:**
- `python/coinbase-agentkit/coinbase_agentkit/action_providers/hyperboliclabs/`
- Multiple test files

#### Allora Network API Key
- **ALLORA_API_KEY** - Custom Allora Network API key (optional, falls back to default public key)

**Referenced in:**
- Allora action provider tests
- Integration test configuration

### Authentication Credentials

#### Privy API Credentials
- **PRIVY_APP_ID** - Privy application ID
- **PRIVY_APP_SECRET** - Privy application secret

**Referenced in:**
- `typescript/examples/langchain-privy-chatbot/`
- Privy integration templates

---

## 3. Configuration Template Files

The following files are templates with empty placeholders for users to fill in their own API keys:

### TypeScript Examples
- `typescript/examples/langchain-cdp-chatbot/.env-local`
- `typescript/examples/langchain-twitter-chatbot/.env-local`
- `typescript/examples/vercel-ai-sdk-cdp-chatbot/.env-local`
- `typescript/examples/langchain-smart-wallet-chatbot/.env-local`
- `typescript/examples/langchain-privy-chatbot/.env-local`
- `typescript/examples/langchain-solana-chatbot/.env-local`
- `typescript/examples/langchain-farcaster-chatbot/.env-local`

### Python Examples
- `python/examples/langchain-cdp-chatbot/.env.local`
- `python/examples/langchain-twitter-chatbot/.env.local`
- `python/examples/langchain-smart-wallet-chatbot/.env.local`
- `python/examples/langchain-eth-account-chatbot/.env.local`
- `python/examples/openai-agents-sdk-cdp-chatbot/.env.local`

### Template Files (Jinja)
- `python/create-onchain-agent/templates/chatbot/.env.local.jinja`
- `python/create-onchain-agent/templates/beginner/.env.local.jinja`

**Example content:**
```
OPENAI_API_KEY=
CDP_API_KEY_NAME=
CDP_API_KEY_PRIVATE_KEY=
```

All template files contain only empty placeholders and no actual API keys.

---

## 4. Test Mock Keys

The test files contain mock/fake API keys for testing purposes. These are not real keys:

### Examples:
- `"test-api-key"` - Used throughout test files
- `"mock-api-key"` - Used in Python test fixtures
- `"alch-demo"` - Mock Alchemy API key in tests
- Mock Ethereum addresses like `"0x1234567890123456789012345678901234567890"`
- Mock transaction hashes and other blockchain identifiers

**These are all fake values used for testing and pose no security risk.**

---

## 5. Documentation References

API keys are mentioned in documentation files (README.md) with instructions on how to obtain them:

- Links to OpenAI API key creation: `https://platform.openai.com/api-keys`
- Links to CDP API key creation: `https://docs.cdp.coinbase.com/get-started/docs/cdp-api-keys`
- Instructions for various third-party services

**No actual keys are present in documentation files.**

---

## 6. Smart Contract Addresses and Blockchain Constants

The repository contains many Ethereum/Base contract addresses. These are **public blockchain addresses** and not secret keys:

### Examples:
- WETH addresses: `0x4200000000000000000000000000000000000006`
- Basenames registrar addresses
- Compound protocol addresses
- Moonwell protocol addresses
- WOW token factory addresses
- Various DeFi protocol addresses

**These are public smart contract addresses on public blockchains and are safe to include.**

---

## Security Assessment

✅ **SAFE**: No private/secret API keys found hardcoded
✅ **SAFE**: The only hardcoded key is a documented public development key
✅ **SAFE**: All other keys are referenced as environment variables
✅ **SAFE**: Template files contain only empty placeholders
✅ **SAFE**: Test files use mock/fake keys
✅ **SAFE**: Smart contract addresses are public blockchain constants

### Recommendations

1. **Current State:** The repository follows security best practices by:
   - Using environment variables for sensitive keys
   - Providing empty template files for users
   - Documenting the public development key appropriately
   - Using mock keys in tests

2. **Best Practices Being Followed:**
   - ✅ No secrets committed to version control
   - ✅ Environment variable usage for API keys
   - ✅ Clear documentation for users on key management
   - ✅ Proper separation of configuration from code

3. **Optional Improvements:**
   - Consider adding `.env` to `.gitignore` if not already present (appears to be handled via `.env.local` and `.env-local` naming)
   - Document the Allora public key's limitations and rotation policy in user-facing docs
   - Add security scanning to CI/CD pipeline to catch any future accidental commits

---

## Conclusion

This repository is **secure** with respect to API key management. No sensitive API keys have been exposed. All API keys are properly managed through environment variables, and the codebase follows industry best practices for secret management.

The only hardcoded key (`UP-4151d0cc489a44a7aa5cd7ef`) is explicitly documented as a public development key for testing purposes and poses no security risk.

---

**Last Updated:** 2026-01-02
**Generated By:** GitHub Copilot Security Scan
