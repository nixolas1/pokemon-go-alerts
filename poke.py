import requests
import json
import time
from math import radians, cos, sin, asin, sqrt
from time import strftime

# add 96 to test for drowzee
wanted = (143, 149, 131, 151, 146, 134, 145, 132, 103, 136, 144, 6, 3, 9, 34, 113, 40, 130, 59, 126, 26)
LAT, LON = 59.91489154138958, 10.769691467285156
# LAT, LON =  59.914160096249766,10.746334791183472

request_url = "https://pokevision.com/map/data/"
view_url = "https://pokevision.com/#/@"
scan_time = 10
loop_time = 2
stepSize = 0.009
steps = 2
beep = True
log = True
scan_number = 100000
pokedex = {460: "Abomasnow", 63: "Abra", 359: "Absol", 617: "Accelgor", 681: "Aegislash", 142: "Aerodactyl", 306: "Aggron", 190: "Aipom", 65: "Alakazam", 594: "Alomomola", 334: "Altaria", 698: "Amaura", 424: "Ambipom", 591: "Amoonguss", 181: "Ampharos", 347: "Anorith", 24: "Arbok", 59: "Arcanine", 493: "Arceus", 566: "Archen", 567: "Archeops", 168: "Ariados", 348: "Armaldo", 683: "Aromatisse", 304: "Aron", 144: "Articuno", 531: "Audino", 699: "Aurorus", 713: "Avalugg", 610: "Axew", 482: "Azelf", 184: "Azumarill", 298: "Azurill", 371: "Bagon", 343: "Baltoy", 354: "Banette", 689: "Barbaracle", 339: "Barboach", 550: "Basculin", 411: "Bastiodon", 153: "Bayleef", 614: "Beartic", 267: "Beautifly", 15: "Beedrill", 606: "Beheeyem", 374: "Beldum", 182: "Bellossom", 69: "Bellsprout", 712: "Bergmite", 400: "Bibarel", 399: "Bidoof", 688: "Binacle", 625: "Bisharp", 9: "Blastoise", 257: "Blaziken", 242: "Blissey", 522: "Blitzle", 525: "Boldore", 438: "Bonsly", 626: "Bouffalant", 654: "Braixen", 628: "Braviary", 286: "Breloom", 437: "Bronzong", 436: "Bronzor", 406: "Budew", 418: "Buizel", 1: "Bulbasaur", 427: "Buneary", 659: "Bunnelby", 412: "Burmy", 12: "Butterfree", 331: "Cacnea", 332: "Cacturne", 323: "Camerupt", 703: "Carbink", 455: "Carnivine", 565: "Carracosta", 318: "Carvanha", 268: "Cascoon", 351: "Castform", 10: "Caterpie", 251: "Celebi", 609: "Chandelure", 113: "Chansey", 6: "Charizard", 4: "Charmander", 5: "Charmeleon", 441: "Chatot", 421: "Cherrim", 420: "Cherubi", 652: "Chesnaught", 650: "Chespin", 152: "Chikorita", 390: "Chimchar", 358: "Chimecho", 170: "Chinchou", 433: "Chingling", 573: "Cinccino", 366: "Clamperl", 692: "Clauncher", 693: "Clawitzer", 344: "Claydol", 36: "Clefable", 35: "Clefairy", 173: "Cleffa", 91: "Cloyster", 638: "Cobalion", 563: "Cofagrigus", 415: "Combee", 256: "Combusken", 534: "Conkeldurr", 341: "Corphish", 222: "Corsola", 546: "Cottonee", 346: "Cradily", 408: "Cranidos", 342: "Crawdaunt", 488: "Cresselia", 453: "Croagunk", 169: "Crobat", 159: "Croconaw", 558: "Crustle", 615: "Cryogonal", 613: "Cubchoo", 104: "Cubone", 155: "Cyndaquil", 491: "Darkrai", 555: "Darmanitan", 554: "Darumaka", 702: "Dedenne", 585: "Deerling", 633: "Deino", 301: "Delcatty", 225: "Delibird", 655: "Delphox", 386: "Deoxys", 87: "Dewgong", 502: "Dewott", 483: "Dialga", 719: "Diancie", 660: "Diggersby", 50: "Diglett", 132: "Ditto", 85: "Dodrio", 84: "Doduo", 232: "Donphan", 680: "Doublade", 691: "Dragalge", 148: "Dragonair", 149: "Dragonite", 452: "Drapion", 147: "Dratini", 426: "Drifblim", 425: "Drifloon", 529: "Drilbur", 96: "Drowzee", 621: "Druddigon", 580: "Ducklett", 51: "Dugtrio", 206: "Dunsparce", 578: "Duosion", 632: "Durant", 356: "Dusclops", 477: "Dusknoir", 355: "Duskull", 269: "Dustox", 557: "Dwebble", 603: "Eelektrik", 604: "Eelektross", 133: "Eevee", 23: "Ekans", 125: "Electabuzz", 466: "Electivire", 309: "Electrike", 101: "Electrode", 239: "Elekid", 605: "Elgyem", 500: "Emboar", 587: "Emolga", 395: "Empoleon", 244: "Entei", 589: "Escavalier", 196: "Espeon", 677: "Espurr", 530: "Excadrill", 102: "Exeggcute", 103: "Exeggutor", 295: "Exploud", 83: "Farfetch'd", 22: "Fearow", 349: "Feebas", 653: "Fennekin", 160: "Feraligatr", 597: "Ferroseed", 598: "Ferrothorn", 456: "Finneon", 180: "Flaaffy", 669: "Flab\u00e9b\u00e9", 136: "Flareon", 662: "Fletchinder", 661: "Fletchling", 419: "Floatzel", 670: "Floette", 671: "Florges", 330: "Flygon", 590: "Foongus", 205: "Forretress", 611: "Fraxure", 592: "Frillish", 656: "Froakie", 657: "Frogadier", 478: "Froslass", 676: "Furfrou", 162: "Furret", 444: "Gabite", 475: "Gallade", 596: "Galvantula", 569: "Garbodor", 445: "Garchomp", 282: "Gardevoir", 92: "Gastly", 423: "Gastrodon", 649: "Genesect", 94: "Gengar", 74: "Geodude", 443: "Gible", 526: "Gigalith", 203: "Girafarig", 487: "Giratina", 471: "Glaceon", 362: "Glalie", 431: "Glameow", 207: "Gligar", 472: "Gliscor", 44: "Gloom", 673: "Gogoat", 42: "Golbat", 118: "Goldeen", 55: "Golduck", 76: "Golem", 622: "Golett", 623: "Golurk", 706: "Goodra", 704: "Goomy", 368: "Gorebyss", 574: "Gothita", 576: "Gothitelle", 575: "Gothorita", 711: "Gourgeist", 210: "Granbull", 75: "Graveler", 658: "Greninja", 88: "Grimer", 388: "Grotle", 383: "Groudon", 253: "Grovyle", 58: "Growlithe", 326: "Grumpig", 316: "Gulpin", 533: "Gurdurr", 130: "Gyarados", 440: "Happiny", 297: "Hariyama", 93: "Haunter", 701: "Hawlucha", 612: "Haxorus", 631: "Heatmor", 485: "Heatran", 695: "Heliolisk", 694: "Helioptile", 214: "Heracross", 507: "Herdier", 449: "Hippopotas", 450: "Hippowdon", 107: "Hitmonchan", 106: "Hitmonlee", 237: "Hitmontop", 250: "Ho-Oh", 430: "Honchkrow", 679: "Honedge", 720: "Hoopa", 163: "Hoothoot", 187: "Hoppip", 116: "Horsea", 229: "Houndoom", 228: "Houndour", 367: "Huntail", 635: "Hydreigon", 97: "Hypno", 174: "Igglybuff", 314: "Illumise", 392: "Infernape", 686: "Inkay", 2: "Ivysaur", 593: "Jellicent", 39: "Jigglypuff", 385: "Jirachi", 135: "Jolteon", 595: "Joltik", 189: "Jumpluff", 124: "Jynx", 140: "Kabuto", 141: "Kabutops", 64: "Kadabra", 14: "Kakuna", 115: "Kangaskhan", 588: "Karrablast", 352: "Kecleon", 647: "Keldeo", 230: "Kingdra", 99: "Kingler", 281: "Kirlia", 600: "Klang", 707: "Klefki", 599: "Klink", 601: "Klinklang", 109: "Koffing", 98: "Krabby", 401: "Kricketot", 402: "Kricketune", 552: "Krokorok", 553: "Krookodile", 382: "Kyogre", 646: "Kyurem", 305: "Lairon", 608: "Lampent", 645: "Landorus", 171: "Lanturn", 131: "Lapras", 636: "Larvesta", 246: "Larvitar", 380: "Latias", 381: "Latios", 470: "Leafeon", 542: "Leavanny", 166: "Ledian", 165: "Ledyba", 463: "Lickilicky", 108: "Lickitung", 510: "Liepard", 345: "Lileep", 549: "Lilligant", 506: "Lillipup", 264: "Linoone", 667: "Litleo", 607: "Litwick", 271: "Lombre", 428: "Lopunny", 270: "Lotad", 294: "Loudred", 448: "Lucario", 272: "Ludicolo", 249: "Lugia", 457: "Lumineon", 337: "Lunatone", 370: "Luvdisc", 404: "Luxio", 405: "Luxray", 68: "Machamp", 67: "Machoke", 66: "Machop", 240: "Magby", 219: "Magcargo", 129: "Magikarp", 126: "Magmar", 467: "Magmortar", 81: "Magnemite", 82: "Magneton", 462: "Magnezone", 296: "Makuhita", 687: "Malamar", 473: "Mamoswine", 490: "Manaphy", 630: "Mandibuzz", 310: "Manectric", 56: "Mankey", 226: "Mantine", 458: "Mantyke", 556: "Maractus", 179: "Mareep", 183: "Marill", 105: "Marowak", 259: "Marshtomp", 284: "Masquerain", 303: "Mawile", 308: "Medicham", 307: "Meditite", 154: "Meganium", 648: "Meloetta", 678: "Meowstic", 52: "Meowth", 481: "Mesprit", 376: "Metagross", 375: "Metang", 11: "Metapod", 151: "Mew", 150: "Mewtwo", 619: "Mienfoo", 620: "Mienshao", 262: "Mightyena", 350: "Milotic", 241: "Miltank", 439: "Mime Jr.", 572: "Minccino", 312: "Minun", 200: "Misdreavus", 429: "Mismagius", 146: "Moltres", 391: "Monferno", 414: "Mothim", 122: "Mr. Mime", 258: "Mudkip", 89: "Muk", 446: "Munchlax", 517: "Munna", 198: "Murkrow", 518: "Musharna", 177: "Natu", 34: "Nidoking", 31: "Nidoqueen", 29: "Nidoran\u2640", 32: "Nidoran\u2642", 30: "Nidorina", 33: "Nidorino", 290: "Nincada", 38: "Ninetales", 291: "Ninjask", 164: "Noctowl", 714: "Noibat", 715: "Noivern", 299: "Nosepass", 322: "Numel", 274: "Nuzleaf", 224: "Octillery", 43: "Oddish", 138: "Omanyte", 139: "Omastar", 95: "Onix", 501: "Oshawott", 417: "Pachirisu", 484: "Palkia", 536: "Palpitoad", 674: "Pancham", 675: "Pangoro", 515: "Panpour", 511: "Pansage", 513: "Pansear", 46: "Paras", 47: "Parasect", 504: "Patrat", 624: "Pawniard", 279: "Pelipper", 53: "Persian", 548: "Petilil", 231: "Phanpy", 708: "Phantump", 489: "Phione", 172: "Pichu", 18: "Pidgeot", 17: "Pidgeotto", 16: "Pidgey", 519: "Pidove", 499: "Pignite", 25: "Pikachu", 221: "Piloswine", 204: "Pineco", 127: "Pinsir", 393: "Piplup", 311: "Plusle", 186: "Politoed", 60: "Poliwag", 61: "Poliwhirl", 62: "Poliwrath", 77: "Ponyta", 261: "Poochyena", 137: "Porygon", 474: "Porygon-Z", 233: "Porygon2", 57: "Primeape", 394: "Prinplup", 476: "Probopass", 54: "Psyduck", 710: "Pumpkaboo", 247: "Pupitar", 509: "Purrloin", 432: "Purugly", 668: "Pyroar", 195: "Quagsire", 156: "Quilava", 651: "Quilladin", 211: "Qwilfish", 26: "Raichu", 243: "Raikou", 280: "Ralts", 409: "Rampardos", 78: "Rapidash", 20: "Raticate", 19: "Rattata", 384: "Rayquaza", 378: "Regice", 486: "Regigigas", 377: "Regirock", 379: "Registeel", 369: "Relicanth", 223: "Remoraid", 643: "Reshiram", 579: "Reuniclus", 112: "Rhydon", 111: "Rhyhorn", 464: "Rhyperior", 447: "Riolu", 524: "Roggenrola", 315: "Roselia", 407: "Roserade", 479: "Rotom", 627: "Rufflet", 302: "Sableye", 373: "Salamence", 503: "Samurott", 551: "Sandile", 27: "Sandshrew", 28: "Sandslash", 539: "Sawk", 586: "Sawsbuck", 664: "Scatterbug", 254: "Sceptile", 212: "Scizor", 545: "Scolipede", 560: "Scrafty", 559: "Scraggy", 123: "Scyther", 117: "Seadra", 119: "Seaking", 364: "Sealeo", 273: "Seedot", 86: "Seel", 537: "Seismitoad", 161: "Sentret", 497: "Serperior", 496: "Servine", 336: "Seviper", 540: "Sewaddle", 319: "Sharpedo", 492: "Shaymin", 292: "Shedinja", 372: "Shelgon", 90: "Shellder", 422: "Shellos", 616: "Shelmet", 410: "Shieldon", 275: "Shiftry", 403: "Shinx", 285: "Shroomish", 213: "Shuckle", 353: "Shuppet", 561: "Sigilyph", 266: "Silcoon", 516: "Simipour", 512: "Simisage", 514: "Simisear", 227: "Skarmory", 672: "Skiddo", 188: "Skiploom", 300: "Skitty", 451: "Skorupi", 690: "Skrelp", 435: "Skuntank", 289: "Slaking", 287: "Slakoth", 705: "Sliggoo", 80: "Slowbro", 199: "Slowking", 79: "Slowpoke", 218: "Slugma", 685: "Slurpuff", 235: "Smeargle", 238: "Smoochum", 215: "Sneasel", 495: "Snivy", 143: "Snorlax", 361: "Snorunt", 459: "Snover", 209: "Snubbull", 577: "Solosis", 338: "Solrock", 21: "Spearow", 665: "Spewpa", 363: "Spheal", 167: "Spinarak", 327: "Spinda", 442: "Spiritomb", 325: "Spoink", 682: "Spritzee", 7: "Squirtle", 234: "Stantler", 398: "Staraptor", 397: "Staravia", 396: "Starly", 121: "Starmie", 120: "Staryu", 208: "Steelix", 508: "Stoutland", 618: "Stunfisk", 434: "Stunky", 185: "Sudowoodo", 245: "Suicune", 192: "Sunflora", 191: "Sunkern", 283: "Surskit", 333: "Swablu", 541: "Swadloon", 317: "Swalot", 260: "Swampert", 581: "Swanna", 277: "Swellow", 220: "Swinub", 684: "Swirlix", 528: "Swoobat", 700: "Sylveon", 276: "Taillow", 663: "Talonflame", 114: "Tangela", 465: "Tangrowth", 128: "Tauros", 216: "Teddiursa", 72: "Tentacool", 73: "Tentacruel", 498: "Tepig", 639: "Terrakion", 538: "Throh", 642: "Thundurus", 532: "Timburr", 564: "Tirtouga", 468: "Togekiss", 175: "Togepi", 176: "Togetic", 255: "Torchic", 324: "Torkoal", 641: "Tornadus", 389: "Torterra", 158: "Totodile", 454: "Toxicroak", 520: "Tranquill", 328: "Trapinch", 252: "Treecko", 709: "Trevenant", 357: "Tropius", 568: "Trubbish", 387: "Turtwig", 535: "Tympole", 602: "Tynamo", 157: "Typhlosion", 248: "Tyranitar", 697: "Tyrantrum", 236: "Tyrogue", 696: "Tyrunt", 197: "Umbreon", 521: "Unfezant", 201: "Unown", 217: "Ursaring", 480: "Uxie", 583: "Vanillish", 582: "Vanillite", 584: "Vanilluxe", 134: "Vaporeon", 543: "Venipede", 49: "Venomoth", 48: "Venonat", 3: "Venusaur", 416: "Vespiquen", 329: "Vibrava", 494: "Victini", 71: "Victreebel", 288: "Vigoroth", 45: "Vileplume", 640: "Virizion", 666: "Vivillon", 313: "Volbeat", 721: "Volcanion", 637: "Volcarona", 100: "Voltorb", 629: "Vullaby", 37: "Vulpix", 320: "Wailmer", 321: "Wailord", 365: "Walrein", 8: "Wartortle", 505: "Watchog", 461: "Weavile", 13: "Weedle", 70: "Weepinbell", 110: "Weezing", 547: "Whimsicott", 544: "Whirlipede", 340: "Whiscash", 293: "Whismur", 40: "Wigglytuff", 278: "Wingull", 202: "Wobbuffet", 527: "Woobat", 194: "Wooper", 413: "Wormadam", 265: "Wurmple", 360: "Wynaut", 178: "Xatu", 716: "Xerneas", 562: "Yamask", 193: "Yanma", 469: "Yanmega", 717: "Yveltal", 335: "Zangoose", 145: "Zapdos", 523: "Zebstrika", 644: "Zekrom", 263: "Zigzagoon", 571: "Zoroark", 570: "Zorua", 41: "Zubat", 634: "Zweilous", 718: "Zygarde"}


found = []


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km


def logToFile(text):
    with open("poke.log", "a") as myfile:
        myfile.write(text+"\n")


def check_if_wanted_pokemon_is_nearby(lat, lon, wanted):
    data = requests.get(request_url+str(lat)+'/'+str(lon))
    try:
        data = data.json()
    
    except:
        print("Error, no object")
        return False

    pokemons = data.get("pokemon")

    if data.get("status") == "success" and pokemons:
        for pokemon in pokemons:
            pokeID = pokemon.get("pokemonId")
            if pokeID in wanted or pokeID > 151:
                name = pokedex[pokemon.get("pokemonId")]
                latt = float(pokemon.get("latitude"))
                lonn = float(pokemon.get("longitude"))
                dist = haversine(LON, LAT, lonn, latt)
                id = pokemon.get("id")
                if id not in found:
                    found.append(id)
                    out = "["+strftime("%H:%M")+"] "+"Found a " + name + " " + str(int(dist*1000)) + "m away! Url: " + view_url + str(latt)+","+str(lonn)
                    
                    if(log):
                        logToFile(out)

                    if beep:
                        out += "\a"

                    print out
    if not found:
        return False


def find_around(lat, lon, wanted, steps):
    for x in range(-steps, steps+1):
        for y in range(-steps, steps+1):
            latt = lat + x*stepSize
            lonn = lon + y*stepSize
            check_if_wanted_pokemon_is_nearby(latt, lonn, wanted)
            time.sleep(loop_time)


while(scan_number):
    scan_number -= 1
    # print("Scanning...")
    find_around(LAT, LON, wanted, steps)
    # check_if_wanted_pokemon_is_nearby(lat, lon, wanted)

    time.sleep(scan_time)
