# Dr. Sanket Mishra — Academic Portfolio

Academic portfolio website powered by the [al-folio](https://github.com/alshedivat/al-folio) Jekyll theme (same template as [matouse.github.io](https://matouse.github.io/)).

**Live site:** https://sanket-mishrax.github.io/sanketmishra.github.io/

## Pages

- **Home** — Bio, selected publications, social links
- **Publications** — BibTeX-driven list with expandable summaries (click **Abs**)
- **Research** — Research areas and impact metrics
- **Teaching** — Subjects taught and course materials placeholders
- **Experience** — Positions and education
- **Collaborations** — Co-author network
- **Administration** — Academic service

## Updating Content

| File | Purpose |
|------|---------|
| `_pages/about.md` | Homepage bio |
| `_bibliography/papers.bib` | Publications (with `abstract` field for summaries) |
| `_data/subjects.yml` | Courses taught |
| `_data/teaching_materials.yml` | Course materials (upload files to `assets/materials/`) |
| `_config.yml` | Site settings, social links, scholar ID |

## Local Development

```bash
bundle install
bundle exec jekyll serve
```

Visit http://localhost:4000
