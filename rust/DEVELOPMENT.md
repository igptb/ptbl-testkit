# Rust dev workflow

This folder is the Rust-side validator migration workspace.

## One-time setup

If you installed Rust via rustup, you can add formatter and linter components:

```powershell
rustup component add rustfmt clippy
```

## Build and test

From repo root:

```powershell
cd rust
cargo build
cargo test
```

## Formatting

Check formatting (CI-style):

```powershell
cd rust
cargo fmt --all -- --check
```

Auto-format (writes changes):

```powershell
cd rust
cargo fmt --all
```

## Linting

Run clippy with warnings treated as errors:

```powershell
cd rust
cargo clippy --workspace --all-targets --all-features -- -D warnings
```

## Convenience aliases

If you are inside `rust/`, you can also run:

```powershell
cargo fmt-check
cargo lint
cargo test-all
cargo build-all
```

These are defined in `rust/.cargo/config.toml`.
