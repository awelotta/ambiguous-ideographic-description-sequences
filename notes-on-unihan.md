# Unihan

x-axis: meaning
y-axis: major shape differences (e.g. simplified vs. traditional)
z-axis: minor typographical differences (e.g. double-storey vs. single-storey g; stylistic differences between countries)

Unicode intends to encode x/y-variants; this is what Unicode (mostly) does with the other symbols, 
and language-markup should deal with z-variants. 

reasons for z-variants in Unicode
- to support **round-trip** compatibility. (This also motivates some duplicates, if some earlier encoding had duplicates.)
- others? support for low-memory devices?
- sometimes "z-variants" are considered significant in some contexts but not others. for example,
	- in Japan, place names tend to be conservative. Unicode® Technical Standard #37, says to use variant selectors, which are special characters in Unicode

in reality, they made several (how many?) mistakes

unicode also has a bunch of metadata for each character. like what its variants are

CJK Unified Ideographs are in:
CJK Unified Ideographs, 
CJK Unified Ideographs Extension A-H, 
parts of CJK Compatibility Ideographs block (U+FA0E, U+FA0F, U+FA11, U+FA13, U+FA14, U+FA1F, U+FA21, U+FA23, U+FA24, U+FA27, U+FA28, and U+FA29), 

CJK Compatibility Ideographis are in:
most of CJK Compatibility Ideographs block (excluding U+FA0E, U+FA0F, U+FA11, U+FA13, U+FA14, U+FA1F, U+FA21, U+FA23, U+FA24, U+FA27, U+FA28, and U+FA29)
CJK Compatibility Supplement

https://www.unicode.org/reports/tr38/#BlockListing

... there's also other Unihan stuff

https://en.wikipedia.org/wiki/Han_unification#Unihan_database_files
https://en.wikipedia.org/wiki/Z-variant
https://www.unicode.org/reports/tr38
https://www.unicode.org/notes/tn26/
https://www.unicode.org/reports/tr37/