import argparse
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("files", type=str, nargs="+")
    parser.add_argument("-o", "--output", type=str, default="merged.json")
    result = dict()
    for file in parser.parse_args().files:
        with open(file, "r", encoding="utf-8") as f:
            current = json.load(f)
        for key, value in current.items():
            if key not in result:
                result[key] = value
                continue
            for key2, value2 in value.items():
                if key2 not in ["German", "English"]:
                    continue
                assert key2 in result[key]
                result[key][key2].extend(value2)
    with open(parser.parse_args().output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
