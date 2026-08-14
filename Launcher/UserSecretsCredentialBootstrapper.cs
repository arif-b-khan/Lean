/*
 * QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
 * Lean Algorithmic Trading Engine v2.0. Copyright 2014 QuantConnect Corporation.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
*/

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using Microsoft.Extensions.Configuration;

namespace QuantConnect.Lean.Launcher
{
    /// <summary>
    /// Loads required credentials from .NET user secrets and validates that all required keys are present.
    /// </summary>
    public static class UserSecretsCredentialBootstrapper
    {
        private const string ManifestFileName = "required-credentials.json";

        /// <summary>
        /// Loads and validates required credentials from .NET user secrets.
        /// </summary>
        /// <param name="manifestPath">Optional explicit manifest path for tests</param>
        /// <param name="secretsConfiguration">Optional explicit secrets configuration for tests</param>
        /// <param name="requireAllCredentials">If false, missing credentials will be logged as warnings instead of errors</param>
        /// <returns>Dictionary suitable for Config.MergeSecretsWithConfiguration</returns>
        /// <exception cref="InvalidOperationException">Thrown when manifest is missing/invalid or required keys are missing (if requireAllCredentials is true)</exception>
        public static Dictionary<string, string> LoadAndValidateRequiredCredentials(
            string manifestPath = null,
            IConfiguration secretsConfiguration = null,
            bool requireAllCredentials = true)
        {
            var resolvedManifestPath = manifestPath ?? ResolveManifestPath();
            var requiredKeys = LoadRequiredKeys(resolvedManifestPath);

            var secrets = secretsConfiguration ?? new ConfigurationBuilder()
                .AddUserSecrets<Program>(optional: true)
                .Build();

            var missingKeys = new List<string>();
            var mergedSecrets = new Dictionary<string, string>();

            foreach (var key in requiredKeys)
            {
                var value = secrets[key];
                if (string.IsNullOrWhiteSpace(value))
                {
                    missingKeys.Add(key);
                    continue;
                }

                mergedSecrets[key] = value;
            }

            if (missingKeys.Count != 0)
            {
                var message = "Missing credentials in .NET user secrets: " + string.Join(", ", missingKeys) + Environment.NewLine +
                    "Configure credentials using dotnet user-secrets, for example:" + Environment.NewLine +
                    "dotnet user-secrets --project Launcher/QuantConnect.Lean.Launcher.csproj set \"<key>\" \"<value>\"";

                if (requireAllCredentials)
                {
                    throw new InvalidOperationException(message);
                }

                // In development/test environments, just warn about missing credentials
                Console.WriteLine("WARNING: " + message);
            }

            return mergedSecrets;
        }

        private static string ResolveManifestPath()
        {
            var localPath = Path.Combine(AppContext.BaseDirectory, ManifestFileName);
            if (File.Exists(localPath))
            {
                return localPath;
            }

            // Try alternative location in development
            var devPath = Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "specs", "001-credential-source-hardening", ManifestFileName);
            if (File.Exists(devPath))
            {
                return Path.GetFullPath(devPath);
            }

            throw new InvalidOperationException(
                "Credential manifest file was not found at startup. Expected file: " + localPath +
                Environment.NewLine +
                "Ensure required-credentials.json is copied to launcher output.");
        }

        private static List<string> LoadRequiredKeys(string manifestPath)
        {
            if (!File.Exists(manifestPath))
            {
                throw new InvalidOperationException("Credential manifest file not found: " + manifestPath);
            }

            var json = File.ReadAllText(manifestPath);
            var manifest = JsonSerializer.Deserialize<RequiredCredentialsManifest>(json, new JsonSerializerOptions
            {
                PropertyNameCaseInsensitive = true
            });

            var keys = manifest?.RequiredCredentialKeys
                ?.Where(key => !string.IsNullOrWhiteSpace(key))
                .Distinct(StringComparer.Ordinal)
                .ToList();

            if (keys == null || keys.Count == 0)
            {
                throw new InvalidOperationException(
                    "Credential manifest contains no required keys: " + manifestPath);
            }

            return keys;
        }

        private sealed class RequiredCredentialsManifest
        {
            public List<string> RequiredCredentialKeys { get; set; }
        }
    }
}
