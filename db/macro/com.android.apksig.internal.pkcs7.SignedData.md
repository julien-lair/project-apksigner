**Class**: `com.android.apksig.internal.pkcs7.SignedData`  
**Package**: `com.android.apksig.internal.pkcs7`  
**Role**: A lightweight, data‑only representation of the ASN.1 *SignedData* structure used in PKCS#7 (also known as CMS – Cryptographic Message Syntax).  
It is **not** a parser or encoder itself; rather, it holds the fields that a signed APK will expose once the underlying ASN.1 blob has been parsed by a dedicated reader. The class is constructed by other utility classes that read a PKCS#7 block from an APK and populate these fields.

---

### 1. Main purpose / role
- **High‑level function**: Hold the parsed contents of a PKCS#7 `SignedData` object.  
- **Key responsibilities**  
  - Store the signed data version (`int version`).  
  - Maintain a list of the digest algorithms (`List<AlgorithmIdentifier> digestAlgorithms`).  
  - Keep the encapsulated content (`EncapsulatedContentInfo encapContentInfo`).  
  - Preserve the certificates that accompany the signature (`List<Asn1OpaqueObject> certificates`).  
  - Keep any certificate revocation lists (`List<ByteBuffer> crls`).  
  - Reference the individual signers (`List<SignerInfo> signerInfos`).  

These fields mirror the ASN.1 definition of *SignedData*:

```
SignedData ::= SEQUENCE {
  version CMSVersion,
  digestAlgorithms SET OF AlgorithmIdentifier,
  encapContentInfo EncapsulatedContentInfo,
  certificates [0] IMPLICIT CertificateSet OPTIONAL,
  crls [1] IMPLICIT RevocationInfoChoices OPTIONAL,
  signerInfos SignerInfos
}
```

Because the class contains only data, it acts as a simple DTO (Data Transfer Object) that downstream components can read to perform validation or verification.

---

### 2. Importance in the application
- **Core component**: The entire APK signature verification logic depends on having a fully populated `SignedData` instance.  
- **Foundation**: Many other classes (`ApkSigningBlockUtils`, `V1SchemeVerifier`, etc.) consume this object to access certificates, CRLs, or signer details.  
- **Single point of truth**: It provides a central, immutable snapshot of the signature block that can be reused by multiple verification passes (e.g., V1 vs V2 vs V3 signature schemes).

---

### 3. Context and use case
- **Context**: Used during APK loading when the verifier encounters the *v1* (JAR signature) block or the *v2/v3* signing block that contains a PKCS#7 signature.  
- **Problem solved**:  
  1. **Parsing** – Converts a binary PKCS#7 blob into a structured Java object.  
  2. **Verification** – Exposes certificates and signer information to the verifier to check chain validity, digest algorithms, and signature integrity.  
  3. **Re‑use** – Allows the verifier to process the same signed data in different contexts (e.g., verifying the entire APK vs verifying specific entries).  

- **Flow**:  
  1. `ApkSigningBlockUtils` reads the signing block from an APK.  
  2. The PKCS#7 reader builds a `SignedData` instance.  
  3. The `V1SchemeVerifier` (and possibly other verifiers) inspect the `SignedData` object: iterate over `signerInfos`, extract certificate chains, validate CRLs, and compute message digests.

---

### 4. What you can infer (missing details)
- **No explicit methods**: The class relies on public fields or simple getters; it likely uses a library like Bouncy Castle for low‑level ASN.1 handling.  
- **Immutability**: Because the fields are `public`, the object may be modified by the parsing code but is treated as read‑only thereafter.  
- **Encoding/decoding**: The actual parsing logic is not shown, but it would involve reading an ASN.1 `SEQUENCE` and mapping each component to the appropriate field.  
- **Compatibility**: This class is part of the internal implementation, so changes to it would be version‑controlled by the APK Signature library.

---

**Summary**  
`SignedData` is a central, data‑only model representing a PKCS#7 signed block within the Android APK signing infrastructure. It is a core component that allows the rest of the verification pipeline to inspect and validate the signatures, certificates, and associated metadata embedded in an APK.