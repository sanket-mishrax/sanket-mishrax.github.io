# GitHub Pages setup

## Your site URL

Because your GitHub username is **sanket-mishrax** (not `sanketmishra`), the site is published at:

**https://sanket-mishrax.github.io/sanketmishra.github.io/**

The URL `sanketmishra.github.io` only works if you log in to the GitHub account named `sanketmishra` and host the repo there.

## Fix Pages settings (one-time)

1. Go to **Settings → Pages** in this repository
2. Under **Build and deployment**:
   - Set **Source** to **GitHub Actions** (recommended), OR
   - Set **Branch** to `master` and folder to `/ (root)`
3. Save and wait 2–5 minutes for the site to rebuild

## Local preview

```bash
bundle install
bundle exec jekyll serve
```

Visit http://localhost:4000
