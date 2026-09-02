- The primitives the OS uses to keep secrets, prove identity, and detect tampering. Three families: symmetric encryption (one shared key), asymmetric encryption (separate public and private keys), and hash functions (no key, one-way).
- This note covers the mechanism of each primitive and the security property it provides. Specific OS uses live in [[os security#Cryptographic Capabilities|capability tokens]] and [[authentication]].

# Kerckhoff's Principle

- The cryptographic algorithm should not need to be secret. The only secret is a ==key== chosen by the participants.
- Two reasons:
	- Less secret information is easier to keep secret. An algorithm shipped on every machine cannot be hidden; a key chosen per session can.
	- If the key leaks, replace it. If the algorithm leaks, the entire system is compromised.
- Restated by Shannon: "the enemy knows the system." A scheme that depends on secrecy of the algorithm is broken by definition; a scheme that depends only on key secrecy is what cryptographers actually study.

# Symmetric Encryption

- Both parties share one ==key==. Encryption and decryption use the same key.

```
  E(Data, Key) = Ciphertext
  D(Ciphertext, Key) = Data
  D(E(Data, K), K) = Data
```

**Caesar cipher** (didactic example)

- Shift each letter forward by $n$ positions in the alphabet. The key is $n \in \{1, \dots, 25\}$.
- `ATTACK AT DAWN` with $n = 13$ → `NGGNPX NG QNJA`. Trivially broken (try all 25 keys).

**AES** (production)

- Performs a sequence of substitutions and permutations parameterized by a 128- or 256-bit key. The output has no detectable relationship to the input without the key.
- $2^{128}$ possible keys — far beyond any brute-force search. Considered secure as of current public knowledge.

- Problem: the two parties must somehow share the key first. On the open Internet, this is precisely the thing they cannot do without already having a way to communicate securely. Public-key cryptography exists to bootstrap that.

# Asymmetric (Public-Key) Encryption

- Each party has a ==key pair==: a ==public key== distributed openly and a ==private key== kept secret. They are mathematically linked; recovering the private key from the public key is computationally infeasible.

```
  E(PubKey, Data) = Ciphertext       // anyone can do this
  D(PrivKey, Ciphertext) = Data      // only the private key holder
```

- To send a secret to Alice, encrypt with Alice's public key. Only Alice's private key can decrypt.
- Algorithms: ==RSA== (1977, based on the difficulty of factoring large composite numbers), elliptic-curve schemes (smaller keys, equivalent security).
- Public-key operations are 100-1000× slower than symmetric ones. Real systems use public-key crypto only to negotiate a session key, then switch to symmetric for the bulk traffic.

# Diffie-Hellman Key Exchange

- A different question: can two parties agree on a shared secret over a public channel an eavesdropper monitors? Surprisingly, yes. The 1976 Diffie-Hellman protocol predates RSA.

- Sketch:
	1. Both parties agree publicly on a large prime $p$ and a base $g$.
	2. Alice picks a private $a$, sends $g^a \bmod p$. Bob picks a private $b$, sends $g^b \bmod p$.
	3. Alice computes $(g^b)^a \bmod p = g^{ab} \bmod p$. Bob computes $(g^a)^b \bmod p = g^{ab} \bmod p$. They now share $g^{ab} \bmod p$ — their session key.
	4. The eavesdropper saw $p$, $g$, $g^a$, $g^b$. Recovering $a$ from $g^a \bmod p$ is the ==discrete logarithm problem==, computationally infeasible at the sizes used. The eavesdropper cannot derive $g^{ab}$.

- Diffie-Hellman gives a shared symmetric key without ever sending one over the wire. Used as the key-agreement step in TLS, SSH, and most modern secure protocols.

# Hash Functions

- A function $H(x) \to y$ that maps arbitrary-length input to fixed-length output, with three properties any cryptographic hash must satisfy:

**Preimage resistance**

- Given $y$, finding any $x$ with $H(x) = y$ is computationally infeasible.
- Why it matters: enables one-way storage of secrets. The verifier stores $H(\text{password})$ and checks by hashing the input; an attacker who steals the stored hash cannot recover the password.

**Second-preimage resistance**

- Given a specific $x_1$, finding a different $x_2$ with $H(x_1) = H(x_2)$ is infeasible.
- Why it matters: signed documents stay signed. An attacker cannot construct a different document with the same signature.

**Collision resistance**

- Finding *any* pair $x_1 \ne x_2$ with $H(x_1) = H(x_2)$ is infeasible.
- Stronger than second-preimage. The attacker chooses both inputs.

- Algorithms: ==MD5== and ==SHA-1== are broken (collisions found). ==SHA-2== and ==SHA-3== are current.

# HMAC and Signed Capabilities

- ==HMAC== (hash-based message authentication code) combines a hash with a secret key:

```
  HMAC(Key, Message) = H( (Key XOR opad) || H((Key XOR ipad) || Message) )
```

- Both parties hold `Key`. The sender computes `HMAC(Key, Message)` and sends it alongside the message; the receiver recomputes and compares.
- An attacker without `Key` cannot produce a valid HMAC, even after observing many (message, HMAC) pairs.
- This is the primitive behind [[os security#Cryptographic Capabilities|cryptographic capabilities]] — `Token = HMAC(Secret, ObjectId + Rights)`. Same construction, same unforgeability argument.
