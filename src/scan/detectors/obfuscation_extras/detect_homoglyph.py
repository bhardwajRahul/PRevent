from src.settings import FULL_FINDINGS


def detect_homoglyph(patch: str) -> list[dict]:
    results = []
    impostors = ''.join(map(str, homoglyphs.values()))
    for impostor in impostors:
        index = patch.find(impostor)
        if index != -1:
            line_number = patch.count('\n', 0, index) + 1
            match = patch.splitlines()[line_number - 1]
            results.append({
                "message": "A hardcoded base64 encoded string.",
                "line_number": line_number,
                "match": match
            })
            if not FULL_FINDINGS:
                return results
    return results


# These characters may be interpreted as similar chars in some programming languages.
# They can help avoid static strings detection.
homoglyphs = {
    "a": "ａ𝐚𝑎𝒂𝒶𝓪𝔞𝕒𝖆𝖺𝗮𝘢𝙖𝚊",
    "b": "ｂ𝐛𝑏𝒃𝒷𝓫𝔟𝕓𝖇𝖻𝗯𝘣𝙗𝚋",
    "c": "ⅽｃ𝐜𝑐𝒄𝒸𝓬𝔠𝕔𝖈𝖼𝗰𝘤𝙘𝚌",
    "d": "ⅆⅾｄ𝐝𝑑𝒅𝒹𝓭𝔡𝕕𝖉𝖽𝗱𝘥𝙙𝚍",
    "e": "ℯⅇｅ𝐞𝑒𝒆𝓮𝔢𝕖𝖊𝖾𝗲𝘦𝙚𝚎",
    "f": "ſｆ𝐟𝑓𝒇𝒻𝓯𝔣𝕗𝖋𝖿𝗳𝘧𝙛𝚏",
    "g": "ℊｇ𝐠𝑔𝒈𝓰𝔤𝕘𝖌𝗀𝗴𝘨𝙜𝚐ᵍ",
    "h": "ℎｈ𝐡𝒉𝒽𝓱𝔥𝕙𝖍𝗁𝗵𝘩𝙝𝚑ᴴ",
    "i": "ℐℑℓℹⅈⅰⅼＩｉｌ𝐈𝐢𝐥𝐼𝑖𝑙𝑰𝒊𝒍𝒾𝓁𝓘𝓲𝓵𝔦𝔩𝕀𝕚𝕝𝕴𝖎𝖑𝖨𝗂𝗅𝗜𝗶𝗹𝘐𝘪𝘭𝙄𝙞𝙡𝙸𝚒𝚕",
    "j": "ⅉｊ𝐣𝑗𝒋𝒿𝓳𝔧𝕛𝖏𝗃𝗷𝘫𝙟𝚓",
    "k": "ｋ𝐤𝑘𝒌𝓀𝓴𝔨𝕜𝖐𝗄𝗸𝘬𝙠𝚔",
    "l": "ℒˡ𝐋𝐿𝑳𝓛𝔏𝕃𝕷𝖫𝗟𝘓𝙇𝙻",
    "m": "ｍ",
    "n": "ｎ𝐧𝑛𝒏𝓃𝓷𝔫𝕟𝖓𝗇𝗻𝘯𝙣𝚗",
    "o": "ℴ",
    "p": "ｐ𝐩𝑝𝒑𝓅𝓹𝔭𝕡𝖕𝗉𝗽𝘱𝙥𝚙ᴾ",
    "q": "ｑ𝐪𝑞𝒒𝓆𝓺𝔮𝕢𝖖𝗊𝗾𝘲𝙦𝚚",
    "r": "ｒ𝐫𝑟𝒓𝓇𝓻𝔯𝕣𝖗𝗋𝗿𝘳𝙧𝚛ʳ",
    "s": "ｓ𝐬𝑠𝒔𝓈𝓼𝔰𝕤𝖘𝗌𝘀𝘴𝙨𝚜ˢ",
    "t": "ｔ𝐭𝑡𝒕𝓉𝓽𝔱𝕥𝖙𝗍𝘁𝘵𝙩𝚝",
    "u": "ｕ𝐮𝑢𝒖𝓊𝓾𝔲𝕦𝖚𝗎𝘂𝘶𝙪𝚞",
    "v": "ⅴｖ𝐯𝑣𝒗𝓋𝓿𝔳𝕧𝖛𝗏𝘃𝘷𝙫𝚟",
    "w": "ｗ𝐰𝑤𝒘𝓌𝔀𝔴𝕨𝖜𝗐𝘄𝘸𝙬𝚠",
    "x": "ⅹｘ𝐱𝑥𝒙𝓍𝔁𝔵𝕩𝖝𝗑𝘅𝘹𝙭𝚡",
    "y": "ｙ𝐲𝑦𝒚𝓎𝔂𝔶𝕪𝖞𝗒𝘆𝘺𝙮𝚢",
    "z": "ｚ𝐳𝑧𝒛𝓏𝔃𝔷𝕫𝖟𝗓𝘇𝘻𝙯𝚣ᶻ",
    "A": "Ａ𝐀𝐴𝑨𝒜𝓐𝔄𝔸𝕬𝖠𝗔𝘈𝘼𝙰",
    "B": "ℬＢ𝐁𝐵𝑩𝓑𝔅𝔹𝕭𝖡𝗕𝘉𝘽𝙱",
    "C": "ℂℭⅭＣ𝐂𝐶𝑪𝒞𝓒𝕮𝖢𝗖𝘊𝘾𝙲",
    "D": "ⅅⅮＤ𝐃𝐷𝑫𝒟𝓓𝔇𝔻𝕯𝖣𝗗𝘋𝘿𝙳",
    "E": "ℰＥ𝐄𝐸𝑬𝓔𝔈𝔼𝕰𝖤𝗘𝘌𝙀𝙴",
    "F": "ℱＦ𝐅𝐹𝑭𝓕𝔉𝔽𝕱𝖥𝗙𝘍𝙁𝙵",
    "G": "Ｇ𝐆𝐺𝑮𝒢𝓖𝔊𝔾𝕲𝖦𝗚𝘎𝙂𝙶",
    "H": "ℋℌℍＨ𝐇𝐻𝑯𝓗𝕳𝖧𝗛𝘏𝙃𝙷",
    "I": "Ⅰ",
    "J": "Ｊ𝐉𝐽𝑱𝒥𝓙𝔍𝕁𝕵𝖩𝗝𝘑𝙅𝙹",
    "K": "KＫ𝐊𝐾𝑲𝒦𝓚𝔎𝕂𝕶𝖪𝗞𝘒𝙆𝙺",
    "L": "ⅬⅬＬ",
    "M": "ℳⅯＭ𝐌𝑀𝑴𝓜𝔐𝕄𝕸𝖬𝗠𝘔𝙈𝙼",
    "N": "ℕＮ𝐍𝑁𝑵𝒩𝓝𝔑𝕹𝖭𝗡𝘕𝙉𝙽",
    "O": "ｏ𝐎𝐨𝑂𝑜𝑶𝒐𝒪𝓞𝓸𝔒𝔬𝕆𝕠𝕺𝖔𝖮𝗈𝗢𝗼𝘖𝘰𝙊𝙤𝙾𝚘",
    "P": "ℙＰ𝐏𝑃𝑷𝒫𝓟𝔓𝕻𝖯𝗣𝘗𝙋𝙿",
    "Q": "ℚＱ𝐐𝑄𝑸𝒬𝓠𝔔𝕼𝖰𝗤𝘘𝙌𝚀",
    "R": "ℛℜℝＲ𝐑𝑅𝑹𝓡𝕽𝖱𝗥𝘙𝙍𝚁",
    "S": "Ｓ𝐒𝑆𝑺𝒮𝓢𝔖𝕊𝕾𝖲𝗦𝘚𝙎𝚂",
    "T": "Ｔ𝐓𝑇𝑻𝒯𝓣𝔗𝕋𝕿𝖳𝗧𝘛𝙏𝚃",
    "U": "Ｕ𝐔𝑈𝑼𝒰𝓤𝔘𝕌𝖀𝖴𝗨𝘜𝙐𝚄",
    "V": "ⅤＶ𝐕𝑉𝑽𝒱𝓥𝔙𝕍𝖁𝖵𝗩𝘝𝙑𝚅",
    "W": "Ｗ𝐖𝑊𝑾𝒲𝓦𝔚𝕎𝖂𝖶𝗪𝘞𝙒𝚆",
    "X": "ⅩＸ𝐗𝑋𝑿𝒳𝓧𝔛𝕏𝖃𝖷𝗫𝘟𝙓𝚇",
    "Y": "Ｙ𝐘𝑌𝒀𝒴𝓨𝔜𝕐𝖄𝖸𝗬𝘠𝙔𝚈",
    "Z": "ℤℨＺ𝐙𝑍𝒁𝒵𝓩𝖅𝖹𝗭𝘡𝙕𝚉"
}
