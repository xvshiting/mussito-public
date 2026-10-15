# Mussito public publishing repository

- This repository is public. It contains only the website, public support documentation, approved brand assets, and release metadata. Product source and private development records belong elsewhere.
- Distribute signed/notarized Mac binaries through GitHub Releases, not Git source control.
- Publish accurate availability. Do not invent App Store URLs, released versions, pricing, testimonials, or download links.
- Edit page content in `content/` and the shared template in `site/layout.html`, then rebuild `docs/` with `conda run -n kora python scripts/build_site.py`.
- Run local validation with `conda run -n kora python scripts/check_site.py`. The production site is served from `main:/docs` by GitHub Pages.
