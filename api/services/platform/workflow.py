from api.models.platform import ProjectState


ALLOWED_TRANSITIONS: dict[ProjectState, set[ProjectState]] = {
    ProjectState.intake: {ProjectState.discovery_active, ProjectState.paused, ProjectState.closed},
    ProjectState.discovery_active: {
        ProjectState.sow_drafting,
        ProjectState.intake,
        ProjectState.paused,
        ProjectState.closed,
    },
    ProjectState.sow_drafting: {
        ProjectState.sow_review,
        ProjectState.discovery_active,
        ProjectState.paused,
        ProjectState.closed,
    },
    ProjectState.sow_review: {
        ProjectState.build_in_progress,
        ProjectState.sow_drafting,
        ProjectState.discovery_active,
        ProjectState.paused,
        ProjectState.closed,
    },
    ProjectState.build_in_progress: {
        ProjectState.pilot_live,
        ProjectState.discovery_active,
        ProjectState.sow_drafting,
        ProjectState.paused,
        ProjectState.closed,
    },
    ProjectState.pilot_live: {
        ProjectState.production_live,
        ProjectState.build_in_progress,
        ProjectState.discovery_active,
        ProjectState.paused,
        ProjectState.closed,
    },
    ProjectState.production_live: {ProjectState.expansion, ProjectState.paused, ProjectState.closed},
    ProjectState.expansion: {
        ProjectState.build_in_progress,
        ProjectState.discovery_active,
        ProjectState.production_live,
        ProjectState.paused,
        ProjectState.closed,
    },
    ProjectState.paused: {
        ProjectState.discovery_active,
        ProjectState.sow_drafting,
        ProjectState.build_in_progress,
        ProjectState.production_live,
        ProjectState.expansion,
        ProjectState.closed,
    },
    ProjectState.closed: set(),
}


def transition_allowed(current: ProjectState, next_state: ProjectState) -> bool:
    if current == next_state:
        return False
    return next_state in ALLOWED_TRANSITIONS[current]
