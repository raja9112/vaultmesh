## 🧩 Contribution Guidelines: Branching & Pull Requests

VaultMesh follows strict GitHub workflow rules to ensure code quality, security, and maintainability. Please follow the conventions below when contributing.

---

### 🔀 Branch Naming Conventions

Use the following format based on the purpose of the branch:

| Branch Type   | Format                        | Example                            |
|---------------|-------------------------------|------------------------------------|
| Feature       | `feature/<short-description>` | `feature/create-wallet-endpoint`   |
| Bug Fix       | `fix/<short-description>`     | `fix/private-key-encryption-error` |
| Refactor      | `refactor/<short-description>`| `refactor/api-client-handler`      |
| Documentation | `docs/<short-description>`    | `docs/update-readme-api-section`   |
| Hotfix        | `hotfix/<short-description>`  | `hotfix/missing-env-variable`      |
| R&D/Spike     | `spike/<short-description>`   | `spike/test-evm-support`           |

---

### ✅ Pull Request Rules

- 🔒 **Do not push directly to `main`.** All changes must go through a pull request.
- ✅ PRs must be created from a non-main branch.
- ✅ Each PR must be linked to an issue (if applicable) using `Closes #issue_number`.

#### PR Title and Description Format

Use clear, concise titles. Example:  
`Add API for custodial wallet creation`

**PR Description Template:**
```md
## Summary
Briefly explain the purpose of this PR.

## Changes
- List of key changes made

## Testing
- Describe test strategy or cases

## Checklist
- [ ] Code is formatted
- [ ] Tests added or updated
- [ ] CI checks passed
- [ ] No hardcoded secrets
