# Grid the Grey — SEO & Growth Checklist

## Phase 1: Search Engine Setup (This Week)

### Google Search Console
- [ ] Add property in Google Search Console (use DNS verification)
- [ ] Verify ownership via Cloudflare DNS TXT record
- [ ] Submit `/sitemap.xml`
- [ ] Check "Coverage" tab — ensure pages are indexed
- [ ] Check "Performance" tab weekly to see which keywords you're ranking for
- [ ] Check "Mobile Usability" — fix any issues

### Bing Webmaster Tools
- [ ] Add property in Bing Webmaster Tools
- [ ] Submit sitemap
- [ ] (Bing has 20-30% search traffic in some niches)

### Site Verification
- [ ] Verify sitemap.xml works: `https://gridthegrey.com/sitemap.xml`
- [ ] Verify robots.txt works: `https://gridthegrey.com/robots.txt`
- [ ] Test with: `curl -I https://gridthegrey.com/robots.txt` (should be 200)
- [ ] Test with: `curl -I https://gridthegrey.com/sitemap.xml` (should be 200)

## Phase 2: On-Page Optimization (Week 2)

### Article Quality
- [ ] Ensure every article has:
  - [ ] Unique, descriptive title (50-60 chars)
  - [ ] Meta description (150-160 chars) — currently auto-generated from summary
  - [ ] Framework tags (MITRE ATLAS or OWASP LLM)
  - [ ] Threat level badge (CRITICAL, HIGH, MEDIUM, LOW, INFO)
  - [ ] Categories assigned
  - [ ] Relevance score ≥ 7.0 (already done by Claude API)

### Homepage Optimization
- [ ] Add homepage og:image (brand image for social sharing)
  - Path: `hugo-site/static/img/og-image.png` (1200x630px)
  - Update meta.html to include fallback: `{{ if .Params.thumbnail }}...{{ else }}{{ "img/og-image.png" | absURL }}{{ end }}`
- [ ] H1 tag should be "GRID THE GREY" (check index.html)
- [ ] Homepage description should match tagline

### Internal Linking
- [ ] Link-rich archive pages:
  - [ ] Create `/frameworks/mitre-atlas/` page listing all articles with each technique
  - [ ] Create `/frameworks/owasp-llm/` page listing all articles with each category
  - [ ] These become "pillar pages" for SEO
- [ ] Each article should link to related articles (by framework/threat level)

## Phase 3: Content Strategy (Ongoing)

### Keyword Research
- [ ] Monitor Google Search Console monthly
- [ ] Identify keywords you rank #5-15 for → optimize those posts to rank #1
- [ ] Target long-tail: "MITRE ATLAS AML.T0043 examples", "prompt injection detection"
- [ ] Track competitor sites: what are they ranking for?

### Content Gaps
- [ ] Write meta-posts about your framework mappings:
  - [ ] "How MITRE ATLAS Maps to AI Attacks: A Complete Guide"
  - [ ] "OWASP LLM Top 10: Which Vulnerabilities Matter Most"
  - [ ] These target high-intent keywords and drive backlinks

### Fresh Content Signals
- [ ] Your daily pipeline already handles this ✓
- [ ] Ensure recent articles appear on homepage
- [ ] Consider "Last Updated" badge for major updates

## Phase 4: Off-Page SEO (Week 3+)

### Community Engagement
- [ ] **Reddit**:
  - [ ] r/netsec: Share 1-2 articles/month with unique framework insights
  - [ ] r/cybersecurity: Post analysis of threats in your vertical
  - [ ] r/MachineLearning: Post when covering AI model attacks
  - Strategy: Share, don't spam. Comment genuinely on others' posts first.

- [ ] **Hacker News**:
  - [ ] Submit your highest-scoring articles (7.5+) to HN
  - [ ] Story titles should emphasize unique angle: "We mapped AI attacks to MITRE ATLAS" not just news
  - [ ] Be prepared to discuss in comments

- [ ] **LinkedIn**:
  - [ ] Post weekly: "Top AI security threat this week: [article title]"
  - [ ] Tag relevant communities: #cybersecurity #infosec #AIrisk
  - [ ] Share 3-sentence analysis + link to full article

### Backlink Strategy
- [ ] Email threat intel vendors:
  - [ ] "Hi, we've mapped your incident to MITRE ATLAS [technique]. Here's our analysis: [link]"
  - [ ] Most threat researchers appreciate framework context
  - [ ] 1-2 of these per week = legitimate backlinks

- [ ] Reach out to security blogs:
  - [ ] "Your article on [topic] fits our OWASP LLM Top 10 coverage. We've created this framework analysis: [link]"
  - [ ] Request: "Would you link to this for additional context?"

- [ ] Security conferences:
  - [ ] Monitor: DEF CON, Black Hat, RSA, USENIX Security
  - [ ] Create articles around conference talks: "DEF CON 2026: [Speaker] on AI attacks mapped to MITRE ATLAS"
  - [ ] Conference organizers often link to relevant commentary

### Newsletter Growth
- [ ] Add signup CTA in sidebar (already done ✓)
- [ ] Add signup CTA to article footer (consider: "Read the full weekly digest")
- [ ] Cross-promote in Reddit/HN posts: "We send a weekly digest of the top AI security stories, framework-mapped"
- [ ] Track: Beehiiv signup rate weekly

## Phase 5: Technical SEO (Ongoing)

### Performance
- [ ] Check PageSpeed Insights: `https://pagespeed.web.dev/`
- [ ] Target: >90 on mobile, >95 on desktop
- [ ] Hugo static site should already be fast ✓

### Crawlability
- [ ] Monitor Google Search Console "Coverage" tab
- [ ] If pages show "Excluded" → check why (noindex, robots.txt, etc.)
- [ ] Ensure no duplicate content (should be fine with custom domain + canonical URLs ✓)

### Mobile Friendliness
- [ ] Test on mobile: `https://gridthegrey.com`
- [ ] Sidebar should collapse to menu on mobile
- [ ] Text should be readable (no tiny fonts)
- [ ] Buttons should be tap-friendly (min 48px)

## Phase 6: Monitoring (Weekly)

### Metrics to Track
1. **Google Search Console**:
   - Clicks (traffic)
   - Impressions (how often you appear in results)
   - Average position (currently ranking where?)
   - Click-through rate (CTR — are snippets compelling?)

2. **Beehiiv**:
   - Newsletter subscribers
   - Open rate
   - Click rate
   - Signup source (track which articles drive signups)

3. **Site Analytics** (if using):
   - Traffic source (direct, search, referral, social)
   - Time on page (are people reading or bouncing?)
   - Bounce rate by article
   - Which articles drive newsletter signups

### Monthly Goals
- Month 1: Get indexed (500+ pages), 50+ newsletter subscribers
- Month 2: Rank for 10+ long-tail keywords, 100+ subscribers
- Month 3: 100+ monthly search visitors, 200+ subscribers

## Priority Order (Do This First)
1. ✅ Robots.txt (done)
2. Google Search Console setup & sitemap submission (THIS WEEK)
3. Verify sitemap + robots.txt work
4. Create og:image fallback
5. Start Reddit/HN posting (low effort, high impact)
6. Create pillar pages for frameworks
7. Weekly monitoring of Google Search Console

## Notes
- Your main competitive advantage: **MITRE ATLAS + OWASP mapping** — no other news site does this
- Your audience: **security researchers, threat intel teams, CISO analysts** — they find you via Google, HN, Reddit, LinkedIn
- Your growth lever: **backlinks from threat intel reports, security blogs** — show them your framework insights
- Your conversion: **newsletter signup** — all traffic should flow to newsletter signup (you're running on Beehiiv free tier)

---

**Last Updated**: April 12, 2026
**Next Review**: May 12, 2026 (check GSC performance data)
