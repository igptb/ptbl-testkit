class ResolverError(RuntimeError):
    def __init__(self, rule_id: str, message: str):
        super().__init__(f'{rule_id}: {message}')
        self.rule_id = rule_id


# Phase 1 minimal rule IDs
RESOLVE_LOCK_MISSING = 'RESOLVE_LOCK_MISSING'
RESOLVE_UNRESOLVED_IMPORT = 'RESOLVE_UNRESOLVED_IMPORT'
RESOLVE_CYCLE = 'RESOLVE_CYCLE'
RESOLVE_CONFLICT = 'RESOLVE_CONFLICT'
RESOLVE_PATH_TRAVERSAL = 'RESOLVE_PATH_TRAVERSAL'
RESOLVE_SOURCE_UNSUPPORTED = 'RESOLVE_SOURCE_UNSUPPORTED'
