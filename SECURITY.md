# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| main    | Yes       |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

1. **Do not** open a public GitHub issue for security vulnerabilities.
2. Contact the project maintainers directly with a description of the issue.
3. Include steps to reproduce if possible.

## Security Practices

This application handles organizational assessment data. Follow these practices:

- **No secrets in source code** — use environment variables via `.env` (never commit `.env`).
- **Input validation** — all user input is validated server-side with Pydantic.
- **Minimal data collection** — do not enter confidential or personal information in demo mode.
- **LLM isolation** — assessment data is not sent to external LLMs without explicit user action.
- **Safe file generation** — PDF reports are generated server-side with validated inputs.

## Demo Application Notice

This is a demonstration assessment tool. Do not enter confidential, personal, proprietary, or sensitive information.
