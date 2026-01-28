**Main purpose / role**  
`com.android.apksig.ApkSigner` is the central class that performs the signing of an Android application package (APK).  It reads an existing APK, applies one or more signature schemes (V1/JAR‑signing, V2‑APK‑signing, V3‑APK‑signing, V4‑APK‑signing), optionally creates a source‑stamp, and writes the signed result to an output file.  The class orchestrates the whole pipeline: parsing the input ZIP/central‑directory, creating the required signature blocks, handling data‑alignment constraints, and delegating the actual cryptographic operations to an `ApkSignerEngine`.  It is the API that callers (e.g., the `apksigner` command‑line tool, Android Studio, or custom build scripts) interact with when they want to sign an APK.

**Importance in the application**  
This is a **core** class.  It implements the business logic of the APK signing tool.  Without it the tool would not be able to read an APK, apply the Android‑specific signature schemes, or produce a valid signed package.  It is the primary workhorse that the command‑line wrapper (`com.android.apksigner.ApkSignerTool`) delegates to, and many other helper classes rely on it for lower‑level operations (e.g., handling ZIP entries, extracting the manifest, computing min‑SDK constraints).

**Context and use case**  
1. **Build pipeline** – During an Android build, once the unsigned APK has been assembled, the Gradle `apkSigner` task (or the `apksigner` command) creates an instance of `ApkSigner` with a list of `SignerConfig`s that describe the certificates and signing modes.  It then calls `sign()` to produce the final signed APK (and optionally a V4 signature file).  
2. **APK verification / re‑signing** – Tools that need to add or replace signatures on an already‑signed APK can construct an `ApkSigner` with the existing APK as input and the desired new signing configuration, then invoke `sign()` to write a re‑signed package.  
3. **Source‑stamp and verity** – When source‑stamping is requested, `ApkSigner` inserts a source‑stamp signature block and/or a verity block, ensuring that the APK can be verified against the original source tree.  
4. **Signature‑scheme enable/disable** – The boolean flags `mV1SigningEnabled`, `mV2SigningEnabled`, etc., allow callers to selectively enable or disable particular signature schemes (e.g., only V2 signing for a debug build).

The class internally performs several non‑trivial operations that are important for Android security:

| Key operation | What it does | Why it matters |
|---------------|--------------|----------------|
| `parseZipCentralDirectory` / `getZipCentralDirectory` | Reads the ZIP central directory of the APK to locate entries like `AndroidManifest.xml` and to discover existing signatures. | Needed to determine min‑SDK, to preserve existing signatures, and to know where to insert new ones. |
| `outputDataToOutputApk` | Writes a ZIP entry to the output APK, respecting the required data alignment for newer signature schemes. | Maintains ZIP integrity and satisfies Android runtime expectations. |
| `fulfillInspectInputJarEntryRequest` | Allows the engine to request information about a specific input entry without exposing the entire ZIP. | Enables lazy, on‑demand reading of entry data during signing. |
| `getMinSdkVersionFromApk` | Extracts the `minSdkVersion` declared in the manifest. | Used to enforce that certain signing modes (e.g., V4) are only applied to supported API levels. |

In short, `ApkSigner` is the heart of the APK signing toolchain, bridging the raw ZIP format of an APK with the sophisticated cryptographic requirements of Android’s modern signature schemes.  It is essential for producing valid, verifiable Android applications.