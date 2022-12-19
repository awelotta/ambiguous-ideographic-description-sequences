## NOTE: I can't be bothered to figure out a CLI, 
## so you have to modify code in here if you want to use a different file or add constraints. 
## Sorry.

import csv

def is_compatibility_ideograph(unicode_hex):
    cjk_compatibility_ideographs = range(0xF900, 0xFADA)
    cci_not_actually_cci = {
        0xFA0E,
        0xFA0F,
        0xFA11,
        0xFA13,
        0xFA14,
        0xFA1F,
        0xFA21,
        0xFA23,
        0xFA24,
        0xFA27,
        0xFA28,
        0xFA29,
    }
    cjk_compatibility_supplement = range(0x2F800, 0x2FA1D)
    return (
        (
            unicode_hex in cjk_compatibility_ideographs
            and unicode_hex not in cci_not_actually_cci
        )
        or unicode_hex in cjk_compatibility_supplement
    )

# https://github.com/cjkvi/cjkvi-ids
ids_file = "./cjkvi-ids/ids-cdp.txt"       ## CHANGE THIS LINE FOR SOURCE FILE
dest_file = "./ambiguities-ids-cdp-uro.tsv"    ## CHANGE THIS LINE FOR OUTPUT DESTINATION
with open(ids_file, 'r', encoding='UTF-8') as f:
    tsv = csv.reader(f, delimiter="\t", quotechar='"')
    # ids_dict is a dict from IDS to list of Annotated Characters # Annotated Character = Character + UCS Columns
    ids_dict = dict()
    for row in tsv:
        # exclude "comment" rows
        if row[0] == ";;" or row[0] == "#":
            continue
        
        if len(row) >= 2:
            (codepoint, char, *idss) = row
            if (codepoint[0:2] == "U+"):
                codepoint = int(codepoint[2:], 16)
                # choose to exclude compatibility ideographs
                if is_compatibility_ideograph(codepoint):
                    continue
                # choose to restrict to CJK Unified Ideographs block U+4E00..U+9FFF
                                        ## CHANGE THESE LINES IF YOU DON'T WANT TO LIMIT
                codepoint_restriction = range(0x4E00, 0xA000)
                if codepoint not in codepoint_restriction:
                    continue
            else:   ## CHANGE IF you don't want to skip over CDP characters. this branch skips over CDP characters
                continue

            for annotated_ids in idss: # it has the form  ⿱⿻臼丨又[GJK] if there are multiple variants, or just ⿰日丙
                splitted = annotated_ids.split("[")
                ids = splitted[0] # e.g. ⿱⿻臼丨又[GJK] to ⿱⿻臼丨又

                annotated_char = char
                if len(splitted) >= 2:
                    ucs_cols = splitted[1]   # e.g. ⿱⿻臼丨又[GJK] to GJK]
                    ucs_cols = ucs_cols[:-1] # then to GJK
                    delimiter = ','
                    annotated_char = f"{char}{delimiter}{ucs_cols}"
                
                if ids not in ids_dict:
                    ids_dict[ids] = list()
                ids_dict[ids].append(annotated_char)
    count = 0
    with open(dest_file, 'w', encoding='UTF-8', newline='') as out:
        writer = csv.writer(out, delimiter='\t', lineterminator='\n')
        for ids in ids_dict:
            if len( ids_dict[ids] ) > 1:
                count += 1
                print( [ids] + [char for char in ids_dict[ids] ] )
                writer.writerow( [ids] + [char for char in ids_dict[ids]] )
    print(f'number of ambiguous IDSs: {count}')

    # ⿱⑧山 𡸭   𡸸 T