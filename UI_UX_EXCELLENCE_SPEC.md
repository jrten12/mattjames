# UI/UX Excellence Spec (Phase 2)

This document defines the quality bar for a premium, low-friction UI across Client Portal and Founder Console.

## Product Intent

- The product should feel premium and trustworthy on first view.
- Non-technical users should complete primary tasks without assistance.
- API complexity should stay hidden from client-facing flows.

## Experience Principles

- One primary action per screen section.
- Progressive disclosure for advanced options.
- Strong visual hierarchy (title -> context -> action).
- Plain-language microcopy; avoid technical jargon.
- High-impact operations require confirmation.
- Empty, loading, success, and error states must always be explicit.

## Visual Standards

- Consistent spacing rhythm and alignment.
- Shared color tokens and semantic usage (success, warning, danger, neutral).
- Readable typography with clear hierarchy.
- Component consistency: button styles, form controls, cards, tables, badges.
- Balanced contrast and accessible interaction states.

## Client Portal Standards

- Wizard should guide users step-by-step with clear progress indicators.
- Inputs should use friendly labels and examples.
- Decision flow should prioritize confidence over speed.
- Status labels should be understandable (human-readable, not raw backend terms).
- Core outcome: submit request and review preview in minimal clicks.

## Founder Console Standards

- Data-heavy operations remain clear with obvious primary CTAs.
- Risky status and release actions include confirmation.
- Context actions should prefill downstream forms where possible.
- Operational visibility should reduce manual copy/paste of IDs.

## API Abstraction Requirement

- Clients should not need direct knowledge of API structure.
- UI must map user intents to backend calls transparently.
- Technical identifiers should be selected from UI context where possible.

## Quality Gate (Definition of Done)

A UI iteration ships only if:

- A first-time non-technical user can complete core flow without external help.
- Primary action on each panel is visually obvious.
- No section appears unfinished or utility-only.
- Confirmation, error, and success states are clear.
- Tests for shell rendering still pass after layout changes.

## Iteration Plan

1. Apply design tokens and layout framework.
2. Refactor high-use surfaces first (`/portal`, then `/founder`).
3. Add interaction polish and microcopy pass.
4. Validate usability with full journey walkthrough.
