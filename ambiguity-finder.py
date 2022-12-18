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
ids_file = "./cjkvi-ids/ids.txt"
dest_file = "./ambiguities_with_ucs_col.tsv"
with open(ids_file, 'r', encoding='UTF-8') as f:
    tsv = csv.reader(f, delimiter="\t", quotechar='"')
    ambiguous_list = set()
    ids_map = dict()
    for row in tsv:
        if len(row) >= 2:
            # TODO how do you put a list of tuples?
            (unicode_encoding, char) = row[0:2]
            idss = row[2:]
            # exclude characters in the compatibility region
            # under the assumption that we don't care about z-variants in the comptaibility region
            if is_compatibility_ideograph( int(unicode_encoding[2:], 16) ):
                continue
            for it in idss:
                splitted = it.split("[")
                ids = splitted[0] # e.g. ⿱⿻臼丨又[GJK] to ⿱⿻臼丨又

                annotated_char = char
                if len(splitted) >= 2:
                    ucs_cols = splitted[1]   # e.g. ⿱⿻臼丨又[GJK] to GJK]
                    ucs_cols = ucs_cols[:-1] # then to GJK
                    annotated_char = char + ucs_cols
                
                if ids in ids_map:
                    ids_map[ids].append( annotated_char )
                else:
                    ids_map[ids] = list()
                    ids_map[ids].append( annotated_char )
    count = 0
    with open(dest_file, 'w', encoding='UTF-8', newline='') as out:
        writer = csv.writer(out, delimiter='\t', lineterminator='\n')
        for ids in ids_map:
            if len( ids_map[ids] ) > 1:
                count += 1
                writer.writerow([ ids, ids_map[ids] ])
    print(f'number of ambiguous IDSs: count')

# issues:
# i still don't really understand how han unification works.
#   for example, sometimes two glyphs differ very slightly, like what I would assume is variant. like the grass head radical being broken vs not.
#       but the decomposition is the same, even though i would expect it to be using a variant IDC because of the variation in the glyph
#       do I need a special font?
#   and I'm not sure if it's totally "correct" for me to just skip the compatibility region.
# I don't know why the same IDC (at least, equivalent according to Python dicts) is sometimes displayed as tofu and sometimes not


# 327 if I skip compatibility ideographs
# 827 if I don't.
# so there are 500 compatibility ideographs? idk
# so some times there's only a collision for certain variants.
# I think I'm interested in AMBIGUITIES, so imagine you're only using one variant.
# 