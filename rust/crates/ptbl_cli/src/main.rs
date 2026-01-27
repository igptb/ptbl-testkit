//! PTBL CLI (Rust) - scaffold only.

fn main() {
    let v = ptbl_validator::version_info();
    println!("{}", v.name);
    println!("(cli scaffold) Next: implement `validate` subcommand and JSON output parity gates.");
}
