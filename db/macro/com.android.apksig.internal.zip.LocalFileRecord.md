**Class:** `com.android.apksig.internal.zip.LocalFileRecord`  
**Package:** `com.android.apksig.internal.zip`  
**Purpose:** A low‑level representation of a ZIP local file header (the “Local File Header” or LFH) that is part of every entry in an APK file.  
It knows how to read a local header from an APK, expose its fields (name, extra data, data offsets, compression flags, etc.), and write a header (and optionally its data) back out to a new file or stream.

---

### Main purpose / role
* **Parse & expose LFH information** – Given a `DataSource` (the APK file) and the corresponding `CentralDirectoryRecord` (which points to the same entry in the central directory), the static `getRecord()` method reads the 30‑byte header, checks the signature, and creates an immutable `LocalFileRecord` instance that contains:
  * Entry name, name length, extra field buffer, data offsets inside the record
  * Size of the header record, size of the compressed data, compression flag, uncompressed size, CRC‑32, etc.
* **Write LFH + data** – The instance can write itself to a `DataSink`.  
  * `outputRecord()` copies the header and the original data.  
  * `outputRecordWithModifiedExtra()` lets you replace the extra field bytes while preserving everything else.  
  * `outputRecordWithDeflateCompressedData()` writes a header + data that you supply (e.g., a newly‑compressed block).  
* **Convenience helpers** – Static helpers like `outputUncompressedData()` and `getUncompressedData()` read the data part of the file entry directly, optionally decompressing it if it is compressed.

In short, the class is a *zip‑record serializer/deserializer* for APK entries.

---

### Importance in the application
* **Core** – The Android APK signature verification process relies on reading the exact bytes of each entry as they appear in the archive.  
  * `ApkVerifier` and `V1SchemeVerifier` use `LocalFileRecord` to extract the raw data that is covered by the V1 signature.  
  * `ApkSigner` (when re‑signing) rewrites local file headers and may modify the extra field or recompress data.  
* The class is a building block used by many other classes in the `com.android.apksig` hierarchy, so its correctness is vital for the entire signing/verifying tool chain.

---

### Context and use case
* **During verification**  
  * `ApkVerifier` iterates over the central directory entries.  
  * For each entry it calls `LocalFileRecord.getRecord(apk, cdRec, cdStartOffset)` to read the exact header that was originally written.  
  * It then compares the extracted header+data against the digests stored in the V1 signature block to detect tampering.  
* **During signing or re‑signing**  
  * When adding or updating a V1 signature block, the signer must re‑write the entire APK.  
  * It uses `LocalFileRecord` to copy every existing entry’s header and data unchanged, or to modify a specific entry’s extra field (e.g., to embed a new signature).  
  * `outputRecordWithDeflateCompressedData()` is used when the signer re‑compresses an entry (e.g., if the compressor is switched or the data was altered).  
* **When generating test data or debugging**  
  * The static `getUncompressedData()` helper can be called to retrieve the raw bytes for an entry for unit tests or for forensic analysis.

---

### Key Implementation Details (for reference)

| Field / Method | Purpose |
|----------------|---------|
| `RECORD_SIGNATURE` (0x04034b50) | Magic number that identifies a local file header. |
| `HEADER_SIZE_BYTES` (30) | Size of the fixed part of the header. |
| `GP_FLAGS_OFFSET`, `CRC32_OFFSET`, `COMPRESSED_SIZE_OFFSET`, `UNCOMPRESSED_SIZE_OFFSET`, `NAME_LENGTH_OFFSET`, `EXTRA_LENGTH_OFFSET`, `NAME_OFFSET` | Offsets into the byte buffer used to parse the header. |
| `mName`, `mNameSizeBytes`, `mExtra`, `mStartOffsetInArchive`, `mSize`, `mDataStartOffset`, `mDataSize`, `mDataCompressed`, `mUncompressedDataSize` | Cached values extracted from the header; immutable after construction. |
| `getRecord()` | Parses a header from the APK using the central directory entry and the start of the central directory. Handles optional data descriptor logic. |
| `outputRecord()` | Writes the header and the original compressed data to an output stream. |
| `outputRecordWithModifiedExtra()` | Allows altering the extra field while keeping the rest unchanged. |
| `outputRecordWithDeflateCompressedData()` | Writes a header that points to a new compressed byte array (used when re‑compressing). |
| `outputUncompressedData()` | Extracts the data part (compressed or uncompressed) and writes it to a sink, optionally decompressing on the fly. |
| `getUncompressedData()` | Returns the raw uncompressed byte array for an entry – handy for signature calculation. |

---

### Bottom line
`LocalFileRecord` is the *heartbeat* of the APK signature verification logic: it knows exactly how the ZIP format stores each file, can read those bytes from an existing archive, and can emit them again (or with modifications). Its reliability is essential for both signing and verifying APKs.