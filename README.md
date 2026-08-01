# sanketmishra.github.io

Academic portfolio website for **Dr. Sanket Mishra** — Associate Professor at MIT Bengaluru, MAHE.

Live site: [https://sanketmishra.github.io](https://sanketmishra.github.io)

## Sections

- **Home** — Overview and recent highlights
- **Research** — Research areas and impact metrics
- **Publications** — Peer-reviewed papers from [Google Scholar](https://scholar.google.com/citations?user=LkngaM4AAAAJ)
- **Collaborations** — Co-author network
- **Experience** — Current and past positions, education
- **Institutes** — Academic affiliations timeline
- **Administration** — Administrative roles and academic service
- **About** — Biography and contact

## Updating Content

Content is managed through YAML data files in `_data/`:

| File | Contents |
|------|----------|
| `_data/publications.yml` | Publications list |
| `_data/collaborators.yml` | Research collaborators |
| `_data/institutes.yml` | Institute affiliations |
| `_data/experience.yml` | Work experience and education |
| `_data/admin.yml` | Administrative roles |
| `_data/subjects.yml` | Courses and subjects taught |
| `_data/teaching_materials.yml` | Lecture slides, notes, assignments (upload files to `assets/materials/`) |

Update `_config.yml` for site-wide settings and Google Scholar citation metrics.

## Local Development

```bash
bundle install
bundle exec jekyll serve
```

Visit `http://localhost:4000`

## Built With

- [Jekyll](https://jekyllrb.com/)
- [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) theme
