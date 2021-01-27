import vobject
import argparse
from pprint import pprint


def main():
    parser = argparse.ArgumentParser(description='Convert Gmail contacts to Nokia contacts.')
    parser.add_argument('--src', type=str, help='Input vCard file')
    parser.add_argument('--dst', type=str, help='Output vCard 2.1 Nokia file')

    args = parser.parse_args()
    print("Reading from %s" % args.src)
    print("Writing to %s" % args.dst)

    with open(args.src, 'r', encoding='utf-8') as input_file:
        all_lines = input_file.readlines()
        all_content = ''.join(all_lines)

    with open(args.dst, 'w', encoding='utf-8') as output_file:
        for e in vobject.readComponents(all_content):
            names = []
            tels = []

            if e.contents.get('fn'):
                names.extend([name.value for name in e.contents['fn']])
            if e.contents.get('n'):
                names.extend([name.value for name in e.contents['n']])

            if e.contents.get('tel'):
                for tel in e.contents['tel']:
                    types = []
                    if tel.params.get('TYPE'):
                        types = tel.params['TYPE']
                    tels.append((tel.value, types))
            print("-------------------")
            print("    " + str(names))
            print("    " + str(tels))

            if len(names) > 0 and len(tels) > 0:
                i=1
                for tel_tuple in tels:
                    if len(tels) > 1:
                        name = "{} ({})".format(names[0], i)
                    else:
                        name = names[0]
                    tel = tel_tuple[0]

                    lines = [
                        "BEGIN:VCARD",
                        "VERSION:2.1",
                        "N;ENCODING=QUOTED-PRINTABLE;CHARSET=UTF-8:;=",
                        name.replace(" ", "=20") + ";;;",
                        "TEL;VOICE;CELL:" + tel.replace(" ", "").replace("-", ""),
                        "END:VCARD"
                    ]
                    output_file.write("\n".join(lines) + "\n")
                    i += 1


if __name__ == "__main__":
    main()
