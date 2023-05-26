[app]

title = Chat-Gpi
package.name = chat_gpi


source.dir = .

version = 1.0.0
version.filename = main.py



source.include_exts = py,png,jpg,kv,atlas
source.include_patterns = assets/*,images/*.png
source.exclude_exts = spec
source.exclude_dirs = tests, bin
source.exclude_patterns = license,*/*.jp*

orientation = portrait

requirements = kivy, python-telegram-bot, psutil

android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE

android.api = 29
android.minapi = 21
android.sdk = 28
android.ndk = 21.3.6528147
android.private_storage = True

[buildozer]
android.debug = True