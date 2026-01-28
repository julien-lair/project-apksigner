**Class:** `com.android.apksig.internal.apk.v1.V1SchemeVerifier`  
*Public type:* `abstract class` – all of its methods are static and the constructor is private, so it’s really a utility helper that never gets instantiated.  

---

## 1. Main purpose / role  
- **Verify APK v1 signatures.**  
  The V1 scheme is the classic JAR‑signing approach that Android used before the v2/v3 schemes were introduced. It checks that the `META-INF/MANIFEST.MF` (and the optional `META-INF/CERT.RSA` / `CERT.SF` files) correctly describe every entry in the APK and that the signatures over those manifests match the actual data.  
- **Provide helper logic for the v1 verification pipeline.**  
  The class contains a number of low‑level utilities that the higher‑level `ApkVerifier` and `DefaultApkSignerEngine` call:
  * Parse the ZIP central directory and the manifest.
  * Extract the digests that need to be checked for a given entry.
  * Verify that the digests in the manifest match the digests computed from the file data.
  * Resolve the canonical JCA names for digest algorithms (e.g., “SHA‑256” → “SHA-256”).
  * Map Android SDK versions to supported digest algorithms.

---

## 2. Importance in the application  
- **Core component** – Every time an APK is verified (or signed) with the v1 scheme, this class is the heart of the process.  
- **Not a public API** – It lives in `com.android.apksig.internal.apk.v1`, so it’s intended for internal use by the `apksig` library. External code interacts with the public `ApkVerifier` or `DefaultApkSignerEngine`, which delegate to this verifier.  
- **Performance‑critical** – The verifier walks the ZIP central directory once, computes digests for each file, and compares them against the manifest entries. This must be fast and memory‑efficient because it can be run on large apps.

---

## 3. Context and use case  
| Context | What the class does | Where it is invoked |
|---------|---------------------|---------------------|
| **APK verification** | The static `verify(...)` method is called by `ApkVerifier.verify()` when the caller requests the v1 scheme. It pulls the APK’s ZIP sections, the manifest, the signature files, and then verifies that every entry’s digest matches. | `ApkVerifier` (public API) → `V1SchemeVerifier.verify()` |
| **APK signing** | When `DefaultApkSignerEngine` creates a v1 signature, it calls `V1SchemeVerifier.verify()` after the signing step to ensure the newly‑created manifest and signature files are correct. | `DefaultApkSignerEngine` (internal signer) |
| **Algorithm handling** | Methods like `getCanonicalJcaMessageDigestAlgorithm()` and `getMinSdkVersionFromWhichSupportedInManifestOrSignatureFile()` map between human‑readable digest names, the JCA names understood by `MessageDigest`, and the Android SDK version ranges that support each algorithm. | Internal logic of the verifier; used by `verify()` to decide which algorithms to accept. |
| **Duplicate entry detection** | `checkForDuplicateEntries(...)` scans the ZIP central directory for duplicate names, which would break signature verification because a manifest entry would have no unique target. | Called early in `verify()` to abort if duplicates exist. |
| **Manifest parsing** | `parseManifest(...)` turns the raw manifest bytes into a map of sections (`META-INF/CERT.RSA` → `CERT.SF` → `MANIFEST.MF`) so that the verifier can look up the digest of any entry. | Invoked by `verify()` before computing digests. |
| **Digest computation** | The `digest(String algorithm, byte[] data, int offset, int length)` overloads compute the SHA‑1/256/384/512 digests of an APK entry’s data. | Used by `verifyJarEntriesAgainstManifestAndSigners()` to check each entry. |
| **Signature‑file/manifest cross‑check** | `verifyJarEntriesAgainstManifestAndSigners()` iterates over the entries, looks up the corresponding digest in the manifest, and ensures the signature files (SF + RSA/DSA/ECDSA) actually sign those digest values. | Final stage of `verify()`. |

---

## 4. How it fits into the overall program  

1. **High‑level flow** –  
   *`ApkVerifier`* → *`V1SchemeVerifier.verify()`* → (ZIP parsing, manifest parsing, digest checks) → `Result`.  
   If the v2/v3 scheme is also requested, the verifier will later merge the v1 results with the v2/v3 results, but the v1 part is handled entirely by this class.

2. **Algorithm mapping** –  
   The class maintains a mapping from Android SDK version → supported digest algorithms (`MIN_SDK_VESION_FROM_WHICH_DIGEST_SUPPORTED_IN_MANIFEST`).  
   When verifying, it ignores digests that the current min/max SDK constraints would not support, preventing false negatives on older Android devices.

3. **Error handling** –  
   All verification errors are reported via the returned `Result` object (with `Status.FAILURE` and descriptive messages).  
   The static methods are designed to throw `IOException`, `NoSuchAlgorithmException`, or `ApkFormatException` only for unrecoverable conditions; typical verification failures are recorded in `Result`.

4. **Extensibility** –  
   The class is abstract but provides only static methods; the “abstract” modifier is mainly to prevent accidental instantiation.  
   If new v1‑style signature variations are needed (e.g., additional digest attributes), a new subclass could add helper methods without breaking the existing public API.

---

## 5. Summary  

- **Primary responsibility:** *Validate the integrity of an APK signed with the legacy JAR‑signing (v1) scheme.*  
- **Core importance:** *Central to the `apksig` library’s v1 support; all verification logic for this scheme is concentrated here.*  
- **Use case:** *Invoked automatically by `ApkVerifier` or `DefaultApkSignerEngine` when an APK needs to be checked or freshly signed with the v1 scheme.*  

This class is the workhorse that ensures that every file inside an APK matches the manifest digests, that the signatures over those digests are valid, and that no duplicate or unsupported entries slip through. Its design reflects the strict requirements of Android security: correctness, performance, and backward compatibility with older SDK versions.