# nameID=1,2, platformID=3, platEncID, langID
# nameID:
#       1: Font Family name, 2: Font Style name
# platformID:
#       3: Windows
# platEncID: (Windows) always 1
#       1: Unicode BMP, 3: PRC, 4: Big5, 10: Unicode full repertoire
# langID: (Windows)
#       2052: PRC, 1028: TW, 4100: Singapore, 3076: HK, 5124: Macao
#       1041: JPN, 1042: KOR
# https://docs.microsoft.com/en-us/typography/opentype/spec/name
fontIDSeq = [2052, 1028, 4100, 3076, 5124, 1041, 1042, None]

fontsize = 20 # int
fonttext = '這是示例文字' # str
fontperpage = 50 # int

# don't change these
maxsearch = 15 #(10)
dupeperpage = 5 #(3)