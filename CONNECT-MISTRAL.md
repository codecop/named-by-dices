# Connect Mistral

Steps to push from a Vibe sandbox to GitHub.

## 1. Enable the GitHub connector in Mistral Studio

- Open Studio -> Connectors -> the GitHub App card -> Connect and finish the OAuth authorisation ("Act on your behalf").
- In the session, release the connector so `GH_TOKEN` lands in the sandbox environment and `gh` is logged in as your account.
- Set all tools to "Allowed" in the connector configuration.

## 2. Install the Mistral GitHub App on GitHub

This is the decisive step. Without an installation there is no token with write access and every push fails with `403`.

- Go to <https://github.com/apps/mistralai/installations/new>.
- Choose the account (e.g. `codecop`) and the repository selection: "All repositories" or "Only select repositories" -> select the target repository (e.g. `naming-by-dices`).
- Check the permissions (Settings -> Installations -> MistralAI): **Contents: Read and write** and **Pull requests: write** must be granted.

## 3. Reconnect the connector

- Disconnect and reconnect the connector in Studio (or start a new session) so a fresh user access token is minted that knows the new installation. The token is short-lived and renewed before it expires.

## 4. Work with git in the sandbox as usual

- Clone the repository: `git clone https://github.com/<owner>/<repo>.git` (public repositories also clone anonymously).
- Create a branch, edit, commit: `git checkout -b vibe/<topic>`, `git commit -m "..."` (disable commit signing locally if GitHub rejects the signature: `git config commit.gpgsign false`).
- Push: `git push -u origin <branch>` - the token is injected automatically via the Sandbox Proxy, so no manual credential helper is needed, and never write a token into a file, URL or remote.
- Open a pull request: `gh pr create` or via the `pull/new/<branch>` URL on GitHub.

**Rule of thumb:** the connector in Studio grants tool access and identity; the GitHub App installation grants the actual repository permissions (Contents: write). Both are required, otherwise push stays read-only with a 403.
