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
using System.Text.Json;
using Microsoft.Extensions.Configuration;
using NUnit.Framework;
using QuantConnect.Lean.Launcher;

namespace QuantConnect.Tests.Launcher
{
    [TestFixture]
    public class UserSecretsCredentialBootstrapperTests
    {
        [Test]
        public void ThrowsWithMissingRequiredKeysAndDoesNotLeakValues()
        {
            var manifestPath = Path.GetTempFileName();
            File.WriteAllText(manifestPath, "{\"requiredCredentialKeys\":[\"secret-key-a\",\"secret-key-b\"]}");

            var config = new ConfigurationBuilder()
                .AddInMemoryCollection(new Dictionary<string, string>
                {
                    { "secret-key-a", "sensitive-value" }
                })
                .Build();

            var exception = Assert.Throws<InvalidOperationException>(() =>
                UserSecretsCredentialBootstrapper.LoadAndValidateRequiredCredentials(manifestPath, config));

            Assert.That(exception.Message, Does.Contain("secret-key-b"));
            Assert.That(exception.Message, Does.Not.Contain("sensitive-value"));

            File.Delete(manifestPath);
        }

        [Test]
        public void LoadsOnlyRequiredKeysFromSecretsConfiguration()
        {
            var manifestPath = Path.GetTempFileName();
            File.WriteAllText(manifestPath, "{\"requiredCredentialKeys\":[\"alpha\",\"beta\"]}");

            var config = new ConfigurationBuilder()
                .AddInMemoryCollection(new Dictionary<string, string>
                {
                    { "alpha", "a" },
                    { "beta", "b" },
                    { "gamma", "c" }
                })
                .Build();

            var secrets = UserSecretsCredentialBootstrapper.LoadAndValidateRequiredCredentials(manifestPath, config);

            Assert.That(secrets.ContainsKey("alpha"), Is.True);
            Assert.That(secrets.ContainsKey("beta"), Is.True);
            Assert.That(secrets.ContainsKey("gamma"), Is.False);
            Assert.That(secrets["alpha"], Is.EqualTo("a"));
            Assert.That(secrets["beta"], Is.EqualTo("b"));

            File.Delete(manifestPath);
        }

        [Test]
        public void ManifestNotFoundThrowsWithoutLeakingPaths()
        {
            var exception = Assert.Throws<InvalidOperationException>(() =>
                UserSecretsCredentialBootstrapper.LoadAndValidateRequiredCredentials(
                    "/nonexistent/path/required-credentials.json",
                    new ConfigurationBuilder().Build()));

            Assert.That(exception.Message, Does.Contain("manifest"));
            Assert.That(exception.Message, Does.Contain("not found"));
        }

        [Test]
        public void EmptyManifestThrowsWithClearError()
        {
            var manifestPath = Path.GetTempFileName();
            File.WriteAllText(manifestPath, "{\"requiredCredentialKeys\":[]}");

            var exception = Assert.Throws<InvalidOperationException>(() =>
                UserSecretsCredentialBootstrapper.LoadAndValidateRequiredCredentials(
                    manifestPath,
                    new ConfigurationBuilder().Build()));

            Assert.That(exception.Message, Does.Contain("no required keys"));
            File.Delete(manifestPath);
        }

        [Test]
        public void MalformedManifestThrowsWithClearError()
        {
            var manifestPath = Path.GetTempFileName();
            File.WriteAllText(manifestPath, "{ this is not valid json }");

            var exception = Assert.Throws<JsonException>(() =>
                UserSecretsCredentialBootstrapper.LoadAndValidateRequiredCredentials(
                    manifestPath,
                    new ConfigurationBuilder().Build()));

            Assert.That(exception.Message, Does.Contain("invalid"));
            File.Delete(manifestPath);
        }

        [Test]
        public void SuccessfulLoadingReturnsValidDictionary()
        {
            var manifestPath = Path.GetTempFileName();
            File.WriteAllText(manifestPath, "{\"requiredCredentialKeys\":[\"key1\",\"key2\"]}");

            var config = new ConfigurationBuilder()
                .AddInMemoryCollection(new Dictionary<string, string>
                {
                    { "key1", "value1" },
                    { "key2", "value2" }
                })
                .Build();

            var secrets = UserSecretsCredentialBootstrapper.LoadAndValidateRequiredCredentials(manifestPath, config);

            Assert.That(secrets, Is.Not.Null);
            Assert.That(secrets.Count, Is.EqualTo(2));
            Assert.That(secrets["key1"], Is.EqualTo("value1"));
            Assert.That(secrets["key2"], Is.EqualTo("value2"));

            File.Delete(manifestPath);
        }
    }
}
