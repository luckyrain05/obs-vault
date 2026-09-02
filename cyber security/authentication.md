- The mechanism that maps a person at a keyboard to a [[os security|principal]] the kernel will treat as them. Builds on the [[cryptography|crypto primitives]] — most authentication schemes are an application of hash functions, public-key crypto, or both.
- Three families of evidence: ==something you know== (password), ==something you have== (token, smart card, phone), ==something you are== (biometric). Real systems combine them; each family has distinct failure modes.

# Passwords

- The user shares a secret string with the server. To authenticate, present the string; if it matches, identity is established.
- Easiest scheme to implement and the most heavily attacked.

**Password storage**

- Storing the password directly is wrong. A breach of the password file leaks every credential. Users reuse passwords; the breach compromises other systems too.
- Store $H(\text{password})$ instead, using a [[cryptography#Hash Functions|cryptographic hash]]. To verify: hash the input, compare against the stored hash. The hash's preimage resistance means a stolen file does not directly reveal passwords.

**Precomputation attack**

- Precompute $H(p)$ for every common password $p$. When the hash file leaks, look each entry up in the precomputed table. ==Rainbow tables== compress this efficiently — a 100GB rainbow table covers most common passwords.
- ==Salt== defeats it: store $(s, H(s + \text{password}))$ where $s$ is a random per-user string. The attacker would need a separate rainbow table per salt; the storage cost is no longer amortized across users.

**Slow hashes**

- Standard cryptographic hashes (SHA-2 etc.) are designed to be fast — billions of evaluations per second on a GPU. Useful for general signing; bad for passwords because attackers also evaluate billions per second.
- ==bcrypt== is deliberately slow (configurable iteration count, ~100ms per evaluation). ==scrypt== adds large memory requirements that defeat GPU parallelism.
- The slowdown costs the attacker proportionally more than the legitimate user (one check vs. billions of guesses).

# Challenge-Response

- Sending the password over the network is risky — an eavesdropper records it. Challenge-response avoids transmitting the secret.

```
  1. Both sides know secret s.
  2. Server picks a random r and sends it.
  3. Client computes H(r + s) and sends it.
  4. Server computes the same and checks for equality.
```

- The value sent over the wire is `H(r + s)`. An eavesdropper sees `r` and `H(r + s)` but cannot derive `s` (preimage resistance). Replaying the captured response fails because the server picks a fresh `r` next time.

# Lamport Hash Chains

- One-time passwords without exchanging them in advance. Computed by repeatedly applying a hash starting from a seed.

```
  Choose password p. Pick depth k (e.g. 1000).
  Server stores H^k(p) = H(H(H(... H(p) ...))).

  First login:    client sends H^{k-1}(p).
                  Server checks H( H^{k-1}(p) ) == stored value.
                  Server replaces stored value with H^{k-1}(p).
  Next login:     client sends H^{k-2}(p).
                  Server checks, replaces, etc.
```

- Each login's transmitted value is one preimage step before the stored value — easy for the client (apply $H$ one fewer time), infeasible for an eavesdropper (preimage resistance).
- After $k$ logins, the chain is exhausted; user re-enrolls with a new seed.

# Physical Tokens

- Something the user physically possesses that proves identity. Oldest example: a metal key.
- Modern: ATM cards, smart cards, RFID badges, phones running an authenticator app, hardware security keys.

**Smart card**

- A chip with a stored secret key and the ability to perform cryptographic operations. The reader sends a challenge; the card computes the response on-card without revealing the key.
- The reader never learns the key — even a malicious or compromised reader cannot impersonate the card later.

**RFID**

- The card has no battery. The reader emits radio waves; the card harvests energy from them, computes the response, and transmits it back. Same crypto as a smart card, contactless.

# Biometrics

- Measure something intrinsic to the person: fingerprint, retina, face, voiceprint, gait.
- Two phases:
	- ==Enrollment==: take measurements of the user, convert to a digital template, store. Often repeated to capture natural variation.
	- ==Verification==: take a fresh measurement, compare to the stored template, accept if "close enough."

- Two error rates trade off:
	- ==False reject rate== (FRR): genuine user denied. Annoying.
	- ==False accept rate== (FAR): impostor accepted. Dangerous.
	- Tightening the comparison threshold lowers FAR but raises FRR. The crossover point depends on the modality (retinas are more discriminating than gait).

**Revocation problem**

- A stolen password is replaced by choosing a new one. A stolen biometric template is permanent — the user cannot grow new fingerprints.
- Once a fingerprint database leaks, every system using fingerprint auth on those users is permanently degraded.

# PassKeys

- A modern alternative to passwords. Uses [[cryptography#Asymmetric (Public-Key) Encryption|public-key crypto]].
- Mechanism:
	1. The device generates a fresh key pair when the user creates an account on a site.
	2. The private key stays on the device, locked behind biometric or PIN unlock.
	3. The public key goes to the server.
	4. To log in, the server sends a challenge; the device signs it with the private key; the server verifies with the stored public key.
- Wins:
	- The server never holds a password-equivalent. A breach exposes only public keys, which are useless to an attacker.
	- The signature is bound to the website's origin (TLS handle), so a phishing site cannot trick the device into signing for it. ==Phishing-resistant==.
	- Nothing to remember; the device's biometric or PIN unlocks everything.
- Drawbacks: vendor lock-in (Apple/Google/Microsoft each sync passkeys within their ecosystem); device loss requires account recovery (often the weakest link); inconsistent support across services.
