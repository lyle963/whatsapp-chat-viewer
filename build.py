"""Turn a WhatsApp chat export into a password-protected single-file web app (_build/index.html, gitignored).

Usage:  python3 build.py EXPORT.txt "Your Name As In Export"
Password: set CHAT_PASSWORD in the environment, or you'll be prompted (nothing private is stored in this file).
"""
import json, re, sys, os, subprocess, base64, getpass

if len(sys.argv) != 3:
    sys.exit(__doc__)
SRC, ME = sys.argv[1], sys.argv[2]  # ME = the sender shown on the right (green bubbles)
PW = os.environ.get('CHAT_PASSWORD') or getpass.getpass('Password: ')

rx = re.compile(r'^(\d\d/\d\d/\d\d), (\d{1,2}:\d\d)\s*([ap]m) - (.*)$')
msgs = []
for line in open(SRC, encoding='utf-8').read().replace(' ', ' ').replace('‎', '').split('\n'):
    m = rx.match(line)
    if m:
        d, t, ap, rest = m.groups()
        who, sep, text = rest.partition(': ')
        if not sep:
            who, text = '', rest  # system message
        msgs.append([d, f"{t} {ap}", who, text])
    elif msgs:
        msgs[-1][3] += '\n' + line
if not any(m[2] == ME for m in msgs):
    sys.exit(f'No messages from "{ME}". Senders found: {sorted({m[2] for m in msgs if m[2]})}')
other = next(m[2] for m in msgs if m[2] and m[2] != ME)
raw = json.dumps({"me": ME, "other": other, "msgs": msgs}, ensure_ascii=False).encode()
enc = subprocess.run(['openssl', 'enc', '-aes-256-cbc', '-pbkdf2', '-iter', '100000', '-md', 'sha256', '-pass', 'env:PW'],
                     input=raw, capture_output=True, check=True, env={**os.environ, 'PW': PW}).stdout
data = json.dumps(base64.b64encode(enc).decode())
os.makedirs('_build', exist_ok=True)
open('_build/index.html', 'w', encoding='utf-8').write(open('template.html', encoding='utf-8').read().replace('__DATA__', data))
print(len(msgs), 'messages built')
