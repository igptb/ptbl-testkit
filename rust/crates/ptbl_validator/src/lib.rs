//! PTBL validator (Rust) - scaffold only.
//!
//! This crate will progressively implement the Phase 2 validator behavior.
//! Keep the public API small and stable because PTB will embed this later.

use serde::{Deserialize, Serialize};

/// Placeholder type so the crate is non-empty and compiles.
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VersionInfo {
    pub name: String,
}

/// Placeholder function.
pub fn version_info() -> VersionInfo {
    VersionInfo {
        name: "ptbl_validator scaffold".to_string(),
    }
}
