"""Pseudo-terminal smoke test for the console game: steer once, then quit."""
import os
import pty
import select
import subprocess
import sys
import time

exe = sys.argv[1] if len(sys.argv) > 1 else "./build/pacman"
master, slave = pty.openpty()
proc = subprocess.Popen([exe], stdin=slave, stdout=slave, stderr=slave, close_fds=True)
os.close(slave)
time.sleep(0.2)
os.write(master, b"d")
time.sleep(0.4)
os.write(master, b"q")
out = b""
deadline = time.time() + 8
while time.time() < deadline:
    ready, _, _ = select.select([master], [], [], 0.2)
    if ready:
        try:
            out += os.read(master, 65536)
        except OSError:
            break
    if proc.poll() is not None:
        while True:
            ready, _, _ = select.select([master], [], [], 0.2)
            if not ready:
                break
            try:
                out += os.read(master, 65536)
            except OSError:
                break
        break
rc = proc.wait()
os.close(master)
text = out.decode("utf-8", "replace")
assert rc == 0, "exit code %r" % rc
assert "PAC-MAN" in text and "SCORE" in text, "no frame rendered"
assert "BYE" in text, "no quit message"

master2, slave2 = pty.openpty()
proc2 = subprocess.Popen([exe], stdin=slave2, stdout=slave2, stderr=slave2, close_fds=True)
os.close(slave2)
time.sleep(0.4)
os.close(master2)
rc2 = proc2.wait(timeout=8)
assert rc2 == 0, "exit code on tty hangup %r" % rc2
print("pty smoke ok")
