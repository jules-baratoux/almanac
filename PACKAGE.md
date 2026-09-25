Test the app on an Android device
```shell
flet run --android
```

Create the signing key
```powershell
keytool -genkey -v -keystore "C:/Users/jules/keystores/fr.baratoux.jules.almanac.jks" -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

Build for testing on Android
```shell
flet build apk
```

Build for Google Play Store
```shell
$env:FLET_ANDROID_SIGNING_KEY_STORE_PASSWORD = ...
$env:FLET_ANDROID_SIGNING_KEY_PASSWORD = ...
flet build aab
```


## Registering this package name, add your public key.
### Retrieving SHA-256 from a keystore file
```shell
keytool -list -v -keystore "C:/Users/jules/keystores/fr.baratoux.jules.almanac.jks" -alias upload
```
The long string of colon-separated hexadecimal characters next to SHA256: is your public SHA-256 certificate fingerprint.


## Create an app
https://play.google.com/console/u/0/developers/5584278303172842028/create-new-app

