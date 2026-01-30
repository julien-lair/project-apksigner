wget https://github.com/skylot/jadx/releases/download/v1.5.3/jadx-1.5.3.zip
 decompiler en json :  ./jadx apk.jar -d decompile-json --output-format json --deobf



 tester sur : https://www.corellium.com/blog/android-mobile-reverse-engineering




 récupérer le resources/meta-info/manisfest.mf



com.android.apksig.internal.x509.Certificate.java - deg: 19
com.android.apksig.internal.apk.p001v2.V2SchemeSigner.java - deg: 20
com.android.apksig.internal.apk.p002v3.V3SchemeSigner.java - deg: 21
com.android.apksig.internal.apk.stamp.SourceStampCertificateLineage.java - deg: 22
com.android.apksig.internal.apk.stamp.V2SourceStampVerifier.java - deg: 22
com.android.apksig.internal.apk.p002v3.V3SigningCertificateLineage.java - deg: 24
com.android.apksig.internal.apk.p003v4.V4SchemeVerifier.java - deg: 25
com.android.apksig.internal.apk.p003v4.V4SchemeSigner.java - deg: 28
com.android.apksig.internal.apk.stamp.SourceStampVerifier.java - deg: 29
com.android.apksig.SigningCertificateLineage.java - deg: 32
com.android.apksig.internal.apk.p000v1.V1SchemeSigner.java - deg: 33
com.android.apksig.internal.apk.p001v2.V2SchemeVerifier.java - deg: 36
com.android.apksig.internal.apk.p002v3.V3SchemeVerifier.java - deg: 37
com.android.apksig.ApkSigner.java - deg: 38
com.android.apksig.ApkVerifier.java - deg: 39
com.android.apksig.DefaultApkSignerEngine.java - deg: 44
com.android.apksig.internal.apk.p000v1.V1SchemeVerifier.java - deg: 52
com.android.apksig.internal.apk.ApkSigningBlockUtils.java - deg: 60



étapes suivantes :
pour les classes le splus susceptible d'être utile : 
- pourcentage d'imprtance : coef = 100/nbrMax 
  nbr * coef = %
- primtive cryptographique -> crypto : "" dans un json. -> IA wich algo (embeding pour rechecrher)
- détceteur de vulnérabilité 


curl -fsSL https://ollama.com/install.sh | sh
pkill ollama
# ollama serve
ollama pull qwen3-vl:32b
echo $OPEN_BUTTON_TOKEN