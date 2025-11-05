import argparse, getpass
from pathlib import Path
from .core.encryption import encrypt_file, decrypt_file, _load_or_create_master_key
from .core.whitelist import add_device, get_devices, is_allowed
from .core.totp import init_secret, verify as totp_verify
from .core.tamper import build_manifest, verify_manifest

def main():
    ap = argparse.ArgumentParser(prog="azicure", description="Azicure security CLI")
    sp = ap.add_subparsers(dest="cmd")

    sp.add_parser("keygen", help="Generate/ensure master key exists")

    p_dev = sp.add_parser("device", help="Manage device whitelist")
    spd = p_dev.add_subparsers(dest="dev_cmd")
    p_dev_add = spd.add_parser("add")
    p_dev_add.add_argument("--id", required=True)

    p_totp = sp.add_parser("totp", help="TOTP utilities")
    spt = p_totp.add_subparsers(dest="totp_cmd")
    p_totp_init = spt.add_parser("init")
    p_totp_init.add_argument("--account", required=False, default=getpass.getuser())
    p_totp_verify = spt.add_parser("verify")
    p_totp_verify.add_argument("--secret", required=True)
    p_totp_verify.add_argument("--token", required=True)

    p_enc = sp.add_parser("encrypt")
    p_enc.add_argument("src")
    p_enc.add_argument("dst")
    p_enc.add_argument("--aad", default="")

    p_dec = sp.add_parser("decrypt")
    p_dec.add_argument("src")
    p_dec.add_argument("dst")
    p_dec.add_argument("--aad", default="")

    p_tamp = sp.add_parser("tamper", help="Build or verify manifest")
    spta = p_tamp.add_subparsers(dest="tamper_cmd")
    p_tamp_build = spta.add_parser("build")
    p_tamp_build.add_argument("--paths", nargs="+", required=True)
    p_tamp_verify = spta.add_parser("verify")

    args = ap.parse_args()

    if args.cmd == "keygen":
        _load_or_create_master_key()
        print("Master key ensured.")
    elif args.cmd == "device":
        if args.dev_cmd == "add":
            add_device(args.id)
            print("Device added.")
        else:
            print("Devices:", ", ".join(sorted(get_devices())))
    elif args.cmd == "totp":
        if args.totp_cmd == "init":
            uri = init_secret(args.account)
            print("Scan this URI in your authenticator app:
", uri)
        elif args.totp_cmd == "verify":
            ok = totp_verify(args.secret, args.token)
            print("Valid" if ok else "Invalid")
    elif args.cmd == "encrypt":
        encrypt_file(Path(args.src), Path(args.dst), args.aad.encode())
        print("Encrypted:", args.dst)
    elif args.cmd == "decrypt":
        decrypt_file(Path(args.src), Path(args.dst), args.aad.encode())
        print("Decrypted:", args.dst)
    elif args.cmd == "tamper":
        if args.tamper_cmd == "build":
            build_manifest(args.paths)
            print("Manifest built.")
        elif args.tamper_cmd == "verify":
            res = verify_manifest()
            for p, ok in res.items():
                print(p, "OK" if ok else "MISMATCH")
    else:
        ap.print_help()

if __name__ == "__main__":
    main()
