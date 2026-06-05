# SpyKiller
**SpyKiller** is an ephemeral, ultra-private automated browser environment designed to prevent data leaks, enforce advanced anti-tracking, and completely block AI/LLM data scraping or access.

It operates as a localized, short-lived secure runtime environment. Its internal pipeline is explicitly engineered to bypass persistent data storage, circumvent browser telemetry telemetry, and enforce client-side network restrictions through a 6-phase lifecycle.

# Phase 1: Ephemeral Sandbox Generation (Disk Isolation)

The moment the script is executed, it establishes a secure perimeter within the host machine's file system:

    Dynamic Sandbox Allocation: Utilizing tempfile.mkdtemp(prefix="navegador_privado_"), the script requests a cryptographically randomized directory inside the Operating System's temporary directory hierarchy (e.g., AppData\Local\Temp\ on Windows).

    Context Isolation: Inside this specialized parent directory, distinct execution subdirectories are initialized (such as the downloads path). Every tracking element, user profile configuration, cache ledger, and cookie store generated during the browser session is hardlocked into this volatile directory structure.

# Phase 2: Isolated Binary Procurement (Selenium Manager)

To eliminate traditional installation dependencies and ensure portability, SpyKiller intercepts how web drivers handle executable paths:

    Cache Redirection: The script injects an explicit runtime variable via os.environ["SE_CACHE_PATH"], shifting the default target of the underlying Selenium Manager component.

    On-Demand Sandboxed Download: If a global installation of Mozilla Firefox is missing from the system path, the automated engine reaches out securely to official Mozilla distribution channels. It downloads a standalone, matching architecture version of the Firefox stable binary and the required communication proxy (geckodriver) directly into the ephemeral sandbox created in Phase 1.

# Phase 3: Profile Hardening (about:config Optimization)

Before rendering any graphical user interface (GUI), SpyKiller rewrites the browser’s DNA via programmatic preferences manipulation (Options()):

    Native Incognito Flag (-private): Passed directly into the browser's execution flags, forcing it to spawn in a native RAM-only state that restricts runtime history serialization to disk.

    Telemetry and Phone-Home Mitigation: The profile overrides critical internal variables (toolkit.telemetry.enabled, tracking protection matrices, and fingerprinter obfuscation). This blocks automated background pings, search bar predictions, and crash reporting routines to external entities.

    Global Privacy Control (GPC): Enables privacy.globalprivacycontrol.enabled natively. This enforces strict GPC headers on every outgoing HTTP request, signaling to external servers that user data cannot be sold or harvested for AI training sets.

# Phase 4: Network-Level Anti-AI Firewall (PAC Mechanism)

To guarantee that user input cannot be leaked to large language model (LLM) providers, SpyKiller implements a local proxy auto-configuration layer instead of relying on browser extensions that can fail or be easily disabled:

    Data URI Ingestion: The program compiles a functional JavaScript routine (FindProxyForURL) and transforms it into an encoded browser string (data:application/x-ns-proxy-autoconfig,...).

    Real-time Host Interception: For every DNS resolution or HTTP request transaction initiated inside the browser, the destination domain name is instantly parsed against an internal array.

    The Blackhole Proxy Route: If the target host matches predefined AI infrastructure patterns (e.g., gemini.google.com, chatgpt.com, or API endpoints), the PAC routine instructs the browser to immediately dump the packet stream into PROXY 127.0.0.1:1. Because no local server is listening on port 1, the connection fails instantly due to immediate connection refusal, completely neutralizing data egress before it leaves the local network card.

# Phase 5: Persistence Loop & Runtime State Listener

Once the browser window is instantiated and navigated to its default destination (Brave Search), the main Python thread goes into a state of active observation:

    An asynchronous synchronization loop (while len(driver.window_handles) > 0) polls the browser framework every 1000ms to verify window handles state.

    The application listens for underlying termination hooks, such as an explicit window exit command from the user or a terminal interruption (Ctrl + C).

# Phase 6: Anti-Forensic Deconstruction & Shredding

When the persistence loop in Phase 5 is broken, the script moves directly into a mandatory finally: sequence, conducting a total digital sanitization procedure:

    Graceful Process Termination (driver.quit()): Sends an immediate termination signal to the underlying browser tree and drivers. This is critical to ensure that the operating system drops all structural file locks on disk items.

    Recursive Access Sanitization (os.walk + os.chmod): Operating systems frequently flag running executables or configuration tables with "Read-Only" privileges to prevent deletions. The clean-up logic systematically parses the sandbox tree from the bottom up, rewriting all individual permission masks to full write access (stat.S_IWRITE).

    Volatile Root Destruction (shutil.rmtree): The parent sandbox directory is completely removed from the file system. Because the sandboxed browser, temporary caches, databases, and session profiles lived entirely inside this bubble, every trace is eliminated simultaneously. This destruction loop retries up to 5 times with minor delays to clear files stuck in OS file-system lag.
