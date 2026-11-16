# WhatsApp Chat Viewer: turn an exported chat into a private, password-protected web app

**Relive an old WhatsApp conversation in a familiar WhatsApp-style interface. It runs as one encrypted HTML file you can host anywhere.**

Lost an old chat? Ask a friend to export it and send you the `.txt`. Convert it into a single encrypted web page and read it whenever you like, for as long as you like.

## Why

- **Nostalgia, archived.** Years of messages, jokes and voice-note-era memories in a UI you already know: green and white bubbles, timestamps, day dividers.
- **Private by design.** The chat is encrypted with **AES-256** (key derived from your password with PBKDF2, 100,000 rounds). The HTML file contains no readable messages, names or text. Without the password it's just noise.
- **Zero servers, zero tracking.** Decryption happens in your browser. Your password and messages never leave your device.
- **One file.** Upload `index.html` to GitHub Pages, Netlify, Cloudflare Pages, S3, or any static host. No backend and no database.
- **Handles huge chats.** Tested on a chat of 170,000+ messages. It loads the newest messages first and streams older ones as you scroll.
- **Jump to any date.** A built-in calendar in the top-right takes you straight to that day.

## Quick start

You need Python 3 and OpenSSL, both preinstalled on macOS and most Linux systems.

1. **Export the chat** in WhatsApp: open the chat, tap the contact or group name, choose **Export chat**, then **Without media**. Save the `.txt`.
2. **Build the app:**

   ```bash
   CHAT_PASSWORD='a-long-random-passphrase' python3 build.py "WhatsApp Chat with Someone.txt" "Your Name As In The Export"
   ```

   The second argument is your name exactly as it appears in the export. Your messages show on the right in green. Leave out `CHAT_PASSWORD` and you'll be prompted for it.
3. **Open or host** `_build/index.html`. Enter your password to unlock the chat.

`_build/` is gitignored, so your encrypted chat never lands in the repo.

## Hosting it

Any static host works. Upload only `_build/index.html`. Use `https://` or `localhost`, because browsers only allow in-page decryption in a secure context.

## Privacy and security notes

- Anyone who can download the file can try to guess your password offline. **Use a long random passphrase**, such as four or more unrelated words.
- Keep the original export `.txt` out of this repo. The `.gitignore` already blocks `*.txt`.
- Back up `_build/index.html`. If you delete the export, it's your only copy of the chat. It's safe to back up because it's encrypted.

## Supported export format

The parser expects WhatsApp's Android-style export lines, such as `09/09/16, 2:52 pm - Name: message`, with day/month/year dates and a 12-hour clock. Multi-line messages, system messages and `<Media omitted>` placeholders are handled. Other regional or iOS formats may need a small tweak to the regex in `build.py`.

## How it works

`build.py` parses the export, encrypts it with `openssl` (AES-256-CBC, PBKDF2-SHA256) and embeds the ciphertext in `template.html`. In the browser, the Web Crypto API derives the key from your password and decrypts the chat locally.

## Keywords

WhatsApp chat viewer, WhatsApp export viewer, read exported WhatsApp chat, WhatsApp chat archive, encrypted chat backup, WhatsApp chat to HTML, WhatsApp chat to web app, private chat archive, offline chat reader, self-hosted chat viewer.
