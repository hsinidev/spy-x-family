# Spy x Family: "Operation Strix" Master Deployment Protocol

This document serves as the authoritative blueprint for building a high-performance, SEO-dominant, and GEO-targeted manga portal for **Spy x Family** at `https://readspyxfamily.org/`.

## 1. Project Core Configuration

* **Manga Name:** Spy x Family
* **Website Name:** Spy x Family Online
* **Domain:** `https://readspyxfamily.org/`
* **Google Tag ID:** `G-NXKN3VT9XD`
* **Visual Style:** Cold War Dossier / Mid-Century Modern Minimalist

## 2. Antigravity Skill Orchestration

Utilize the following skills from `C:\Users\hsini\.gemini\antigravity\skills` to automate the build:

| **Skill ID**            | **Primary Function**                                                     |
| ----------------------------- | ------------------------------------------------------------------------------ |
| `antigravity-design-expert` | Implementation of "Dossier" card system and glassmorphism UI.                  |
| `ui-ux-pro-max`             | Advanced layout correction (filling the "Dead Zone") and kinetic interactions. |
| `performance-optimizer`     | AVIF encoding, lazy-loading, and Intersection Observer logic.                  |
| `seo-programmatic`          | Automated generation of unique chapter analyses for 100+ chapters.             |
| `seo-geo`                   | Localization for US, FR, JP, BR, and ID markets.                               |
| `progressive-web-app`       | Conversion to a mobile-first "Spy Tool" standalone app experience.             |
| `3d-web-experience`         | Integration of GLB/GLTF floating assets and CSS-perspective transforms.        |

## 3. Visual & UI/UX Directives

### A. The "Intelligence Archive" Layout

* **Hero Section:** Centered cinematic composition using **Nano Banana 2** generated character art.
* **Grid System:** Use Tailwind CSS 4.1 to build a responsive grid. No more empty black space.
  * `grid-template-columns: repeat(auto-fill, minmax(320px, 1fr))`
* **Dossier Cards:** Chapters are styled as manila folders.
  * **Hover Effect:** Folders "open" slightly using `rotateY` 3D transforms to reveal a high-quality manga panel.
  * **Typography:** DM Serif Display for headers; Special Elite (Typewriter) for mission numbers.

### B. Navigation & Interaction

* **Persistent Search Dropdown:** A top-nav searchable dropdown titled `MISSION_LOG` present on the home page and all 200+ chapter pages. Must allow "Filter by Arc" and "Direct Search."
* **Dual-Entry Engagement (Home Page):**
  1. **[INITIATE_MISSION_001]** : Primary button to start from the very first chapter.
  2. **[ACCESS_LATEST_INTEL]** : Secondary button to jump straight to the newest release.
* **Stella Star Progress:** A custom vertical scrollbar featuring a glowing Stella Star that moves as the reader progresses.

### C. Mobile-First & Immersive Reader

* **Full-Screen Reader:** On chapter pages, images must use `object-fit: contain` and span the full width/height of the viewport for a 100% immersive experience.
* **App Shell:** Bottom-bar navigation on mobile for one-handed operation (Home, Chapters, Favorites, Settings).

## 4. Footer & Legal Infrastructure

A comprehensive "Classified" footer must be present on every page with the following dedicated links:

* **Primary Links:** About Us, Contact, Privacy Policy.
* **Compliance:** DMCA, Terms of Service, Cookies Policy, Disclaimer.
* **Style:** Use "Redacted" black bars that reveal text on hover/tap.

## 5. SEO & GEO Performance Protocol

### A. GEO-Targeting (Global Reach)

* **Target Regions:** US, France, Japan, Brazil, Indonesia.
* **Hreflang Logic:** Auto-inject `<link rel="alternate" hreflang="...">` for each region.
* **Localized Meta:** Use region-specific slang (e.g., "Scan VF" for France).

### B. Generative Engine Optimization (GEO)

* **AI Summary Node:** Every chapter page must include a 150-word "Executive Summary" in a `<blockquote>` for AI search crawlers.
* **Tactical Reports:** 1,500 words per chapter page covering lore and character spycraft analysis.
* **JSON-LD Schema:** Comprehensive `ComicSeries` and `BreadcrumbList` markup.

## 6. Technical Stack & Performance

* **Image Pipeline:** 100% AVIF format. Panels converted via `python-performance-optimization`.
* **Reader Logic:** "Gapless" vertical scrolling with zero white lines between slices.
* **PWA Transformation:** `display: standalone` in `manifest.json` with offline-first caching for subway/dead-zone reading.




### 7. Generative Engine Optimization (GEO) & API Configuration

For full-scale content generation (1500+ word articles per page), use the following high-performance model and rotated keys:

* **Endpoint:** `https://ollama.com/api/generate`
* **Model:** `gpt-oss:120b`
* **Key Rotation Cluster:**
  1. `[REDACTED_API_KEY]`
  2. `[REDACTED_API_KEY]`
  3. `[REDACTED_API_KEY]`
  4. `[REDACTED_API_KEY]`
  5. `[REDACTED_API_KEY]`
  6. `[REDACTED_API_KEY]`
  7. `[REDACTED_API_KEY]`
  8. `[REDACTED_API_KEY]`
  9. `[REDACTED_API_KEY]`
  10. `[REDACTED_API_KEY]`
  11. `[REDACTED_API_KEY]`
  12. `[REDACTED_API_KEY]`
  13. `[REDACTED_API_KEY]`
  14. `[REDACTED_API_KEY]`
  15. `[REDACTED_API_KEY]`
  16. `[REDACTED_API_KEY]`
* **Output Directive:** Generate deep tactical reports and character psychological profiles to anchor long-form organic traffic and AI search snippets.

## 8. Execution Prompt for Antigraviter IDE

> "Execute **Operation Strix Build Protocol** for `readspyxfamily.org`.
>
> 1. Load folder structure and initiate **Tailwind CSS 4.1** Grid layout (Full Width).
> 2. Build the **Searchable MISSION_LOG Dropdown** for all pages.
> 3. Implement **Dual-Button Entry** (First Chapter vs Latest Chapter) in the Hero section.
> 4. Ensure **Chapter Images are Full-Screen** and optimized for mobile touch.
> 5. Generate the **7-Link Classified Footer** (About, Contact, Privacy, DMCA, Terms, Cookies, Disclaimer).
> 6. Trigger the **SEO/GEO** engine for localized metadata and AI summary nodes."
>
>    7.
>
>    1. Use **gpt-oss:120b** with the provided 16-key rotation to generate 1500-word SEO articles for home and all 200+ chapters.
>    2. Build the **Searchable MISSION_LOG Dropdown** for all pages.
>    3. Implement **Dual-Button Entry** (First Chapter vs Latest Chapter) in the Hero section.
>    4. Ensure **Chapter Images are Full-Screen** and optimized for mobile touch.
>    5. Generate the **7-Link Classified Footer** with redacted styles."
