# Planned GitHub Issues

Create these issues to track future development work.

## Phase 2: Questionnaire & Scoring

- [ ] Seed all governance questions across 9 categories
- [ ] Implement deterministic scoring engine with unit tests
- [ ] Build FastAPI CRUD endpoints for assessments
- [ ] Create frontend assessment workflow (profile → questions → submit)
- [ ] Handle "Not applicable" responses correctly in scoring

## Phase 3: Results Dashboard

- [ ] Overall score gauge and readiness level display
- [ ] Category radar chart and horizontal bar charts
- [ ] AI system risk badge (separate from readiness)
- [ ] Category drill-down with score explainability
- [ ] Responsive, accessible chart components

## Phase 4: Recommendation Engine

- [ ] Define recommendation rules per question/category
- [ ] Priority classification (Critical, High, Medium, Low)
- [ ] Improvement roadmap generation (0–30, 31–90, 3–6, 6–12 months)
- [ ] Unit tests for all recommendation rules

## Phase 5: Risk Matrix

- [ ] AI system risk profile calculation from profile flags
- [ ] 5×5 risk matrix UI
- [ ] Governance gap calculation
- [ ] Risk matrix visualization on dashboard

## Phase 6: PDF Reporting

- [ ] Professional PDF template (cover, executive summary, methodology)
- [ ] Server-side PDF generation
- [ ] Report download endpoint
- [ ] Report includes all 16 required sections

## Phase 7: Optional LLM

- [ ] Executive summary generation (clearly labeled as AI-generated)
- [ ] Plain-language recommendation rewriting
- [ ] Explicit user opt-in before sending data to LLM
- [ ] Never use LLM for numerical scores

## Phase 8: Quality & Security

- [ ] Full keyboard navigation and ARIA labels
- [ ] Screen-reader-friendly chart alternatives
- [ ] Input validation and error handling
- [ ] Assessment delete functionality
- [ ] Security audit of API endpoints

## Phase 9: Demo Mode

- [ ] Northstar College demo assessment
- [ ] Student Success Risk Prediction System scenario
- [ ] Intentional governance gaps for demonstration

## Phase 10: Production

- [ ] Architecture diagram in README
- [ ] Screenshots and deployment configuration
- [ ] PostgreSQL migration guide
- [ ] CI/CD pipeline

## Enhancements (Post-MVP)

- [ ] Multi-user authentication
- [ ] Assessment history and comparison
- [ ] Custom question sets per industry
- [ ] Internationalization
- [ ] Export to CSV/JSON
