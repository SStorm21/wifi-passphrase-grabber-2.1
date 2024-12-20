import os
import ast
import sys
import zlib
import base64
import random
import argparse
import marshal


class PyObfuscator:
    def __init__(self, code: str, include_imports: bool = False, recursion: int = 1) -> None:
        self._code = code
        self._imports = []
        self._aliases = {}
        self._valid_identifiers = [chr(i) for i in range(0x41, 0x7A) if chr(i).isidentifier()] 

        # Options
        self.__include_imports = include_imports
        if recursion < 1:
            raise ValueError("Recursion length cannot be less than 1")
        else:
            self.__recursion = recursion

    def obfuscate(self) -> str:
        self._remove_comments_and_docstrings()
        self._save_imports()

        layers = [
            self._layer_1,
            self._layer_2,
            self._layer_3,
            self._layer_4
        ] * self.__recursion
        random.shuffle(layers)

        if layers[-1] == self._layer_3:
            for index, layer in enumerate(layers):
                if layer != self._layer_3:
                    layers[index], layers[-1] = layers[-1], layers[index]
                    break

        for layer in layers:
            layer()

        if self.__include_imports:
            self._prepend_imports()
        return self._code

    def _remove_comments_and_docstrings(self) -> None:
        tree = ast.parse(self._code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str):
                node.value.value = ""  
        self._code = ast.unparse(tree)

    def _save_imports(self) -> None:
        tree = ast.parse(self._code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self._imports.append((None, alias.name))
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                for alias in node.names:
                    self._imports.append((module, alias.name))

    def _prepend_imports(self) -> None:
        imports_code = "\n".join(
            f"from {module} import {name}" if module else f"import {name}" for module, name in self._imports
        )
        self._code = imports_code + "\n" + self._code

    def _layer_1(self) -> None:
        encoded = base64.b64encode(zlib.compress(self._code.encode())).decode()
        self._code = f"import zlib, base64\nexec(zlib.decompress(base64.b64decode('{encoded}')))"

    def _layer_2(self) -> None:
        key = random.randint(1, 255)
        encrypted = [key ^ b for b in zlib.compress(self._code.encode())]
        self._code = (
            f"import zlib\n"
            f"key={key}\n"
            f"encrypted={encrypted}\n"
            f"exec(zlib.decompress(bytes([key ^ b for b in encrypted])))"
        )

    def _layer_3(self) -> None:
        encoded = base64.b64encode(zlib.compress(self._code.encode())).decode()
        ip_chunks = [encoded[i : i + 4] for i in range(0, len(encoded), 4)]
        self._code = (
            "import zlib, base64\n"
            "data = " + str(ip_chunks) + "\n"
            "decoded = ''.join(data)\n"
            "exec(zlib.decompress(base64.b64decode(decoded)))"
        )

    def _layer_4(self) -> None:
        marshaled_code = marshal.dumps(compile(self._code, "<string>", "exec"))
        compressed = zlib.compress(marshaled_code)
        encoded = base64.b64encode(compressed).decode()
        self._code = (
            f"import marshal, zlib, base64\n"
            f"exec(marshal.loads(zlib.decompress(base64.b64decode('{encoded}'))))"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="PyObfuscator: Obfuscates Python code to make it unreadable and hard to reverse.",
    )
    parser.add_argument(
        "--input", "-i", required=True, help="The file containing the code to obfuscate", metavar="PATH"
    )
    parser.add_argument(
        "--output",
        "-o",
        required=False,
        help="The file to write the obfuscated code (defaults to Obfuscated_[input].py)",
        metavar="PATH",
    )
    parser.add_argument(
        "--recursive",
        "-r",
        type=int,
        default=1,
        help="Number of recursive obfuscation layers (default: 1)",
    )
    parser.add_argument(
        "--include-imports",
        required=False,
        action="store_true",
        help="Include the import statements on the top of the obfuscated file",
    )

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print("Error: Input file does not exist.")
        sys.exit(1)

    output_file = args.output or f"Obfuscated_{os.path.basename(args.input)}"
    with open(args.input, "r", encoding="utf-8") as file:
        original_code = file.read()

    obfuscator = PyObfuscator(original_code, args.include_imports, args.recursive)
    obfuscated_code = obfuscator.obfuscate()

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(obfuscated_code)

    print(f"Obfuscated code written to {output_file}")


if __name__ == "__main__":
    main()
