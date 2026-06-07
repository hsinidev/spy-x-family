
import os
import re

BASE_DIR = r"c:\Users\hsini\Desktop\website manga projects\Spy X Family"

TEMPLATE = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Spy X Family</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Public+Sans:ital,wght@0,100..900;1,100..900&family=Special+Elite&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="index.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <script src="script.js" defer></script>
</head>
<body class="bg-[#050505] text-[#fef3c7] font-sans selection:bg-[#991b1b] selection:text-white antialiased custom-scrollbar">
    <!-- TOP-SECRET STAMP -->
    <div class="fixed top-12 right-12 opacity-10 transform rotate-12 pointer-events-none select-none z-0">
        <div class="border-8 border-[#991b1b] px-8 py-4 rounded-xl">
            <h1 class="text-8xl font-black text-[#991b1b] special-elite">CONFIDENTIAL</h1>
        </div>
    </div>

    <!-- NAVIGATION BAR Placeholder (will be replaced by standardize_site.py) -->
    <nav class="fixed w-full z-[100] bg-[#050505]/90 backdrop-blur-2xl border-b border-[#064e3b]/30">
        <div class="max-w-[2000px] mx-auto px-8 h-24 flex items-center justify-between">
            <a href="./index.html" class="text-3xl font-['DM_Serif_Display'] logo-glow">SPY x FAMILY</a>
        </div>
    </nav>

    <main class="relative pt-40 pb-24 px-6 z-10">
        <div class="max-w-4xl mx-auto">
            <!-- HEADER -->
            <div class="mb-16 border-l-4 border-[#064e3b] pl-8">
                <p class="text-[#064e3b] uppercase tracking-[0.4em] font-bold mb-2">Subject: {subject}</p>
                <h1 class="text-5xl md:text-7xl font-bold mb-4 special-elite tracking-tighter uppercase">{title}</h1>
                <div class="flex items-center space-x-4 text-sm opacity-60">
                    <span>DOCUMENT ID: {doc_id}</span>
                    <span class="w-1 h-1 bg-[#fef3c7] rounded-full"></span>
                    <span>LAST UPDATED: 16 APRIL 2024</span>
                </div>
            </div>

            <!-- CONTENT -->
            <div class="space-y-12 prose prose-invert prose-amber max-w-none">
                {content}
                
                <section class="pt-8 border-t border-[#064e3b]/20">
                    <h2 class="text-2xl font-bold mb-4 special-elite text-[#064e3b]">CONTACT COMMAND</h2>
                    <p class="mb-6 opacity-80">For inquiries regarding transmission errors or mission parameters, reach out via the secure channel:</p>
                    <a href="mailto:admin@spyxfamily.portal" class="inline-flex items-center px-8 py-3 bg-[#064e3b] text-[#fef3c7] font-bold rounded-lg hover:bg-[#064e3b]/80 transition-all transform hover:scale-105">
                        <i data-lucide="mail" class="w-4 h-4 mr-2"></i>
                        MISSION SUPPORT
                    </a>
                </section>
            </div>
        </div>
    </main>

    <footer class="bg-black py-24"></footer>
    <nav class="mobile-app-shell"></nav>

    <script>
        lucide.createIcons();
    </script>
</body>
</html>
"""

PAGES = {
    "about.html": {
        "title": "About WISE Agency",
        "subject": "Mission Briefing",
        "doc_id": "WISE-AB-001",
        "content": """
                <section class="bg-[#e1c699]/5 p-8 border border-[#e1c699]/10 rounded-2xl relative overflow-hidden group">
                    <h2 class="text-2xl font-bold mb-4 text-[#e1c699] special-elite flex items-center">
                        <i data-lucide="shield" class="w-6 h-6 mr-3 text-[#064e3b]"></i>
                        OUR MISSION
                    </h2>
                    <p class="leading-relaxed opacity-80">
                        Westalis Intelligence Services' Eastern-Focused Division (WISE) is dedicated to maintaining the fragile peace between Westalis and Ostania. Our primary objective is Operation Strix: the infiltration of the prestigious Eden Academy to monitor the movements of Donovan Desmond.
                    </p>
                </section>
                <section>
                    <h2 class="text-2xl font-bold mb-6 special-elite flex items-center">
                        <i data-lucide="users" class="w-6 h-6 mr-3 text-[#064e3b]"></i>
                        THE TEAM
                    </h2>
                    <p class="leading-relaxed opacity-80">
                        This portal provides encrypted access to the mission logs of Agent Twilight and his unconventional 'family'. While our records are classified, we provide public intelligence summaries for educational purposes, ensuring the citizens of Berlint remain informed about the ongoing peace efforts.
                    </p>
                </section>
        """
    },
    "privacy.html": {
        "title": "Privacy Protocol",
        "subject": "Data Redaction",
        "doc_id": "WISE-PP-082",
        "content": """
                <section class="bg-[#e1c699]/5 p-8 border border-[#e1c699]/10 rounded-2xl relative overflow-hidden group">
                    <h2 class="text-2xl font-bold mb-4 text-[#e1c699] special-elite flex items-center">
                        <i data-lucide="lock" class="w-6 h-6 mr-3 text-[#064e3b]"></i>
                        ENCRYPTION STANDARDS
                    </h2>
                    <p class="leading-relaxed opacity-80">
                        Your interaction with this intelligence portal is protected by AES-256-GCM encryption. We do not store any identifiable bio-data of our readers. Any metadata collected is purely for mission performance optimization and is purged every 24 operational hours.
                    </p>
                </section>
                <section>
                    <h2 class="text-2xl font-bold mb-6 special-elite flex items-center">
                        <i data-lucide="eye-off" class="w-6 h-6 mr-3 text-[#064e3b]"></i>
                        AGENT ANONYMITY
                    </h2>
                    <p class="leading-relaxed opacity-80">
                        In accordance with the WISE Privacy Directives, we ensure that no tracking mechanisms are utilized beyond the necessary operation of the manga reading interface. Your progress is stored locally in your browser's encrypted storage and is never transmitted to Ostanian surveillance servers.
                    </p>
                </section>
        """
    },
    "contact.html": {
        "title": "Contact Command",
        "subject": "Secure Channel",
        "doc_id": "WISE-CC-999",
        "content": """
                <section class="bg-[#e1c699]/5 p-8 border border-[#e1c699]/10 rounded-2xl relative overflow-hidden group">
                    <h2 class="text-2xl font-bold mb-4 text-[#e1c699] special-elite flex items-center">
                        <i data-lucide="send" class="w-6 h-6 mr-3 text-[#064e3b]"></i>
                        SIGNAL INTERCEPT
                    </h2>
                    <p class="leading-relaxed opacity-80">
                        Need to report a bug in the mission logs? Or perhaps you've discovered a typo in the intelligence reports? Use the secure channel below to reach the WISE support desk. Responses are typically returned within one business week, unless the agent is currently deep undercover.
                    </p>
                </section>
        """
    },
    "cookies.html": {
        "title": "Cookies Directive",
        "subject": "Tracker Protocol",
        "doc_id": "WISE-CD-404",
        "content": """
                <section class="bg-[#e1c699]/5 p-8 border border-[#e1c699]/10 rounded-2xl relative overflow-hidden group">
                    <h2 class="text-2xl font-bold mb-4 text-[#e1c699] special-elite flex items-center">
                        <i data-lucide="cookie" class="w-6 h-6 mr-3 text-[#064e3b]"></i>
                        TRACKER USAGE
                    </h2>
                    <p class="leading-relaxed opacity-80">
                        Our "cookies" are actually small tactical trackers used to remember your position in the manga mission archives. They allow the portal to show you which missions you have already completed. No third-party surveillance cookies are permitted within this secure zone.
                    </p>
                </section>
        """
    },
    "dmca.html": {
        "title": "DMCA Protocol",
        "subject": "Copyright Redaction",
        "doc_id": "WISE-DM-777",
        "content": """
                <section class="bg-[#e1c699]/5 p-8 border border-[#e1c699]/10 rounded-2xl relative overflow-hidden group">
                    <h2 class="text-2xl font-bold mb-4 text-[#e1c699] special-elite flex items-center">
                        <i data-lucide="alert-triangle" class="w-6 h-6 mr-3 text-[#991b1b]"></i>
                        REDACTION REQUEST
                    </h2>
                    <p class="leading-relaxed opacity-80">
                        We respect the intellectual property of all creators. If you believe any mission log on this portal violates your copyright, please submit a formal redaction request. Since our physical headquarters is technically classified, all DMCA notices must be sent via the mission support channel.
                    </p>
                </section>
        """
    },
    "disclaimer.html": {
        "title": "Legal Disclaimer",
        "subject": "Operational Risk",
        "doc_id": "WISE-LD-000",
        "content": """
                <section class="bg-[#e1c699]/5 p-8 border border-[#e1c699]/10 rounded-2xl relative overflow-hidden group">
                    <h2 class="text-2xl font-bold mb-4 text-[#e1c699] special-elite flex items-center">
                        <i data-lucide="info" class="w-6 h-6 mr-3 text-[#064e3b]"></i>
                        FOR INFORMATIONAL USE ONLY
                    </h2>
                    <p class="leading-relaxed opacity-80">
                        The content on this site is for entertainment and educational purposes only. WISE does not guarantee the success of any real-world espionage operations based on the tactics displayed in these mission logs. Use of Forger family techniques (telepathy, assassination, or elite spy skills) is at your own risk.
                    </p>
                </section>
        """
    },
    "terms.html": {
        "title": "Terms of Deployment",
        "subject": "Rules of Engagement",
        "doc_id": "WISE-TD-123",
        "content": """
                <section class="bg-[#e1c699]/5 p-8 border border-[#e1c699]/10 rounded-2xl relative overflow-hidden group">
                    <h2 class="text-2xl font-bold mb-4 text-[#e1c699] special-elite flex items-center">
                        <i data-lucide="file-text" class="w-6 h-6 mr-3 text-[#064e3b]"></i>
                        USER AGREEMENT
                    </h2>
                    <p class="leading-relaxed opacity-80">
                        By entering this portal, you agree to become an auxiliary reader-agent. You must not attempt to breach the secure firewall, scrape the mission archives using non-sanctioned bots, or disrupt the peaceful reading experience of other agents in the sector.
                    </p>
                </section>
        """
    }
}

for filename, data in PAGES.items():
    path = os.path.join(BASE_DIR, filename)
    print(f"Generating {filename}...")
    content = TEMPLATE.format(**data)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("All legal pages generated. Now run standardize_site.py to inject components.")
