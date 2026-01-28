**Class:** `com.android.apksig.internal.zip.CentralDirectoryRecord`  
**Package:** `com.android.apksig.internal.zip`  
**Role:** Represents a single entry in a ZIP archive’s *Central Directory* (the table that lists all files in the archive and holds the metadata needed to locate and decompress each file).

---

### 1. Main Purpose / Role  
| What it does | Why it matters |
|--------------|----------------|
| **Parses** the binary data of a central‑directory record from a `ByteBuffer`. | Every ZIP file ends with a central‑directory table; this class turns that raw data into a usable Java object. |
| **Provides accessors** for all of the record’s fields (file name, CRC‑32, sizes, timestamps, compression method, flags, and the offset to the corresponding Local File Header). | Callers can query these fields to know how to read or validate a particular file in the archive. |
| **Writes** a central‑directory record back into a `ByteBuffer` (`copyTo`). | Needed when the library rewrites an APK or a ZIP after adding signatures or performing other modifications. |
| **Creates** new records, either from scratch (`createWithDeflateCompressedData`) or by tweaking an existing one (`createWithModifiedLocalFileHeaderOffset`). | Useful when the signing tool needs to inject a new signature file or adjust offsets after a stream rewrite. |
| **Offers a Comparator** (`BY_LOCAL_FILE_HEADER_OFFSET_COMPARATOR`) so records can be sorted by the offset of their corresponding local file header. | Sorting is often required when re‑ordering or rebuilding the central directory. |

---

### 2. Importance in the Application  
* **Core component** of the APK‑signing/verifying subsystem.  
* The signing and verification processes operate on the ZIP representation of an APK; every file’s metadata must be known.  
* Without a correct `CentralDirectoryRecord`, the verifier would not be able to locate the signature files or validate their checksums.

---

### 3. Context & Use Case  
1. **APK Signing**  
   * When a new V1 (JAR‑signature) block is added, the library writes a new entry (`.SF` / `.RSA`) into the central directory.  
   * It uses `createWithDeflateCompressedData` to build a record with the appropriate sizes and CRC, then writes it to the output APK.

2. **APK Verification**  
   * The verifier reads the APK’s central directory by repeatedly calling `getRecord(ByteBuffer)` to build a list of all entries.  
   * It looks up the signature files by name, retrieves the CRC and sizes, and checks that the local file headers match.

3. **Re‑ordering or Re‑building**  
   * The comparator allows the library to sort entries by the offset of their local headers, which is useful when re‑arranging the APK for size or performance reasons.

4. **Zip Format Validation**  
   * The constructor is *private* – construction is controlled through static factory methods, ensuring that every record follows the ZIP specification (e.g., correct signature value, valid sizes).  
   * `getRecord` throws `ZipFormatException` if the buffer does not contain a valid central‑directory record, helping early failure in corrupt archives.

---

### 4. Key Design Choices  
* **Immutability** – all fields are `final`; once a record is created it cannot change, making it safe to share between threads.  
* **Minimal API** – only what the signing/verifying logic needs (getters, copy, create).  
* **Static factory** – enforces the ZIP format (e.g., the `RECORD_SIGNATURE` constant).  
* **ByteBuffer‑centric** – avoids copying the entire file into memory; operations work on slices of the original APK stream.

---

### 5. Summary

`CentralDirectoryRecord` is the “glue” between the raw ZIP binary data of an APK and the high‑level signing/verifying logic. It parses, exposes, and rewrites the essential metadata for each file entry. Because every verification or signature operation depends on accurate record data, this class is a core, non‑optional part of the APK‑signing library.