"""Confronta le parole di configurazione XC32 nell'ELF con i pragma e il DFP."""
import argparse
from pathlib import Path
from struct import Struct, unpack_from


def expected(source, definitions):
    fields = {}
    for line in definitions.splitlines():
        parts = line.split(":")
        if parts[0] == "CWORD":
            address = int(parts[1], 16)
        elif parts[0] == "CSETTING":
            values = {}
            fields[parts[2]] = address, int(parts[1], 16), values
        elif parts[0] == "CVALUE":
            values[parts[2]] = int(parts[1], 16)

    words = {}
    for line in source.splitlines():
        if not line.startswith("#pragma config "):
            continue
        for assignment in line.removeprefix("#pragma config ").split(","):
            setting, choice = (part.strip() for part in assignment.split("="))
            address, mask, values = fields[setting]
            used, value = words.get(address, (0, 0))
            if used & mask:
                raise ValueError(f"{setting} definita due volte")
            words[address] = used | mask, value | (values[choice] & mask)
    if not words:
        raise ValueError("Nessun pragma di configurazione")
    return words


def check_image(image, words):
    if image[:6] != b"\x7fELF\x01\x01" or unpack_from("<HH", image, 16) != (2, 8):
        raise ValueError("Atteso ELF32 MIPS eseguibile little endian")
    entry, _, table = unpack_from("<III", image, 24)
    size, count = unpack_from("<HH", image, 46)
    header = Struct("<10I")
    if size < header.size or table + count * size > len(image):
        raise ValueError("Tabella sezioni non valida")
    pending = dict(words)
    code = False
    for index in range(count):
        _, kind, flags, addr, offset, length, *_ = header.unpack_from(image, table + index * size)
        if kind != 1 or not flags & 2:
            continue
        if offset + length > len(image):
            raise ValueError("Sezione troncata")
        code |= bool(flags & 4 and addr <= entry < addr + length)
        for address, (mask, wanted) in list(pending.items()):
            if addr <= address and address + 4 <= addr + length:
                actual, = unpack_from("<I", image, offset + address - addr)
                if actual & mask != wanted:
                    raise ValueError(f"Configurazione errata a {address:#x}")
                del pending[address]
    if pending or not code:
        raise ValueError(f"Configurazione mancante {list(map(hex, pending))} o entry point non eseguibile")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("source", "definitions", "elf"):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    words = expected(args.source.read_text(), args.definitions.read_text())
    check_image(args.elf.read_bytes(), words)
    print(f"ELF MIPS verificato: {len(words)} parole di configurazione")
