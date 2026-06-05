import os
import stat
import shutil
import tempfile
import time
import urllib.parse
import selenium
import selenium.webdriver
import selenium.webdriver.firefox.webdriver
import selenium.webdriver.firefox.options
import selenium.webdriver.firefox.service

def forcar_exclusao_pasta(caminho_pasta, max_tentativas=5, intervalo=1):
    """
    Forcibly removes a folder, changing read-only file permissions 
    and performing loop retries in case the browser process is still closing.
    """
    if not os.path.exists(caminho_pasta):
        return

    # 1. Remove the 'read-only' property from all internal files and directories
    for raiz, diretorios, arquivos in os.walk(caminho_pasta, topdown=False):
        for arquivo in arquivos:
            try:
                os.chmod(os.path.join(raiz, arquivo), stat.S_IWRITE)
            except Exception:
                pass
        for diretorio in diretorios:
            try:
                os.chmod(os.path.join(raiz, diretorio), stat.S_IWRITE)
            except Exception:
                pass

    # 2. Retry loop to wait for the actual termination of Firefox processes
    for tentativa in range(max_tentativas):
        try:
            shutil.rmtree(caminho_pasta)
            print(f"[+] Success! All traces in '{caminho_pasta}' have been permanently eliminated.")
            return True
        except PermissionError:
            if tentativa < max_tentativas - 1:
                print(f"[-] Files still locked by the system. Attempt {tentativa + 1}/{max_tentativas}. Waiting {intervalo}s...")
                time.sleep(intervalo)
            else:
                print(f"[!] Error: Could not release files after {max_tentativas} attempts.")
        except Exception as e:
            print(f"[!] Unexpected error while cleaning the folder: {e}")
            break
    return False

def iniciar_navegador_privado():
    # Create temporary directories
    pasta_temporal = tempfile.mkdtemp(prefix="navegador_privado_")
    pasta_downloads = os.path.join(pasta_temporal, "downloads")
    os.makedirs(pasta_downloads)
    
    # --- AUTOMATIC & ISOLATED BROWSER DOWNLOAD CONFIGURATION ---
    # Redirects Selenium Manager cache to our temporary folder.
    # If Firefox is missing, Selenium will automatically download it HERE.
    # When the script exits, the downloaded browser is completely shredded!
    os.environ["SE_CACHE_PATH"] = os.path.join(pasta_temporal, "selenium_cache")
    # ------------------------------------------------------------
    
    print("="*60)
    print(" PYTHON PRIVATE BROWSER (ANTI-LEAK & ANTI-AI MECHANISM) ")
    print("="*60)
    print(f"[+] Ephemeral session created at: {pasta_temporal}")
    print(f"[+] Session downloads: {pasta_downloads}")
    print(f"[+] AI & LLM Blocking: Enabled (Including Gemini/Google AI)")
    print(f"[+] Automated Browser Management: Active (Zero-trace cache)")
    print("-"*60)

    # Firefox Configurations using explicit package namespace
    options = selenium.webdriver.firefox.options.Options()
    options.add_argument("-private") # Forces native Private Browsing mode
    
    # Force Selenium Manager to manage and obtain the browser binary if not found globally
    options.browser_version = "stable"
    
    # Advanced privacy preferences (About:config)
    options.set_preference("browser.privatebrowsing.autostart", True)
    options.set_preference("places.history.enabled", False) 
    options.set_preference("privacy.sanitize.sanitizeOnShutdown", True) 
    options.set_preference("privacy.clearOnShutdown.history", True)
    options.set_preference("privacy.clearOnShutdown.cookies", True)
    options.set_preference("privacy.clearOnShutdown.cache", True)
    
    # Telemetry and Tracking Protection
    options.set_preference("toolkit.telemetry.enabled", False)
    options.set_preference("privacy.trackingprotection.enabled", True)
    options.set_preference("privacy.fingerprintingProtection", True) 

    # Default Search Engine: Brave Search
    options.set_preference("browser.search.defaultenginename", "Brave")
    options.set_preference("browser.search.selectedEngine", "Brave")
    options.set_preference("browser.urlbar.suggest.searches", False)

    # --- ANTI-AI AND LLM BLOCKING CONFIGURATION ---
    # 1. Enable Global Privacy Control (Signals websites NOT to use data for AI training)
    options.set_preference("privacy.globalprivacycontrol.enabled", True)
    
    # 2. Deploy a Proxy Auto-Config (PAC) script as a Data URI to drop AI domain connections
    pac_script = """
    function FindProxyForURL(url, host) {
        var aiDomains = [
            "openai.com", "chatgpt.com", "anthropic.com", "claude.ai", 
            "perplexity.ai", "cohere.com", "midjourney.com", "groq.com",
            "stability.ai", "copy.ai", "jasper.ai", "suna.ai",
            "gemini.google.com", "google.ai", "aistudio.google.com", "deepmind.com"
        ];
        for (var i = 0; i < aiDomains.length; i++) {
            if (host === aiDomains[i] || host.indexOf("." + aiDomains[i]) !== -1) {
                return "PROXY 127.0.0.1:1"; // Dead-end route to completely block connection
            }
        }
        return "DIRECT"; // Let all other traffic pass normally
    }
    """
    pac_data_uri = "data:application/x-ns-proxy-autoconfig," + urllib.parse.quote(pac_script)
    options.set_preference("network.proxy.type", 2) # Type 2 enables automatic proxy configuration URL
    options.set_preference("network.proxy.autoconfig_url", pac_data_uri)
    # -----------------------------------------------

    # Download Destination and Behavior
    options.set_preference("browser.download.folderList", 2) 
    options.set_preference("browser.download.dir", pasta_downloads)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", 
                           "application/octet-stream,application/pdf,application/zip,image/jpeg,image/png,text/plain")
    options.set_preference("pdfjs.disabled", True) # Forces PDF downloads instead of opening them in-browser

    try:
        # Instantiating the driver using full explicit package namespace
        # If Firefox is missing from the OS, Selenium Manager will download it automatically now
        driver = selenium.webdriver.Firefox(options=options)
        driver.maximize_window()
        driver.get("https://search.brave.com")
        
        print("\n[!] Browser ready. Use the Firefox window normally.")
        print("[!] Close the window or use Ctrl+C in the terminal to terminate and DELETE EVERYTHING.")
        
        # Keeps the script alive while the browser window is open
        while len(driver.window_handles) > 0:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n[-] Interruption triggered by the user.")
    except Exception as e:
        print(f"\n[!] Window closed or error detected: {e}")
    finally:
        # Ensures safe closure of the driver before deletion
        print("\n[-] Requesting termination of the Firefox process...")
        try:
            driver.quit()
        except Exception:
            pass
        
        print("[-] Starting data shredding and cleanup...")
        # Gives a 1-second breather for the OS to register the end of the process
        time.sleep(1) 
        
        # Executes our robust deletion function
        forcar_exclusao_pasta(pasta_temporal)
        print("="*60)

if __name__ == "__main__":
    iniciar_navegador_privado()