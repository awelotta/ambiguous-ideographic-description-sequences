
# Ambiguous Ideographic Description Sequences

IDS (ideographic description sequences) are sequences of IDCs (ideographic description characters) that describe a CJK character's shape. 
For example: the IDS for 偍 is ⿰亻是. 

IDSs can be ambiguous; different characters can have the same IDS. 
For example: ⿱一一 is the IDS for
- 二 (U+4E8C, 	"two")
- 𠄞 (U+2011E,	"ancient form of 上 ("up")")
- 𠄟 (U+2011F,	"ancient form of 下 ("down")")
- 𠄠 (U+20120,	"variant of 二"). 

Or, for a more common example: ⿱十一 describes both 土 (U+571F, "dirt"), and 士 (U+58EB, "scholar").

([Wikipedia page for Ideographic Description Sequences](https://en.wikipedia.org/wiki/Chinese_character_description_languages#Ideographic_Description_Sequences))

## Summary

- `ambiguity-finder.py` Python script used to generate the `ambiguities-ids-*.tsv` files. I didn't write a CLI, you have to edit it yourself.

The `ambiguities-ids-*.tsv` files contain the results, where each row is formatted like
```
IDS	FIRST_CHARACTER,UCS_COLUMN	SECOND_CHARACTER,UCS_COLUMN
```
(sometimes there is no value for UCS_COLUMN, in which case its blank and there is no comma).

- `ambiguities-ids-cdp.tsv`IDS collisions among all characters from `./cjkvi-ids/ids-cdp.txt`, which uses PUA characters for IDCs missing from Unicode
- `ambiguities-ids-cdp-uro.tsv` same as above, but only CJK Unified Ideographs block Unicode characters
- `categorization-ambiguities-ids-cdp-uro.txt` same as `*-uro.tsv`, but manually organized by type of collision.

The following files are probably less relevant to finding IDS collisions

- `ambiguities-ids.tsv` IDS collisions among all characters from `./cjkvi-ids/ids.txt`, which uses encircled numerals for missing IDCs
- `ambiguities-ids-no-ucs.tsv` same as above, but without UCS Column (i.e. GTJKV) information, which to my understanding represents regional/language variants.
- `notes-on-unihan.md` personal notes I took on Han Unification by Unicode, stuff like what z-variants are

Data is sourced from https://github.com/cjkvi/cjkvi-ids. Go there for more explanation and links. They credit the [CHISE project](https://www.chise.org) for `ids.txt`.

## Looking for all the ambiguous IDSs

I wrote a script, `ambiguity-finder.py`, to go through `/cjkvi-ids/ids.txt` and find all the characters with identical IDSs. I skip over compatibility ideographs, as identified from [Unicode® Standard Annex #38: UNICODE HAN DATABASE (UNIHAN): Section 4.4](https://www.unicode.org/reports/tr38/#BlockListing). Compatibility ideographs are ideographs that Unicode considers equivalent to a different ideograph, i.e. are [z-variants](https://en.wikipedia.org/wiki/Z-variant
) (or sometimes just plain identical), but are distinguished by earlier encodings. I'm *assuming* that any differing decomposition from z-variants are encompassed by the UCS Column, such that I'm not losing any information by skipping the compatibility ideographs. I'm not sure what UCS Column is.

Character shapes can have variants depending on the region / language (since Unicode does not distinguish z-variants). In `ids.txt`, if a character has variants with different IDSs, it lists each IDS for that character. So the first thing I did was make a list where a conflict is counted if a character has *any* IDS that collides with another. This is `ambiguities-ids-no-ucs.tsv`.

In `ambiguities-ids.tsv`, I did the same, but instead of just giving the character, I added an annotation. Each annotated character consists of the character concatenated with letters corresponding to the UCS Column. 
I'm not sure if this is correct. For example, sometimes there is a collision of same IDS, *same Codepoint*, but different UCS Column. I can't see the difference because I don't know how to set it up on my computer. (I'm using VSCode with the [Hanazono font](http://fonts.jp/hanazono/))

Some description characters are not in Unicode. `ids.txt` handles this by representing it as an encircled number, like ④ or ⑤, corresponding to the number of strokes in the DC. `ids-cdp.txt` handles this using PUA (Private Use Area), which will appear as something like `&CDP-xxxx`. It still uses some encircled numbers, but no collisions result from this; this result is `ambiguities-ids-cdp.txt`.

At this point, I also decided to clean up the formatting at this point: tabs to separate, commas to separate the UCS Column from the charatcter. I'm leaving the other files with the default Python pretty printing because I don't think they're interesting.

I'm also curious as to what the *common* collisions are, so I reran the script but only analyzing characters within the CJK Unified Ideographs Unicode block, i.e. U+4E00..U+9FFF. The result is `ambiguities-ids-cdp-uro.tsv` (URO stands for [Unified Repertoire and Ordering](https://en.wikipedia.org/wiki/CJK_Unified_Ideographs_(Unicode_block))).

### Commentary

Looking at `ambiguities-ids-cdp-uro.tsv`, there are cases that I want to ignore. I'm only interested in the case where IDSs don't adequately specify the positioning of components.

- an IDC represents multiple shapes

For example: ⿰亻具 = 俱 (U+4FF1) = 倶 (U+5036). In the font I'm using, 具 only appears in 倶 (U+5036). I'm not interested in ambiguities caused by Unicode characters used as IDCs having variant shapes.

- one language's variant of a character may be perfectly identical to another character

Ex: ⿱竹㓣 = 劄 (U+5284) (Taiwan, Hong Kong, and Macau) = 箚 (U+7B9A). IDSs unambiguously describe the shape of the characters in this case, though the semantics are different.

- the IDS given in ids.txt is erroneous

I think the IDS ⿰女⿺免生 for 嬎 (U+5B0E) and 嬔 (U+5B14) (Taiwan, Hong Kong) might be wrong in that 免 is not the same as 免 is distinct from 兔. Or I might have the wrong font. Not sure

- I might want to ignore cross-language z-variants.

If someone designs an input method for a specific language, and were using IDSs or a derived system, then some ambiguities could be disambiguated by the choice of language. OTOH, it seems that part of the motivation of using a graphical system is the ability to, e.g., use the same system for traditional and simplified characters. Also, some of the z-variants are obsolete.

In `categorization-ambiguities-ids-cdp-uro.txt`, I have the contents of `ambiguities-ids-cdp-uro.tsv` but manually reorganized by whether it the ambiguity is like (土 vs. 士), is like (俱 vs. 倶), or is like (劄 (HT) vs. 箚). I'm only doing this based on appearance with (a Japanese font), and I'm not checking super thoroughly if the variants exist or not.

I was thinking that ambiguous IDSs might be useful information if someone were to design an input method or automated typeface design. idk