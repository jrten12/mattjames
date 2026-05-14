# Platform Execution Checklist

Use this as the single source of truth for execution order.

- [ ] 1) Lock roles and boundaries (Founder Console vs Client Portal)
- [x] 2) Add Intake Request backend model
- [x] 3) Build Client Portal: New Request flow
- [x] 4) Build Founder Console: Intake Queue
- [x] 5) Add Preview Build model
- [x] 6) Build Client Preview Review screen
- [x] 7) Add Approval Decision backend flow
- [ ] 8) Build Founder Console: Preview & Approval panel
- [ ] 9) Add Release orchestration endpoints
- [ ] 10) Build Founder Console: Releases panel
- [ ] 11) Add client environment registry
- [ ] 12) Connect metering policy controls
- [ ] 13) Harden UX for non-programmers
- [ ] 14) Run full demo journey (intake -> build -> preview -> approval -> deploy)
- [ ] 15) Freeze v1 operating flow documentation

## Notes

- Mark each step complete only after both backend behavior and UI behavior are validated.
- Keep clients out of backend controls; clients only use Intake + Preview + Approval flows.
