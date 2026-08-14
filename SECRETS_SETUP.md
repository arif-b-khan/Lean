# Credential Setup for QuantConnect Lean

This document explains how to configure credentials for local development and testing using .NET user secrets.

## Overview

QuantConnect Lean requires various credentials for connecting to brokers, data providers, and other services. To keep these credentials secure and out of version control, we use [.NET user secrets](https://learn.microsoft.com/aspnet/core/security/app-secrets) for local development.

## Required Credentials

The list of required credentials is defined in `specs/001-credential-source-hardening/required-credentials.json`. Common credentials include:

- **API Access Tokens**: `api-access-token`
- **Interactive Brokers**: `ib-user-name`, `ib-password`, `ib-account`
- **Binance**: `binance-api-key`, `binance-api-secret`
- **Coinbase**: `coinbase-api-key`, `coinbase-api-secret`
- **Intrinio**: `intrinio-password`
- And others as configured in the manifest

## Setting Up Credentials

### Prerequisites

- **.NET SDK 10.0+** installed and available in your PATH
- Access to the credentials/API keys for services you wish to integrate

### Step 1: Locate Your Secrets Store

User secrets are stored in a user-profile-specific location:

**macOS/Linux**:
```
~/.microsoft/usersecrets/<UserSecretsId>/secrets.json
```

**Windows**:
```
%APPDATA%\Microsoft\UserSecrets\<UserSecretsId>\secrets.json
```

The `<UserSecretsId>` for this project is defined in `Launcher/QuantConnect.Lean.Launcher.csproj` (typically `QuantConnect.Lean.Launcher`).

### Step 2: Add Credentials Using dotnet user-secrets

Configure each required credential using the `dotnet user-secrets set` command:

```bash
cd Launcher

# Example: Setting Interactive Brokers credentials
dotnet user-secrets set "ib-user-name" "your-ib-username"
dotnet user-secrets set "ib-password" "your-ib-password"
dotnet user-secrets set "ib-account" "your-ib-account-id"

# Example: Setting Binance API credentials
dotnet user-secrets set "binance-api-key" "your-binance-api-key"
dotnet user-secrets set "binance-api-secret" "your-binance-api-secret"

# Example: Setting Coinbase API credentials
dotnet user-secrets set "coinbase-api-key" "your-coinbase-api-key"
dotnet user-secrets set "coinbase-api-secret" "your-coinbase-api-secret"

# Example: Setting Intrinio credentials
dotnet user-secrets set "intrinio-password" "your-intrinio-password"
```

### Step 3: Verify Your Setup

List all configured secrets to verify they are set correctly:

```bash
cd Launcher
dotnet user-secrets list
```

This will display all keys you've configured (without showing the values).

### Step 4: Run the Application

When you start the Lean launcher, it will automatically:

1. Load the `required-credentials.json` manifest
2. Read your configured user secrets
3. Validate that all required credentials are present
4. Fail with a clear error message if any are missing

```bash
cd Launcher
dotnet run
```

If credentials are missing, you'll see an error like:

```
Missing required credentials in .NET user secrets: api-access-token, binance-api-key
Configure credentials using dotnet user-secrets, for example:
dotnet user-secrets --project Launcher/QuantConnect.Lean.Launcher.csproj set "<key>" "<value>"
```

## Removing / Clearing Secrets

To remove a single secret:

```bash
cd Launcher
dotnet user-secrets remove "key-name"
```

To clear all secrets for this project:

```bash
cd Launcher
dotnet user-secrets clear
```

## Troubleshooting

### "Credential manifest file was not found"

Ensure that `specs/001-credential-source-hardening/required-credentials.json` is copied to the Launcher output directory. This is configured in the project file (`.csproj`) and should happen automatically during build.

### "Missing required credentials in .NET user secrets"

Run `dotnet user-secrets list` to see which credentials are currently set, then use `dotnet user-secrets set` to add the missing ones.

### Credentials not being picked up

- Verify you're running from the `Launcher` directory or using `--project Launcher/QuantConnect.Lean.Launcher.csproj`
- Ensure your `UserSecretsId` in the `.csproj` file matches `QuantConnect.Lean.Launcher`
- Check that the environment variable `ASPNETCORE_ENVIRONMENT` is not set to `Production` (user secrets are disabled in production)

## Security Best Practices

✅ **DO**:
- Store credentials in user secrets for local development
- Use environment variables or secure vaults for CI/CD pipelines
- Rotate credentials regularly
- Never commit credentials to version control
- Use `.gitignore` to exclude config files containing credentials

❌ **DON'T**:
- Store credentials in `config.json` or committed configuration files
- Share your `secrets.json` file with others
- Log or print credential values
- Use the same credentials across environments

## Integration with CI/CD

For automated testing and deployment:

1. **GitHub Actions**: Secrets are injected via GitHub repository secrets
2. **Local CI**: Use environment variables or secure secret management tools
3. **Docker**: Pass secrets via `--secret` flag or secure environment variables

See `.github/workflows/` for examples of secret injection in CI pipelines.

## Reference

- [Microsoft: Safe storage of app secrets in development](https://learn.microsoft.com/aspnet/core/security/app-secrets)
- [.NET User Secrets documentation](https://learn.microsoft.com/dotnet/api/microsoft.extensions.configuration.usersecrets)
- QuantConnect required credentials manifest: `specs/001-credential-source-hardening/required-credentials.json`
