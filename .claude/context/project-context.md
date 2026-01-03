# Kris Krug Project Context

> Building a Responsible & Inclusive AI Future for British Columbia

## Mission & Values

### Core Mission
Kris Krug is a grassroots ecosystem initiative dedicated to building a responsible and inclusive AI future for British Columbia. We bring together diverse voices—from AI enthusiasts and professionals to policy makers, educators, artists, and community organizers.

### Core Values

**1. Community First**
- Grassroots, bottom-up approach
- Regional hubs and hyperlocal engagement
- Inclusive and welcoming to all
- Collaborative rather than competitive

**2. Responsible AI**
- Transparency and explainability
- Privacy and data protection
- Ethical considerations paramount
- Question technology that may harm or exclude

**3. Inclusivity & Accessibility**
- WCAG 2.1 AA compliance is mandatory, not optional
- Multiple ways to participate (events, online, resources)
- Consider diverse abilities, backgrounds, and contexts
- Welcoming to newcomers and experts alike

**4. Regional Focus**
- British Columbia context matters
- Canadian spelling and sensibilities
- Local hubs and regional engagement
- Supporting BC's unique AI ecosystem

**5. Knowledge Sharing**
- Open resources and documentation
- Educational approach
- Share learnings broadly
- Build collective intelligence

## Target Audience

### Primary Users
- **AI Enthusiasts** - People curious about AI and its applications
- **Professionals** - Those working in AI/ML fields
- **Community Organizers** - People building local AI communities
- **Policy Makers** - Government and institutional decision makers
- **Educators** - Teachers and trainers
- **Artists & Creatives** - Exploring AI in creative work

### User Needs
- Stay informed about AI developments
- Connect with like-minded people
- Find events and learning opportunities
- Access resources (funding, tools, guides)
- Contribute to responsible AI discourse
- Participate in specialized communities (AI Film Club, Mind/AI/Consciousness)

### Technical Context
- **Diverse technical literacy** - From non-technical to expert developers
- **Mobile-heavy usage** - Many users on phones, some on slower connections
- **Accessibility needs** - Screen readers, keyboard navigation, etc.
- **Geographic distribution** - Across British Columbia, some remote areas

## Content Strategy

### Voice & Tone
- **Friendly but professional** - Approachable, not stuffy
- **Educational** - Explain the "why", not just the "what"
- **Inclusive** - Welcoming language, avoid jargon or explain it
- **Optimistic** - Positive about AI's potential while acknowledging challenges
- **Community-oriented** - "We" not "I", collective rather than individual

### Key Messages
- AI can be built responsibly and inclusively
- Community input shapes BC's AI future
- Grassroots movements matter
- Everyone has a role in shaping AI
- British Columbia is building something special

## Design Principles

### Accessibility First
- Not just WCAG compliance, but genuinely usable by all
- Keyboard navigation throughout
- Screen reader friendly
- High contrast, readable fonts
- Multiple ways to accomplish tasks

### Performance Matters
- Mobile-first approach
- Fast loading (< 3 seconds)
- Optimized for slower connections
- Minimal JavaScript where possible
- Progressive enhancement

### Content Before Chrome
- Content is king
- Navigation is simple and clear
- Features serve content, not the other way around
- Avoid unnecessary complexity

### Community Personality
- Visual warmth (not cold corporate)
- Use of appropriate imagery
- Celebration of diversity
- BC regional identity (mountains, nature metaphors appropriate)

## Key Initiatives

### Regional Hubs
Hyperlocal approach to building AI community across BC regions.

### AI Film Club
Exploring AI through cinema and media.

### Mind/AI/Consciousness
Philosophical discussions about AI and consciousness.

### Events & Workshops
Regular community gatherings, both online and in-person.

### Resource Directory
Curated resources for funding, tools, hackathons, and learning.

## External Integrations

### Notion (Content Management)
- News updates and editorial content
- Content sync to WordPress
- Potential single-point-of-failure

### Luma (Events)
- Event listings and RSVPs
- External platform dependency
- Consider eventual consolidation

## Technical Constraints

### Current Known Issues (from audit)
1. Contact form (Gravity Forms #3) not functional
2. WCAG 2.1 AA compliance gaps
3. Meta descriptions truncated
4. Performance issues (JavaScript, assets)
5. Navigation UX clarity issues
6. External link dependencies
7. Authentication flow undocumented

### Performance Baselines (to improve)
- Current page load: Unknown, needs measurement
- Target: < 3 seconds on 3G
- Core Web Vitals: Need to meet Google standards

### Browser Support
- Modern browsers (last 2 versions)
- Mobile Safari (iOS users)
- Chrome on Android
- Desktop: Chrome, Firefox, Safari
- Graceful degradation for older browsers

## Development Priorities

### Must Have
1. Accessibility (WCAG 2.1 AA)
2. Security (WordPress hardening)
3. Performance (mobile-first)
4. Functionality (core features work)

### Should Have
1. SEO optimization
2. Analytics and insights
3. Content freshness
4. Community features

### Nice to Have
1. Advanced features
2. Experimental AI integrations
3. Polish and refinement

## Success Metrics

### Community Impact
- Event attendance and engagement
- Resource usage and downloads
- Community member growth
- Geographic reach across BC

### Technical Quality
- WCAG 2.1 AA compliance: 100%
- Core Web Vitals: All green
- Uptime: > 99.5%
- Zero critical security issues

### User Experience
- Contact form completion rate
- Event registration rate
- Time on site
- Return visitor rate

## Canadian Context

### Spelling & Language
- Use Canadian spelling (colour, honour, centre, etc.)
- Bilingual considerations (English/French where appropriate)
- Indigenous acknowledgment and respect
- BC-specific terminology and references

### Regional Considerations
- BC's diverse geography (urban Vancouver, rural communities, northern regions)
- Time zones (PST/PDT)
- Local AI companies and institutions
- BC government and policy context

## WordPress Philosophy Alignment

### "Decisions, Not Options"
- Keep interface simple
- Don't overwhelm users with choices
- Make good defaults
- Progressive disclosure of complexity

### Democratizing Publishing
- Easy for non-technical users to manage
- Empower community members to contribute
- Lower barrier to participation

### Performance & Accessibility
- Core WordPress values that align with Kris Krug
- Not negotiable, baked into everything

## Agent Guidance

When making decisions as an AI agent for Kris Krug:

**Ask yourself:**
- Does this serve the community?
- Is it accessible to all?
- Does it align with responsible AI principles?
- Would someone in rural BC be able to use this on their phone?
- Are we being inclusive?
- Does this reflect Kris Krug's grassroots spirit?

**Prioritize:**
1. Accessibility over features
2. Simplicity over complexity
3. Community benefit over technical coolness
4. Security and privacy over convenience
5. Performance for all over perfect for some

**Remember:**
- This is for a community organization, not a corporation
- Every code decision affects real people trying to participate in BC's AI future
- Clean, well-documented code welcomes future contributors
- Tests protect the community from bugs
- Security protects people's privacy and trust

---

**This is not just a website. It's a platform for building BC's inclusive AI future. Code accordingly.**
