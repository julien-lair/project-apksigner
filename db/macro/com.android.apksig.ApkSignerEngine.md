**Class:** `com.android.apksig.ApkSignerEngine`  
**Type:** `interface`  
**Package:** `com.android.apksig`  
**Implements:** `Closeable`  

---

## 1. Main purpose / role
`ApkSignerEngine` is the **high‑level abstraction that drives the APK‑signing workflow**.  
It defines a contract for a component that:

| Step | What the method does (high level) |
|------|-----------------------------------|
| `setExecutor` | Accepts an executor that will run long‑running tasks (e.g., signature calculation). |
| `initWith` | Initializes the engine with the raw manifest bytes and the set of entries that are part of the signing block. Returns the set of entries that will actually be signed. |
| `inputApkSigningBlock` | Feeds the engine the existing APK‑signing block (zip section) before any modifications. |
| `inputJarEntry` | Provides an entry (file) from the APK that will be part of the signature. Returns instructions that control how the entry is processed. |
| `outputJarEntry` | Declares an entry that the engine must emit into the signed APK. Returns a request object that will receive the signed bytes. |
| `inputJarEntryRemoved` / `outputJarEntryRemoved` | Handle entries that are removed from the APK – e.g., updates or roll‑back operations. |
| `outputJarEntries` | Triggers the signing of the accumulated jar entries and returns a request that contains the resulting signature data. |
| `outputZipSections` / `outputZipSections2` | Create the new or updated APK‑signing zip sections (V1, V2, V3, V4). The old method is deprecated in favour of the newer API. |
| `outputDone` | Marks the end of the output phase, letting the engine flush or finalize state. |
| `signV4` | Convenience helper for signing only the V4 scheme directly to a file. |
| `isEligibleForSourceStamp` / `generateSourceStampCertificateDigest` | Optional support for the *source‑stamp* feature – a digest that can be embedded in the signing block to prove the original build source. |
| `close` | Releases any resources held by the engine (e.g., temporary files or thread pools). |

In short, **the engine mediates the entire signing process**: it receives the APK contents, orchestrates the hashing/signing logic for each supported scheme (V1/V2/V3/V4), and produces the final signed output.

---

## 2. Importance in the application
- **Core component**: Every operation that signs or verifies an APK in the Android build tools uses an implementation of this interface (e.g., `DefaultApkSignerEngine`).  
- **Central orchestration point**: It hides the intricacies of the various signing schemes and zip‑section handling from higher‑level callers (`ApkSigner`, Gradle plugins, `apksigner` CLI).  
- **Extensibility hub**: New signing schemes or changes to the APK‑signing block format can be added by creating a new engine implementation that conforms to this contract.

Because the entire signing workflow hinges on this interface, it is a **critical, low‑level building block** of the Android SDK tooling.

---

## 3. Context and use case
1. **When a developer or CI system builds an Android app**  
   - The `apksigner` command (or Gradle’s `:app:assembleRelease`) constructs an instance of a concrete `ApkSignerEngine` (typically `DefaultApkSignerEngine`).  
   - It first calls `initWith` with the APK’s `AndroidManifest.xml` bytes and the set of entries that should be signed.  
   - It feeds the current signing block (if any) via `inputApkSigningBlock`.  
   - For each file that will be part of the APK, the caller calls `inputJarEntry` to provide the bytes and receives instructions on how to process them.  
   - The engine aggregates the hash of each file according to the chosen schemes.  
   - When the APK is ready for output, the caller invokes `outputJarEntries` and the optional `outputZipSections`/`outputZipSections2` to generate the new signing block.  
   - Finally `outputDone` and `close` are called to flush the output and release resources.

2. **When updating an existing APK**  
   - The engine supports *removal* of entries (`inputJarEntryRemoved` / `outputJarEntryRemoved`) so that incremental updates can be signed without recomputing the entire signature.

3. **When signing only a V4 signature**  
   - The `signV4` helper can be used by tools that need to embed a V4 signature in a separate file (used in some build‑time tooling).

4. **When verifying source‑stamp information**  
   - The optional source‑stamp methods allow an engine implementation to embed a digest of the signing certificate chain, which can later be verified to prove that the APK was produced from a particular source tree.

---

### Summary
`ApkSignerEngine` is the **engine‑level contract for APK signing**.  
It abstracts the sequence of input (existing APK, manifest, jar entries), processing (hashing, signing), and output (new signing block, V4 signature file) steps that any implementation must perform.  
Because it is the foundation for the Android build system’s signing pipeline, it is a **core, highly‑critical** class in the overall application.