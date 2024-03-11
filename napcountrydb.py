#!/usr/bin/python3

valid_countries = ['България', 'Австралия', 'Австрия', 'Азербайджан', 'Албания', 'Алжир', 'Ангола', 'Ангуила', 'Андора', 'Антарктида', 'Антигуа и Барбуда', 'Аржентина', 'Армения', 'Аруба', 'Афганистан', 'Бангладеш', 'Барбадос', 'Бахамски о-ви', 'Бахрейн', 'Беларус', 'Белгия', 'Белиз', 'Бенин', 'Бермудски о-ви', 'Боливия', 'Босна и Херцеговина', 'Ботсуана', 'Бразилия', 'Брит. територия в Индийския океан', 'Бруней', 'Буве', 'Буркина фасо', 'Бурунди', 'Бутан', 'Вануату', 'Ватикана', 'Великобритания', 'Венецуела', 'Виетнам', 'Виржински о-ви (Брит.)', 'Виржински о-ви (САЩ)', 'Габон', 'Гамбия', 'Гана', 'Гаяна', 'Гваделупа', 'Гватемала', 'Гвинея', 'Гвинея-Бисау', 'Германия', 'Гиана(Фр.)', 'Гибралтар', 'Гренада', 'Гренландия', 'Грузия', 'Гуам', 'Гърция', 'Дания', 'Джибути', 'Доминика', 'Доминиканска република', 'Египет', 'Ейре (Ирландия)', 'Еквадор', 'Екваториална Гвинея', 'Еритрея', 'Естония', 'Етиопия', 'Заир', 'Замбия', 'Западна Сахара', 'Зимбабве', 'Израел', 'Източен Тимор', 'Източни Самоа (САЩ)', 'Индия', 'Индонезия', 'Ирак', 'Иран', 'Ирландия', 'Исландия', 'Испания', 'Италия', 'Йемен', 'Йордания', 'Кабо Верде', 'Казахстан', 'Кайманови о-ви', 'Камбоджа', 'Камерун', 'Канада', 'Катар', 'Кения', 'Кипър', 'Киргизтан', 'Кирибати', 'Китай', 'КНДР', 'Кокосови о-ви', 'Колумбия', 'Коморски о-ви', 'Конго', 'Косово', 'Коста Рика', 'Кот д`Ивоар', 'Куба', 'Кувейт', 'Лаос', 'Латвия ', 'Лесото', 'Либерия', 'Либия', 'Ливан', 'Литва', 'Лихтенщайн', 'Люксембург', 'Мавритания', 'Мавриций', 'Мадагаскар', 'Макао', 'Малави', 'Малайзия', 'Малдиви', 'Мали', 'Малки далечни о-ви на САЩ', 'Малта', 'Мариански о-ви', 'Мароко', 'Мартиника', 'Маршалски о-ви', 'Мексико', 'Мианмар (Бирма)', 'Микронезия', 'Майот', 'Мозамбик', 'Молдова', 'Монако', 'Монголия', 'Монтсерат', 'Намибия', 'Науру', 'Непал', 'Неутрална зона', 'Нигер', 'Нигерия', 'Нидерландия (Холандия)', 'Нидерландски Антили', 'Никарагуа', 'Ниуе', 'Нова Заландия', 'Нова Келедония', 'Норвегия', 'Норфолк', 'Обединени арабски емирства', 'Оман', 'Остров Джърси (Великобритания)', 'Остров Кук', 'Остров Кюрасао', 'Остров Ман', 'о-ви Аланд', 'Пакистан', 'Палау', 'Палестина', 'Панама', 'Папуа - Нова Гвинея', 'Парагвай', 'Перу', 'Питкерн', 'Полша', 'Португалия', 'Пуерто Рико', 'Република Корея', 'Република Македония', 'Република Южна Африка', 'Реюнион', 'Рождественски о-ви', 'Руанда', 'Румъния', 'Русия', 'Салвадор', 'Самоа', 'Сан Марино', 'Санта Лусия', 'Сао Томе и Принсипи', 'Саудитска Арабия', 'САЩ', 'Свазиленд', 'Света Елена Остров', 'Сейнт Винсенти Гренадини', 'Сейнт Кристофър и Нейвис', 'Сейшелски о-ви', 'Сен Пиер и Микелон', 'Сенегал', 'Сиера Леоне', 'Сингапур', 'Сирия', 'Словашка Република', 'Словения', 'Соломонови о-ви', 'Сомалия', 'Суазиленд', 'Судан', 'Суринам', 'Сърбия', 'Таджикистан', 'Тайван', 'Тайланд', 'Танзания', 'Того', 'Токелау', 'Тонга', 'Тринидад и Тобаго', 'Тувалу', 'Тунис', 'Туркменистан', 'Турция', 'Търкс и Кайкос о-ви', 'Уганда', 'Узбекистан', 'Украйна', 'Унгария', 'Уолис и Футуна', 'Уругвай', 'Ферьорски о-ви', 'Фиджи', 'Филипини', 'Финландия', 'Фолкландски (Малвински) о-ви', 'Франция', 'Френска Полинезия', 'Френски южни територии', 'Хаити', 'Хондурас', 'Хонконг', 'Хърватско (893)', 'Хърд и Макдоналд, о-ви', 'Централна африканска република', 'Чад', 'Черна гора', 'Чешка република', 'Чили', 'Швейцария', 'Швеция', 'Шри Ланка', 'Южна Джорджия и Южни С-еви о-ви', 'Ямайка', 'Ян Майен', 'Япония']


valid_country_data = {
    'България': ['BG', 'BGR', 'Republic of Bulgaria'],
    'Австралия': ['AU', 'AUS', 'Commonwealth of Australia'],
    'Австрия': ['AT', 'AUT', 'Republic of Austria'],
    'Азербайджан': ['AZ', 'AZE', 'Republic of Azerbaijan'],
    'Албания': ['AL', 'ALB', 'Republic of Albania'],
    'Алжир': ['DZ', 'DZA', 'People\'s Democratic Republic of Algeria'],
    'Ангола': ['AO', 'AGO', 'Republic of Angola'],
    'Ангуила': ['AI', 'AIA', 'Anguilla'],
    'Андора': ['AD', 'AND', 'Principality of Andorra'],
    'Антарктида': ['AQ', 'ATA', 'Antarctica'],
    'Антигуа и Барбуда': ['AG', 'ATG', 'Antigua and Barbuda'],
    'Аржентина': ['AR', 'ARG', 'Argentine Republic'],
    'Армения': ['AM', 'ARM', 'Republic of Armenia'],
    'Аруба': ['AW', 'ABW', 'Aruba'],
    'Афганистан': ['AF', 'AFG', 'Islamic Republic of Afghanistan'],
    'Бангладеш': ['BD', 'BGD', 'People\'s Republic of Bangladesh'],
    'Барбадос': ['BB', 'BRB', 'Barbados'],
    'Бахамски о-ви': ['BS', 'BHS', 'Commonwealth of The Bahamas'],
    'Бахрейн': ['BH', 'BHR', 'Kingdom of Bahrain'],
    'Беларус': ['BY', 'BLR', 'Republic of Belarus'],
    'Белгия': ['BE', 'BEL', 'Kingdom of Belgium'],
    'Белиз': ['BZ', 'BLZ', 'Belize'],
    'Бенин': ['BJ', 'BEN', 'Republic of Benin'],
    'Бермудски о-ви': ['BM', 'BMU', 'Bermuda'],
    'Боливия': ['BO', 'BOL', 'Plurinational State of Bolivia'],
    'Босна и Херцеговина': ['BA', 'BIH', 'Bosnia and Herzegovina'],
    'Ботсуана': ['BW', 'BWA', 'Republic of Botswana'],
    'Бразилия': ['BR', 'BRA', 'Federative Republic of Brazil'],
    'Брит. територия в Индийския океан': ['IO', 'IOT', 'British Indian Ocean Territory'],
    'Бруней': ['BN', 'BRN', 'Nation of Brunei, the Abode of Peace'],
    'Буве': ['BV', 'BVT', 'Bouvet Island'],
    'Буркина фасо': ['BF', 'BFA', 'Burkina Faso'],
    'Бурунди': ['BI', 'BDI', 'Republic of Burundi'],
    'Бутан': ['BT', 'BTN', 'Kingdom of Bhutan'],
    'Вануату': ['VU', 'VUT', 'Republic of Vanuatu'],
    'Ватикана': ['VA', 'VAT', 'Vatican City State'],
    'Великобритания': ['GB', 'GBR', 'United Kingdom of Great Britain and Northern Ireland'],
    'Венецуела': ['VE', 'VEN', 'Bolivarian Republic of Venezuela'],
    'Виетнам': ['VN', 'VNM', 'Socialist Republic of Vietnam'],
    'Виржински о-ви (Брит.)': ['VG', 'VGB', 'British Virgin Islands'],
    'Виржински о-ви (САЩ)': ['VI', 'VIR', 'Virgin Islands, U.S.'],
    'Габон': ['GA', 'GAB', 'Gabonese Republic'],
    'Гамбия': ['GM', 'GMB', 'Republic of The Gambia'],
    'Гана': ['GH', 'GHA', 'Republic of Ghana'],
    'Гаяна': ['GY', 'GUY', 'Co-operative Republic of Guyana'],
    'Гваделупа': ['GP', 'GLP', 'Guadeloupe'],
    'Гватемала': ['GT', 'GTM', 'Republic of Guatemala'],
    'Гвинея': ['GN', 'GIN', 'Republic of Guinea'],
    'Гвинея-Бисау': ['GW', 'GNB', 'Republic of Guinea-Bissau'],
    'Германия': ['DE', 'DEU', 'Federal Republic of Germany'],
    'Гиана(Фр.)': ['GF', 'GUF', 'French Guiana'],
    'Гибралтар': ['GI', 'GIB', 'Gibraltar'],
    'Гренада': ['GD', 'GRD', 'Grenada'],
    'Гренландия': ['GL', 'GRL', 'Greenland'],
    'Грузия': ['GE', 'GEO', 'Georgia'],
    'Гуам': ['GU', 'GUM', 'Guam'],
    'Гърция': ['GR', 'GRC', 'Hellenic Republic'],
    'Дания': ['DK', 'DNK', 'Kingdom of Denmark'],
    'Джибути': ['DJ', 'DJI', 'Republic of Djibouti'],
    'Доминика': ['DM', 'DMA', 'Commonwealth of Dominica'],
    'Доминиканска република': ['DO', 'DOM', 'Dominican Republic'],
    'Египет': ['EG', 'EGY', 'Arab Republic of Egypt'],
    'Ейре (Ирландия)': ['IE', 'IRL', 'Ireland'],
    'Еквадор': ['EC', 'ECU', 'Republic of Ecuador'],
    'Екваториална Гвинея': ['GQ', 'GNQ', 'Republic of Equatorial Guinea'],
    'Еритрея': ['ER', 'ERI', 'State of Eritrea'],
    'Естония': ['EE', 'EST', 'Republic of Estonia'],
    'Етиопия': ['ET', 'ETH', 'Federal Democratic Republic of Ethiopia'],
    'Заир': ['ZR', 'ZAR', 'Zaire'],
    'Замбия': ['ZM', 'ZMB', 'Republic of Zambia'],
    'Западна Сахара': ['EH', 'ESH', 'Western Sahara'],
    'Зимбабве': ['ZW', 'ZWE', 'Republic of Zimbabwe'],
    'Израел': ['IL', 'ISR', 'State of Israel'],
    'Източен Тимор': ['TL', 'TLS', 'Democratic Republic of Timor-Leste'],
    'Източни Самоа (САЩ)': ['AS', 'ASM', 'American Samoa'],
    'Индия': ['IN', 'IND', 'Republic of India'],
    'Индонезия': ['ID', 'IDN', 'Republic of Indonesia'],
    'Ирак': ['IQ', 'IRQ', 'Republic of Iraq'],
    'Иран': ['IR', 'IRN', 'Islamic Republic of Iran'],
    'Ирландия': ['IE', 'IRL', 'Ireland'],
    'Исландия': ['IS', 'ISL', 'Republic of Iceland'],
    'Испания': ['ES', 'ESP', 'Kingdom of Spain'],
    'Италия': ['IT', 'ITA', 'Italian Republic'],
    'Йемен': ['YE', 'YEM', 'Republic of Yemen'],
    'Йордания': ['JO', 'JOR', 'Hashemite Kingdom of Jordan'],
    'Кабо Верде': ['CV', 'CPV', 'Republic of Cape Verde'],
    'Казахстан': ['KZ', 'KAZ', 'Republic of Kazakhstan'],
    'Кайманови о-ви': ['KY', 'CYM', 'Cayman Islands'],
    'Камбоджа': ['KH', 'KHM', 'Kingdom of Cambodia'],
    'Камерун': ['CM', 'CMR', 'Republic of Cameroon'],
    'Канада': ['CA', 'CAN', 'Canada'],
    'Катар': ['QA', 'QAT', 'State of Qatar'],
    'Кения': ['KE', 'KEN', 'Republic of Kenya'],
    'Кипър': ['CY', 'CYP', 'Republic of Cyprus'],
    'Киргизтан': ['KG', 'KGZ', 'Kyrgyz Republic'],
    'Кирибати': ['KI', 'KIR', 'Republic of Kiribati'],
    'Китай': ['CN', 'CHN', 'People\'s Republic of China'],
    'КНДР': ['KP', 'PRK', 'Democratic People\'s Republic of Korea'],
    'Кокосови о-ви': ['CC', 'CCK', 'Cocos (Keeling) Islands'],
    'Колумбия': ['CO', 'COL', 'Republic of Colombia'],
    'Коморски о-ви': ['KM', 'COM', 'Union of the Comoros'],
    'Конго': ['CG', 'COG', 'Republic of the Congo'],
    'Косово': ['XK', 'XKX', 'Republic of Kosovo'],
    'Коста Рика': ['CR', 'CRI', 'Republic of Costa Rica'],
    'Кот д`Ивоар': ['CI', 'CIV', 'Republic of Côte d\'Ivoire'],
    'Куба': ['CU', 'CUB', 'Republic of Cuba'],
    'Кувейт': ['KW', 'KWT', 'State of Kuwait'],
    'Лаос': ['LA', 'LAO', 'Lao People\'s Democratic Republic'],
    'Латвия ': ['LV', 'LVA', 'Republic of Latvia'],
    'Лесото': ['LS', 'LSO', 'Kingdom of Lesotho'],
    'Либерия': ['LR', 'LBR', 'Republic of Liberia'],
    'Либия': ['LY', 'LBY', 'Great Socialist People\'s Libyan Arab Jamahiriya'],
    'Ливан': ['LB', 'LBN', 'Lebanese Republic'],
    'Литва': ['LT', 'LTU', 'Republic of Lithuania'],
    'Лихтенщайн': ['LI', 'LIE', 'Principality of Liechtenstein'],
    'Люксембург': ['LU', 'LUX', 'Grand Duchy of Luxembourg'],
    'Мавритания': ['MR', 'MRT', 'Islamic Republic of Mauritania'],
    'Мавриций': ['MU', 'MUS', 'Republic of Mauritius'],
    'Мадагаскар': ['MG', 'MDG', 'Republic of Madagascar'],
    'Макао': ['MO', 'MAC', 'Macao Special Administrative Region'],
    'Малави': ['MW', 'MWI', 'Republic of Malawi'],
    'Малайзия': ['MY', 'MYS', 'Malaysia'],
    'Малдиви': ['MV', 'MDV', 'Republic of Maldives'],
    'Мали': ['ML', 'MLI', 'Republic of Mali'],
    'Малки далечни о-ви на САЩ': ['UM', 'UMI', 'United States Minor Outlying Islands'],
    'Малта': ['MT', 'MLT', 'Republic of Malta'],
    'Мариански о-ви': ['MP', 'MNP', 'Commonwealth of the Northern Mariana Islands'],
    'Мароко': ['MA', 'MAR', 'Kingdom of Morocco'],
    'Мартиника': ['MQ', 'MTQ', 'Martinique'],
    'Маршалски о-ви': ['MH', 'MHL', 'Republic of the Marshall Islands'],
    'Мексико': ['MX', 'MEX', 'United Mexican States'],
    'Мианмар (Бирма)': ['MM', 'MMR', 'Union of Myanmar'],
    'Микронезия': ['FM', 'FSM', 'Federated States of Micronesia'],
    'Майот': ['YT', 'MYT', 'Mayotte'],
    'Мозамбик': ['MZ', 'MOZ', 'Republic of Mozambique'],
    'Молдова': ['MD', 'MDA', 'Republic of Moldova'],
    'Монако': ['MC', 'MCO', 'Principality of Monaco'],
    'Монголия': ['MN', 'MNG', 'Mongolia'],
    'Монтсерат': ['MS', 'MSR', 'Montserrat'],
    'Намибия': ['NA', 'NAM', 'Republic of Namibia'],
    'Науру': ['NR', 'NRU', 'Republic of Nauru'],
    'Непал': ['NP', 'NPL', 'Federal Democratic Republic of Nepal'],
    'Неутрална зона': ['NT', 'NTZ', 'Neutral Zone'],
    'Нигер': ['NE', 'NER', 'Republic of the Niger'],
    'Нигерия': ['NG', 'NGA', 'Federal Republic of Nigeria'],
    'Нидерландия (Холандия)': ['NL', 'NLD', 'Kingdom of the Netherlands'],
    'Нидерландски Антили': ['AN', 'ANT', 'Netherlands Antilles'],
    'Никарагуа': ['NI', 'NIC', 'Republic of Nicaragua'],
    'Ниуе': ['NU', 'NIU', 'Niue'],
    'Нова Заландия': ['NZ', 'NZL', 'New Zealand'],
    'Нова Келедония': ['NC', 'NCL', 'New Caledonia'],
    'Норвегия': ['NO', 'NOR', 'Kingdom of Norway'],
    'Норфолк': ['NF', 'NFK', 'Norfolk Island'],
    'Обединени арабски емирства': ['AE', 'ARE', 'United Arab Emirates'],
    'Оман': ['OM', 'OMN', 'Sultanate of Oman'],
    'Остров Джърси (Великобритания)': ['JE', 'JEY', 'Jersey'],
    'Остров Кук': ['CK', 'COK', 'Cook Islands'],
    'Остров Кюрасао': ['CW', 'CUW', 'Curaçao'],
    'Остров Ман': ['IM', 'IMN', 'Isle of Man'],
    'о-ви Аланд': ['AX', 'ALA', 'Åland Islands'],
    'Пакистан': ['PK', 'PAK', 'Islamic Republic of Pakistan'],
    'Палау': ['PW', 'PLW', 'Republic of Palau'],
    'Палестина': ['PS', 'PSE', 'State of Palestine'],
    'Панама': ['PA', 'PAN', 'Republic of Panama'],
    'Папуа - Нова Гвинея': ['PG', 'PNG', 'Independent State of Papua New Guinea'],
    'Парагвай': ['PY', 'PRY', 'Republic of Paraguay'],
    'Перу': ['PE', 'PER', 'Republic of Peru'],
    'Питкерн': ['PN', 'PCN', 'Pitcairn Islands'],
    'Полша': ['PL', 'POL', 'Republic of Poland'],
    'Португалия': ['PT', 'PRT', 'Portuguese Republic'],
    'Пуерто Рико': ['PR', 'PRI', 'Commonwealth of Puerto Rico'],
    'Република Корея': ['KR', 'KOR', 'Republic of Korea'],
    'Република Македония': ['MK', 'MKD', 'Republic of North Macedonia'],
    'Република Южна Африка': ['ZA', 'ZAF', 'Republic of South Africa'],
    'Реюнион': ['RE', 'REU', 'Réunion'],
    'Рождественски о-ви': ['CX', 'CXR', 'Christmas Island'],
    'Руанда': ['RW', 'RWA', 'Republic of Rwanda'],
    'Румъния': ['RO', 'ROU', 'Romania'],
    'Русия': ['RU', 'RUS', 'Russian Federation'],
    'Салвадор': ['SV', 'SLV', 'Republic of El Salvador'],
    'Самоа': ['WS', 'WSM', 'Independent State of Samoa'],
    'Сан Марино': ['SM', 'SMR', 'Republic of San Marino'],
    'Санта Лусия': ['LC', 'LCA', 'Saint Lucia'],
    'Сао Томе и Принсипи': ['ST', 'STP', 'Democratic Republic of São Tomé and Príncipe'],
    'Саудитска Арабия': ['SA', 'SAU', 'Kingdom of Saudi Arabia'],
    'САЩ': ['US', 'USA', 'United States of America'],
    'Свазиленд': ['SZ', 'SWZ', 'Kingdom of Eswatini'],
    'Света Елена Остров': ['SH', 'SHN', 'Saint Helena, Ascension and Tristan da Cunha'],
    'Сейнт Винсенти Гренадини': ['VC', 'VCT', 'Saint Vincent and the Grenadines'],
    'Сейнт Кристофър и Нейвис': ['KN', 'KNA', 'Federation of Saint Kitts and Nevis'],
    'Сейшелски о-ви': ['SC', 'SYC', 'Republic of Seychelles'],
    'Сен Пиер и Микелон': ['PM', 'SPM', 'Saint Pierre and Miquelon'],
    'Сенегал': ['SN', 'SEN', 'Republic of Senegal'],
    'Сиера Леоне': ['SL', 'SLE', 'Republic of Sierra Leone'],
    'Сингапур': ['SG', 'SGP', 'Republic of Singapore'],
    'Сирия': ['SY', 'SYR', 'Syrian Arab Republic'],
    'Словашка Република': ['SK', 'SVK', 'Slovak Republic'],
    'Словения': ['SI', 'SVN', 'Republic of Slovenia'],
    'Соломонови о-ви': ['SB', 'SLB', 'Solomon Islands'],
    'Сомалия': ['SO', 'SOM', 'Somalia'],
    'Суазиленд': ['SZ', 'SWZ', 'Kingdom of Eswatini'],
    'Судан': ['SD', 'SDN', 'Republic of the Sudan'],
    'Суринам': ['SR', 'SUR', 'Republic of Suriname'],
    'Сърбия': ['RS', 'SRB', 'Republic of Serbia'],
    'Таджикистан': ['TJ', 'TJK', 'Republic of Tajikistan'],
    'Тайван': ['TW', 'TWN', 'Taiwan'],
    'Тайланд': ['TH', 'THA', 'Kingdom of Thailand'],
    'Танзания': ['TZ', 'TZA', 'United Republic of Tanzania'],
    'Того': ['TG', 'TGO', 'Togolese Republic'],
    'Токелау': ['TK', 'TKL', 'Tokelau'],
    'Тонга': ['TO', 'TON', 'Kingdom of Tonga'],
    'Тринидад и Тобаго': ['TT', 'TTO', 'Republic of Trinidad and Tobago'],
    'Тувалу': ['TV', 'TUV', 'Tuvalu'],
    'Тунис': ['TN', 'TUN', 'Republic of Tunisia'],
    'Туркменистан': ['TM', 'TKM', 'Turkmenistan'],
    'Турция': ['TR', 'TUR', 'Republic of Turkey'],
    'Търкс и Кайкос о-ви': ['TC', 'TCA', 'Turks and Caicos Islands'],
    'Уганда': ['UG', 'UGA', 'Republic of Uganda'],
    'Узбекистан': ['UZ', 'UZB', 'Republic of Uzbekistan'],
    'Украйна': ['UA', 'UKR', 'Ukraine'],
    'Унгария': ['HU', 'HUN', 'Hungary'],
    'Уолис и Футуна': ['WF', 'WLF', 'Wallis and Futuna'],
    'Уругвай': ['UY', 'URY', 'Eastern Republic of Uruguay'],
    'Ферьорски о-ви': ['FO', 'FRO', 'Faroe Islands'],
    'Фиджи': ['FJ', 'FJI', 'Republic of Fiji'],
    'Филипини': ['PH', 'PHL', 'Republic of the Philippines'],
    'Финландия': ['FI', 'FIN', 'Republic of Finland'],
    'Фолкландски (Малвински) о-ви': ['FK', 'FLK', 'Falkland Islands (Malvinas)'],
    'Франция': ['FR', 'FRA', 'French Republic'],
    'Френска Полинезия': ['PF', 'PYF', 'French Polynesia'],
    'Френски южни територии': ['TF', 'ATF', 'French Southern Territories'],
    'Хаити': ['HT', 'HTI', 'Republic of Haiti'],
    'Хондурас': ['HN', 'HND', 'Republic of Honduras'],
    'Хонконг': ['HK', 'HKG', 'Hong Kong Special Administrative Region'],
    'Хърватско (893)': ['HR', 'HRV', 'Republic of Croatia'],
    'Хърд и Макдоналд, о-ви': ['HM', 'HMD', 'Heard Island and McDonald Islands'],
    'Централна африканска република': ['CF', 'CAF', 'Central African Republic'],
    'Чад': ['TD', 'TCD', 'Republic of Chad'],
    'Черна гора': ['ME', 'MNE', 'Montenegro'],
    'Чешка република': ['CZ', 'CZE', 'Czech Republic'],
    'Чили': ['CL', 'CHL', 'Republic of Chile'],
    'Швейцария': ['CH', 'CHE', 'Swiss Confederation'],
    'Швеция': ['SE', 'SWE', 'Kingdom of Sweden'],
    'Шри Ланка': ['LK', 'LKA', 'Democratic Socialist Republic of Sri Lanka'],
    'Южна Джорджия и Южни С-еви о-ви': ['GS', 'SGS', 'South Georgia and the South Sandwich Islands'],
    'Ямайка': ['JM', 'JAM', 'Jamaica'],
    'Ян Майен': ['PM', 'SPM', 'Saint Pierre and Miquelon'],
    'Япония': ['JP', 'JPN', 'Japan']}

valid_country_data_full_name_and_abbr = {
    'България': {
        'full_name': 'Republic of Bulgaria',
        'alpha_2': 'BG',
        'alpha_3': 'BGR'
    },
    'Австралия': {
        'full_name': 'Commonwealth of Australia',
        'alpha_2': 'AU',
        'alpha_3': 'AUS'
    },
    'Австрия': {
        'full_name': 'Republic of Austria',
        'alpha_2': 'AT',
        'alpha_3': 'AUT'
    },
    'Азербайджан': {
        'full_name': 'Republic of Azerbaijan',
        'alpha_2': 'AZ',
        'alpha_3': 'AZE'
    },
    'Албания': {
        'full_name': 'Republic of Albania',
        'alpha_2': 'AL',
        'alpha_3': 'ALB'
    },
    'Алжир': {
        'full_name': 'People\'s Democratic Republic of Algeria',
        'alpha_2': 'DZ',
        'alpha_3': 'DZA'
    },
    'Ангола': {
        'full_name': 'Republic of Angola',
        'alpha_2': 'AO',
        'alpha_3': 'AGO'
    },
    'Ангуила': {
        'full_name': 'Anguilla',
        'alpha_2': 'AI',
        'alpha_3': 'AIA'
    },
    'Андора': {
        'full_name': 'Principality of Andorra',
        'alpha_2': 'AD',
        'alpha_3': 'AND'
    },
    'Антарктида': {
        'full_name': 'Antarctica',
        'alpha_2': 'AQ',
        'alpha_3': 'ATA'
    },
    'Антигуа и Барбуда': {
        'full_name': 'Antigua and Barbuda',
        'alpha_2': 'AG',
        'alpha_3': 'ATG'
    },
    'Аржентина': {
        'full_name': 'Argentine Republic',
        'alpha_2': 'AR',
        'alpha_3': 'ARG'
    },
    'Армения': {
        'full_name': 'Republic of Armenia',
        'alpha_2': 'AM',
        'alpha_3': 'ARM'
    },
    'Аруба': {
        'full_name': 'Aruba',
        'alpha_2': 'AW',
        'alpha_3': 'ABW'
    },
    'Афганистан': {
        'full_name': 'Islamic Republic of Afghanistan',
        'alpha_2': 'AF',
        'alpha_3': 'AFG'
    },
    'Бангладеш': {
        'full_name': 'People\'s Republic of Bangladesh',
        'alpha_2': 'BD',
        'alpha_3': 'BGD'
    },
    'Барбадос': {
        'full_name': 'Barbados',
        'alpha_2': 'BB',
        'alpha_3': 'BRB'
    },
    'Бахамски о-ви': {
        'full_name': 'Commonwealth of The Bahamas',
        'alpha_2': 'BS',
        'alpha_3': 'BHS'
    },
    'Бахрейн': {
        'full_name': 'Kingdom of Bahrain',
        'alpha_2': 'BH',
        'alpha_3': 'BHR'
    },
    'Беларус': {
        'full_name': 'Republic of Belarus',
        'alpha_2': 'BY',
        'alpha_3': 'BLR'
    },
    'Белгия': {
        'full_name': 'Kingdom of Belgium',
        'alpha_2': 'BE',
        'alpha_3': 'BEL'
    },
    'Белиз': {
        'full_name': 'Belize',
        'alpha_2': 'BZ',
        'alpha_3': 'BLZ'
    },
    'Бенин': {
        'full_name': 'Republic of Benin',
        'alpha_2': 'BJ',
        'alpha_3': 'BEN'
    },
    'Бермудски о-ви': {
        'full_name': 'Bermuda',
        'alpha_2': 'BM',
        'alpha_3': 'BMU'
    },
    'Боливия': {
        'full_name': 'Plurinational State of Bolivia',
        'alpha_2': 'BO',
        'alpha_3': 'BOL'
    },
    'Босна и Херцеговина': {
        'full_name': 'Bosnia and Herzegovina',
        'alpha_2': 'BA',
        'alpha_3': 'BIH'
    },
    'Ботсуана': {
        'full_name': 'Republic of Botswana',
        'alpha_2': 'BW',
        'alpha_3': 'BWA'
    },
    'Бразилия': {
        'full_name': 'Federative Republic of Brazil',
        'alpha_2': 'BR',
        'alpha_3': 'BRA'
    },
    'Брит. територия в Индийския океан': {
        'full_name': 'British Indian Ocean Territory',
        'alpha_2': 'IO',
        'alpha_3': 'IOT'
    },
    'Бруней': {
        'full_name': 'Nation of Brunei, Abode of Peace',
        'alpha_2': 'BN',
        'alpha_3': 'BRN'
    },
    'Буве': {
        'full_name': 'Bouvet Island',
        'alpha_2': 'BV',
        'alpha_3': 'BVT'
    },
    'Буркина фасо': {
        'full_name': 'Burkina Faso',
        'alpha_2': 'BF',
        'alpha_3': 'BFA'
    },
    'Бурунди': {
        'full_name': 'Republic of Burundi',
        'alpha_2': 'BI',
        'alpha_3': 'BDI'
    },
    'Бутан': {
        'full_name': 'Kingdom of Bhutan',
        'alpha_2': 'BT',
        'alpha_3': 'BTN'
    },
    'Вануату': {
        'full_name': 'Republic of Vanuatu',
        'alpha_2': 'VU',
        'alpha_3': 'VUT'
    },
    'Ватикана': {
        'full_name': 'Vatican City State',
        'alpha_2': 'VA',
        'alpha_3': 'VAT'
    },
    'Великобритания': {
        'full_name': 'United Kingdom of Great Britain and Northern Ireland',
        'alpha_2': 'GB',
        'alpha_3': 'GBR'
    },
    'Венецуела': {
        'full_name': 'Bolivarian Republic of Venezuela',
        'alpha_2': 'VE',
        'alpha_3': 'VEN'
    },
    'Виетнам': {
        'full_name': 'Socialist Republic of Vietnam',
        'alpha_2': 'VN',
        'alpha_3': 'VNM'
    },
    'Виржински о-ви (Брит.)': {
        'full_name': 'British Virgin Islands',
        'alpha_2': 'VG',
        'alpha_3': 'VGB'
    },
    'Виржински о-ви (САЩ)': {
        'full_name': 'Virgin Islands of the United States',
        'alpha_2': 'VI',
        'alpha_3': 'VIR'
    },
    'Габон': {
        'full_name': 'Gabonese Republic',
        'alpha_2': 'GA',
        'alpha_3': 'GAB'
    },
    'Гамбия': {
        'full_name': 'Republic of The Gambia',
        'alpha_2': 'GM',
        'alpha_3': 'GMB'
    },
    'Гана': {
        'full_name': 'Republic of Ghana',
        'alpha_2': 'GH',
        'alpha_3': 'GHA'
    },
    'Гаяна': {
        'full_name': 'Co-operative Republic of Guyana',
        'alpha_2': 'GY',
        'alpha_3': 'GUY'
    },
    'Гваделупа': {
        'full_name': 'Guadeloupe',
        'alpha_2': 'GP',
        'alpha_3': 'GLP'
    },
    'Гватемала': {
        'full_name': 'Republic of Guatemala',
        'alpha_2': 'GT',
        'alpha_3': 'GTM'
    },
    'Гвинея': {
        'full_name': 'Republic of Guinea',
        'alpha_2': 'GN',
        'alpha_3': 'GIN'
    },
    'Гвинея-Бисау': {
        'full_name': 'Republic of Guinea-Bissau',
        'alpha_2': 'GW',
        'alpha_3': 'GNB'
    },
    'Германия': {
        'full_name': 'Federal Republic of Germany',
        'alpha_2': 'DE',
        'alpha_3': 'DEU'
    },
    'Гиана(Фр.)': {
        'full_name': 'French Guiana',
        'alpha_2': 'GF',
        'alpha_3': 'GUF'
    },
    'Гибралтар': {
        'full_name': 'Gibraltar',
        'alpha_2': 'GI',
        'alpha_3': 'GIB'
    },
    'Гренада': {
        'full_name': 'Grenada',
        'alpha_2': 'GD',
        'alpha_3': 'GRD'
    },
    'Гренландия': {
        'full_name': 'Greenland',
        'alpha_2': 'GL',
        'alpha_3': 'GRL'
    },
    'Грузия': {
        'full_name': 'Georgia',
        'alpha_2': 'GE',
        'alpha_3': 'GEO'
    },
    'Гуам': {
        'full_name': 'Guam',
        'alpha_2': 'GU',
        'alpha_3': 'GUM'
    },
    'Гърция': {
        'full_name': 'Hellenic Republic',
        'alpha_2': 'GR',
        'alpha_3': 'GRC'
    },
    'Дания': {
        'full_name': 'Kingdom of Denmark',
        'alpha_2': 'DK',
        'alpha_3': 'DNK'
    },
    'Джибути': {
        'full_name': 'Republic of Djibouti',
        'alpha_2': 'DJ',
        'alpha_3': 'DJI'
    },
    'Доминика': {
        'full_name': 'Commonwealth of Dominica',
        'alpha_2': 'DM',
        'alpha_3': 'DMA'
    },
    'Доминиканска република': {
        'full_name': 'Dominican Republic',
        'alpha_2': 'DO',
        'alpha_3': 'DOM'
    },
    'Египет': {
        'full_name': 'Arab Republic of Egypt',
        'alpha_2': 'EG',
        'alpha_3': 'EGY'
    },
    'Ейре (Ирландия)': {
        'full_name': 'Ireland',
        'alpha_2': 'IE',
        'alpha_3': 'IRL'
    },
    'Еквадор': {
        'full_name': 'Republic of Ecuador',
        'alpha_2': 'EC',
        'alpha_3': 'ECU'
    },
    'Екваториална Гвинея': {
        'full_name': 'Republic of Equatorial Guinea',
        'alpha_2': 'GQ',
        'alpha_3': 'GNQ'
    },
    'Еритрея': {
        'full_name': 'State of Eritrea',
        'alpha_2': 'ER',
        'alpha_3': 'ERI'
    },
    'Естония': {
        'full_name': 'Republic of Estonia',
        'alpha_2': 'EE',
        'alpha_3': 'EST'
    },
    'Етиопия': {
        'full_name': 'Federal Democratic Republic of Ethiopia',
        'alpha_2': 'ET',
        'alpha_3': 'ETH'
    },
    'Заир': {
        'full_name': 'Republic of Zaire',
        'alpha_2': 'ZR',
        'alpha_3': 'ZAR'
    },
    'Замбия': {
        'full_name': 'Republic of Zambia',
        'alpha_2': 'ZM',
        'alpha_3': 'ZMB'
    },
    'Западна Сахара': {
        'full_name': 'Sahrawi Arab Democratic Republic',
        'alpha_2': 'EH',
        'alpha_3': 'ESH'
    },
    'Зимбабве': {
        'full_name': 'Republic of Zimbabwe',
        'alpha_2': 'ZW',
        'alpha_3': 'ZWE'
    },
    'Израел': {
        'full_name': 'State of Israel',
        'alpha_2': 'IL',
        'alpha_3': 'ISR'
    },
    'Източен Тимор': {
        'full_name': 'Democratic Republic of Timor-Leste',
        'alpha_2': 'TL',
        'alpha_3': 'TLS'
    },
    'Източни Самоа (САЩ)': {
        'full_name': 'American Samoa',
        'alpha_2': 'AS',
        'alpha_3': 'ASM'
    },
    'Индия': {
        'full_name': 'Republic of India',
        'alpha_2': 'IN',
        'alpha_3': 'IND'
    },
    'Индонезия': {
        'full_name': 'Republic of Indonesia',
        'alpha_2': 'ID',
        'alpha_3': 'IDN'
    },
    'Ирак': {
        'full_name': 'Republic of Iraq',
        'alpha_2': 'IQ',
        'alpha_3': 'IRQ'
    },
    'Иран': {
        'full_name': 'Islamic Republic of Iran',
        'alpha_2': 'IR',
        'alpha_3': 'IRN'
    },
    'Ирландия': {
        'full_name': 'Ireland',
        'alpha_2': 'IE',
        'alpha_3': 'IRL'
    },
    'Исландия': {
        'full_name': 'Republic of Iceland',
        'alpha_2': 'IS',
        'alpha_3': 'ISL'
    },
    'Испания': {
        'full_name': 'Kingdom of Spain',
        'alpha_2': 'ES',
        'alpha_3': 'ESP'
    },
    'Италия': {
        'full_name': 'Italian Republic',
        'alpha_2': 'IT',
        'alpha_3': 'ITA'
    },
    'Йемен': {
        'full_name': 'Republic of Yemen',
        'alpha_2': 'YE',
        'alpha_3': 'YEM'
    },
    'Йордания': {
        'full_name': 'Hashemite Kingdom of Jordan',
        'alpha_2': 'JO',
        'alpha_3': 'JOR'
    },
    'Кабо Верде': {
        'full_name': 'Republic of Cabo Verde',
        'alpha_2': 'CV',
        'alpha_3': 'CPV'
    },
    'Казахстан': {
        'full_name': 'Republic of Kazakhstan',
        'alpha_2': 'KZ',
        'alpha_3': 'KAZ'
    },
    'Кайманови о-ви': {
        'full_name': 'Cayman Islands',
        'alpha_2': 'KY',
        'alpha_3': 'CYM'
    },
    'Камбоджа': {
        'full_name': 'Kingdom of Cambodia',
        'alpha_2': 'KH',
        'alpha_3': 'KHM'
    },
    'Камерун': {
        'full_name': 'Republic of Cameroon',
        'alpha_2': 'CM',
        'alpha_3': 'CMR'
    },
    'Канада': {
        'full_name': 'Canada',
        'alpha_2': 'CA',
        'alpha_3': 'CAN'
    },
    'Катар': {
        'full_name': 'State of Qatar',
        'alpha_2': 'QA',
        'alpha_3': 'QAT'
    },
    'Кения': {
        'full_name': 'Republic of Kenya',
        'alpha_2': 'KE',
        'alpha_3': 'KEN'
    },
    'Кипър': {
        'full_name': 'Republic of Cyprus',
        'alpha_2': 'CY',
        'alpha_3': 'CYP'
    },
    'Киргизтан': {
        'full_name': 'Kyrgyz Republic',
        'alpha_2': 'KG',
        'alpha_3': 'KGZ'
    },
    'Кирибати': {
        'full_name': 'Republic of Kiribati',
        'alpha_2': 'KI',
        'alpha_3': 'KIR'
    },
    'Китай': {
        'full_name': 'People\'s Republic of China',
        'alpha_2': 'CN',
        'alpha_3': 'CHN'
    },
    'КНДР': {
        'full_name': 'Democratic People\'s Republic of Korea',
        'alpha_2': 'KP',
        'alpha_3': 'PRK'
    },
    'Кокосови о-ви': {
        'full_name': 'Cocos (Keeling) Islands',
        'alpha_2': 'CC',
        'alpha_3': 'CCK'
    },
    'Колумбия': {
        'full_name': 'Republic of Colombia',
        'alpha_2': 'CO',
        'alpha_3': 'COL'
    },
    'Коморски о-ви': {
        'full_name': 'Union of the Comoros',
        'alpha_2': 'KM',
        'alpha_3': 'COM'
    },
    'Конго': {
        'full_name': 'Democratic Republic of the Congo',
        'alpha_2': 'CD',
        'alpha_3': 'COD'
    },
    'Косово': {
        'full_name': 'Republic of Kosovo',
        'alpha_2': 'XK',
        'alpha_3': 'XKX'
    },
    'Коста Рика': {
        'full_name': 'Republic of Costa Rica',
        'alpha_2': 'CR',
        'alpha_3': 'CRI'
    },
    'Кот д`Ивоар': {
        'full_name': 'Republic of Côte d\'Ivoire',
        'alpha_2': 'CI',
        'alpha_3': 'CIV'
    },
    'Куба': {
        'full_name': 'Republic of Cuba',
        'alpha_2': 'CU',
        'alpha_3': 'CUB'
    },
    'Кувейт': {
        'full_name': 'State of Kuwait',
        'alpha_2': 'KW',
        'alpha_3': 'KWT'
    },
    'Лаос': {
        'full_name': 'Lao People\'s Democratic Republic',
        'alpha_2': 'LA',
        'alpha_3': 'LAO'
    },
    'Латвия': {
        'full_name': 'Republic of Latvia',
        'alpha_2': 'LV',
        'alpha_3': 'LVA'
    },
    'Лесото': {
        'full_name': 'Kingdom of Lesotho',
        'alpha_2': 'LS',
        'alpha_3': 'LSO'
    },
    'Либерия': {
        'full_name': 'Republic of Liberia',
        'alpha_2': 'LR',
        'alpha_3': 'LBR'
    },
    'Либия': {
        'full_name': 'State of Libya',
        'alpha_2': 'LY',
        'alpha_3': 'LBY'
    },
    'Ливан': {
        'full_name': 'Lebanese Republic',
        'alpha_2': 'LB',
        'alpha_3': 'LBN'
    },
    'Литва': {
        'full_name': 'Republic of Lithuania',
        'alpha_2': 'LT',
        'alpha_3': 'LTU'
    },
    'Лихтенщайн': {
        'full_name': 'Principality of Liechtenstein',
        'alpha_2': 'LI',
        'alpha_3': 'LIE'
    },
    'Люксембург': {
        'full_name': 'Grand Duchy of Luxembourg',
        'alpha_2': 'LU',
        'alpha_3': 'LUX'
    },
    'Мавритания': {
        'full_name': 'Islamic Republic of Mauritania',
        'alpha_2': 'MR',
        'alpha_3': 'MRT'
    },
    'Мавриций': {
        'full_name': 'Republic of Mauritius',
        'alpha_2': 'MU',
        'alpha_3': 'MUS'
    },
    'Мадагаскар': {
        'full_name': 'Republic of Madagascar',
        'alpha_2': 'MG',
        'alpha_3': 'MDG'
    },
    'Макао': {
        'full_name': 'Macao Special Administrative Region of the People\'s Republic of China',
        'alpha_2': 'MO',
        'alpha_3': 'MAC'
    },
    'Малави': {
        'full_name': 'Republic of Malawi',
        'alpha_2': 'MW',
        'alpha_3': 'MWI'
    },
    'Малайзия': {
        'full_name': 'Malaysia',
        'alpha_2': 'MY',
        'alpha_3': 'MYS'
    },
    'Малдиви': {
        'full_name': 'Republic of Maldives',
        'alpha_2': 'MV',
        'alpha_3': 'MDV'
    },
    'Мали': {
        'full_name': 'Republic of Mali',
        'alpha_2': 'ML',
        'alpha_3': 'MLI'
    },
    'Малки далечни о-ви на САЩ': {
        'full_name': 'United States Minor Outlying Islands',
        'alpha_2': 'UM',
        'alpha_3': 'UMI'
    },
    'Малта': {
        'full_name': 'Republic of Malta',
        'alpha_2': 'MT',
        'alpha_3': 'MLT'
    },
    'Мариански о-ви': {
        'full_name': 'Commonwealth of the Northern Mariana Islands',
        'alpha_2': 'MP',
        'alpha_3': 'MNP'
    },
    'Мароко': {
        'full_name': 'Kingdom of Morocco',
        'alpha_2': 'MA',
        'alpha_3': 'MAR'
    },
    'Мартиника': {
        'full_name': 'Martinique',
        'alpha_2': 'MQ',
        'alpha_3': 'MTQ'
    },
    'Маршалски о-ви': {
        'full_name': 'Republic of the Marshall Islands',
        'alpha_2': 'MH',
        'alpha_3': 'MHL'
    },
    'Мексико': {
        'full_name': 'United Mexican States',
        'alpha_2': 'MX',
        'alpha_3': 'MEX'
    },
    'Мианмар (Бирма)': {
        'full_name': 'Republic of the Union of Myanmar',
        'alpha_2': 'MM',
        'alpha_3': 'MMR'
    },
    'Микронезия': {
        'full_name': 'Federated States of Micronesia',
        'alpha_2': 'FM',
        'alpha_3': 'FSM'
    },
    'Майот': {
        'full_name': 'Department of Mayotte',
        'alpha_2': 'YT',
        'alpha_3': 'MYT'
    },
    'Мозамбик': {
        'full_name': 'Republic of Mozambique',
        'alpha_2': 'MZ',
        'alpha_3': 'MOZ'
    },
    'Молдова': {
        'full_name': 'Republic of Moldova',
        'alpha_2': 'MD',
        'alpha_3': 'MDA'
    },
    'Монако': {
        'full_name': 'Principality of Monaco',
        'alpha_2': 'MC',
        'alpha_3': 'MCO'
    },
    'Монголия': {
        'full_name': 'Mongolia',
        'alpha_2': 'MN',
        'alpha_3': 'MNG'
    },
    'Монтсерат': {
        'full_name': 'Montserrat',
        'alpha_2': 'MS',
        'alpha_3': 'MSR'
    },
    'Намибия': {
        'full_name': 'Republic of Namibia',
        'alpha_2': 'NA',
        'alpha_3': 'NAM'
    },
    'Науру': {
        'full_name': 'Republic of Nauru',
        'alpha_2': 'NR',
        'alpha_3': 'NRU'
    },
    'Непал': {
        'full_name': 'Federal Democratic Republic of Nepal',
        'alpha_2': 'NP',
        'alpha_3': 'NPL'
    },
    'Неутрална зона': {
        'full_name': 'Neutral Zone',
        'alpha_2': 'NT',
        'alpha_3': 'NTZ'
    },
    'Нигер': {
        'full_name': 'Republic of Niger',
        'alpha_2': 'NE',
        'alpha_3': 'NER'
    },
    'Нигерия': {
        'full_name': 'Federal Republic of Nigeria',
        'alpha_2': 'NG',
        'alpha_3': 'NGA'
    },
    'Нидерландия (Холандия)': {
        'full_name': 'Kingdom of the Netherlands',
        'alpha_2': 'NL',
        'alpha_3': 'NLD'
    },
    'Нидерландски Антили': {
        'full_name': 'Netherlands Antilles',
        'alpha_2': 'AN',
        'alpha_3': 'ANT'
    },
    'Никарагуа': {
        'full_name': 'Republic of Nicaragua',
        'alpha_2': 'NI',
        'alpha_3': 'NIC'
    },
    'Ниуе': {
        'full_name': 'Niue',
        'alpha_2': 'NU',
        'alpha_3': 'NIU'
    },
    'Нова Заландия': {
        'full_name': 'New Zealand',
        'alpha_2': 'NZ',
        'alpha_3': 'NZL'
    },
    'Нова Келедония': {
        'full_name': 'New Caledonia',
        'alpha_2': 'NC',
        'alpha_3': 'NCL'
    },
    'Норвегия': {
        'full_name': 'Kingdom of Norway',
        'alpha_2': 'NO',
        'alpha_3': 'NOR'
    },
    'Норфолк': {
        'full_name': 'Norfolk Island',
        'alpha_2': 'NF',
        'alpha_3': 'NFK'
    },
    'Обединени арабски емирства': {
        'full_name': 'United Arab Emirates',
        'alpha_2': 'AE',
        'alpha_3': 'ARE'
    },
    'Оман': {
        'full_name': 'Sultanate of Oman',
        'alpha_2': 'OM',
        'alpha_3': 'OMN'
    },
    'Остров Джърси (Великобритания)': {
        'full_name': 'Jersey',
        'alpha_2': 'JE',
        'alpha_3': 'JEY'
    },
    'Остров Кук': {
        'full_name': 'Cook Islands',
        'alpha_2': 'CK',
        'alpha_3': 'COK'
    },
    'Остров Кюрасао': {
        'full_name': 'Curaçao',
        'alpha_2': 'CW',
        'alpha_3': 'CUW'
    },
    'Остров Ман': {
        'full_name': 'Isle of Man',
        'alpha_2': 'IM',
        'alpha_3': 'IMN'
    },
    'о-ви Аланд': {
        'full_name': 'Åland Islands',
        'alpha_2': 'AX',
        'alpha_3': 'ALA'
    },
    'Пакистан': {
        'full_name': 'Islamic Republic of Pakistan',
        'alpha_2': 'PK',
        'alpha_3': 'PAK'
    },
    'Палау': {
        'full_name': 'Republic of Palau',
        'alpha_2': 'PW',
        'alpha_3': 'PLW'
    },
    'Палестина': {
        'full_name': 'State of Palestine',
        'alpha_2': 'PS',
        'alpha_3': 'PSE'
    },
    'Панама': {
        'full_name': 'Republic of Panama',
        'alpha_2': 'PA',
        'alpha_3': 'PAN'
    },
    'Папуа - Нова Гвинея': {
        'full_name': 'Independent State of Papua New Guinea',
        'alpha_2': 'PG',
        'alpha_3': 'PNG'
    },
    'Парагвай': {
        'full_name': 'Republic of Paraguay',
        'alpha_2': 'PY',
        'alpha_3': 'PRY'
    },
    'Перу': {
        'full_name': 'Republic of Peru',
        'alpha_2': 'PE',
        'alpha_3': 'PER'
    },
    'Питкерн': {
        'full_name': 'Pitcairn Islands',
        'alpha_2': 'PN',
        'alpha_3': 'PCN'
    },
    'Полша': {
        'full_name': 'Republic of Poland',
        'alpha_2': 'PL',
        'alpha_3': 'POL'
    },
    'Португалия': {
        'full_name': 'Portuguese Republic',
        'alpha_2': 'PT',
        'alpha_3': 'PRT'
    },
    'Пуерто Рико': {
        'full_name': 'Commonwealth of Puerto Rico',
        'alpha_2': 'PR',
        'alpha_3': 'PRI'
    },
    'Република Корея': {
        'full_name': 'Republic of Korea',
        'alpha_2': 'KR',
        'alpha_3': 'KOR'
    },
    'Република Македония': {
        'full_name': 'Republic of North Macedonia',
        'alpha_2': 'MK',
        'alpha_3': 'MKD'
    },
    'Република Южна Африка': {
        'full_name': 'Republic of South Africa',
        'alpha_2': 'ZA',
        'alpha_3': 'ZAF'
    },
    'Реюнион': {
        'full_name': 'Réunion',
        'alpha_2': 'RE',
        'alpha_3': 'REU'
    },
    'Рождественски о-ви': {
        'full_name': 'Territory of Christmas Island',
        'alpha_2': 'CX',
        'alpha_3': 'CXR'
    },
    'Руанда': {
        'full_name': 'Republic of Rwanda',
        'alpha_2': 'RW',
        'alpha_3': 'RWA'
    },
    'Румъния': {
        'full_name': 'Romania',
        'alpha_2': 'RO',
        'alpha_3': 'ROU'
    },
    'Русия': {
        'full_name': 'Russian Federation',
        'alpha_2': 'RU',
        'alpha_3': 'RUS'
    },
    'Салвадор': {
        'full_name': 'Republic of El Salvador',
        'alpha_2': 'SV',
        'alpha_3': 'SLV'
    },
    'Самоа': {
        'full_name': 'Independent State of Samoa',
        'alpha_2': 'WS',
        'alpha_3': 'WSM'
    },
    'Сан Марино': {
        'full_name': 'Republic of San Marino',
        'alpha_2': 'SM',
        'alpha_3': 'SMR'
    },
    'Санта Лусия': {
        'full_name': 'Saint Lucia',
        'alpha_2': 'LC',
        'alpha_3': 'LCA'
    },
    'Сао Томе и Принсипи': {
        'full_name': 'Democratic Republic of Sao Tome and Principe',
        'alpha_2': 'ST',
        'alpha_3': 'STP'
    },
    'Саудитска Арабия': {
        'full_name': 'Kingdom of Saudi Arabia',
        'alpha_2': 'SA',
        'alpha_3': 'SAU'
    },
    'САЩ': {
        'full_name': 'United States of America',
        'alpha_2': 'US',
        'alpha_3': 'USA'
    },
    'Свазиленд': {
        'full_name': 'Kingdom of Eswatini',
        'alpha_2': 'SZ',
        'alpha_3': 'SWZ'
    },
    'Света Елена Остров': {
        'full_name': 'Saint Helena, Ascension and Tristan da Cunha',
        'alpha_2': 'SH',
        'alpha_3': 'SHN'
    },
    'Сейнт Винсенти Гренадини': {
        'full_name': 'Saint Vincent and the Grenadines',
        'alpha_2': 'VC',
        'alpha_3': 'VCT'
    },
    'Сейнт Кристофър и Нейвис': {
        'full_name': 'Saint Kitts and Nevis',
        'alpha_2': 'KN',
        'alpha_3': 'KNA'
    },
    'Сейшелски о-ви': {
        'full_name': 'Republic of Seychelles',
        'alpha_2': 'SC',
        'alpha_3': 'SYC'
    },
    'Сен Пиер и Микелон': {
        'full_name': 'Saint Pierre and Miquelon',
        'alpha_2': 'PM',
        'alpha_3': 'SPM'
    },
    'Сенегал': {
        'full_name': 'Republic of Senegal',
        'alpha_2': 'SN',
        'alpha_3': 'SEN'
    },
    'Сиера Леоне': {
        'full_name': 'Republic of Sierra Leone',
        'alpha_2': 'SL',
        'alpha_3': 'SLE'
    },
    'Сингапур': {
        'full_name': 'Republic of Singapore',
        'alpha_2': 'SG',
        'alpha_3': 'SGP'
    },
    'Сирия': {
        'full_name': 'Syrian Arab Republic',
        'alpha_2': 'SY',
        'alpha_3': 'SYR'
    },
    'Словашка Република': {
        'full_name': 'Slovak Republic',
        'alpha_2': 'SK',
        'alpha_3': 'SVK'
    },
    'Словения': {
        'full_name': 'Republic of Slovenia',
        'alpha_2': 'SI',
        'alpha_3': 'SVN'
    },
    'Соломонови о-ви': {
        'full_name': 'Solomon Islands',
        'alpha_2': 'SB',
        'alpha_3': 'SLB'
    },
    'Сомалия': {
        'full_name': 'Federal Republic of Somalia',
        'alpha_2': 'SO',
        'alpha_3': 'SOM'
    },
    'Суазиленд': {
        'full_name': 'Kingdom of Eswatini',
        'alpha_2': 'SZ',
        'alpha_3': 'SWZ'
    },
    'Судан': {
        'full_name': 'Republic of the Sudan',
        'alpha_2': 'SD',
        'alpha_3': 'SDN'
    },
    'Суринам': {
        'full_name': 'Republic of Suriname',
        'alpha_2': 'SR',
        'alpha_3': 'SUR'
    },
    'Сърбия': {
        'full_name': 'Republic of Serbia',
        'alpha_2': 'RS',
        'alpha_3': 'SRB'
    },
    'Таджикистан': {
        'full_name': 'Republic of Tajikistan',
        'alpha_2': 'TJ',
        'alpha_3': 'TJK'
    },
    'Тайван': {
        'full_name': 'Taiwan, Province of China',
        'alpha_2': 'TW',
        'alpha_3': 'TWN'
    },
    'Тайланд': {
        'full_name': 'Kingdom of Thailand',
        'alpha_2': 'TH',
        'alpha_3': 'THA'
    },
    'Танзания': {
        'full_name': 'United Republic of Tanzania',
        'alpha_2': 'TZ',
        'alpha_3': 'TZA'
    },
    'Того': {
        'full_name': 'Togolese Republic',
        'alpha_2': 'TG',
        'alpha_3': 'TGO'
    },
    'Токелау': {
        'full_name': 'Tokelau',
        'alpha_2': 'TK',
        'alpha_3': 'TKL'
    },
    'Тонга': {
        'full_name': 'Kingdom of Tonga',
        'alpha_2': 'TO',
        'alpha_3': 'TON'
    },
    'Тринидад и Тобаго': {
        'full_name': 'Republic of Trinidad and Tobago',
        'alpha_2': 'TT',
        'alpha_3': 'TTO'
    },
    'Тувалу': {
        'full_name': 'Tuvalu',
        'alpha_2': 'TV',
        'alpha_3': 'TUV'
    },
    'Тунис': {
        'full_name': 'Tunisian Republic',
        'alpha_2': 'TN',
        'alpha_3': 'TUN'
    },
    'Туркменистан': {
        'full_name': 'Turkmenistan',
        'alpha_2': 'TM',
        'alpha_3': 'TKM'
    },
    'Турция': {
        'full_name': 'Republic of Turkey',
        'alpha_2': 'TR',
        'alpha_3': 'TUR'
    },
    'Търкс и Кайкос о-ви': {
        'full_name': 'Turks and Caicos Islands',
        'alpha_2': 'TC',
        'alpha_3': 'TCA'
    },
    'Уганда': {
        'full_name': 'Republic of Uganda',
        'alpha_2': 'UG',
        'alpha_3': 'UGA'
    },
    'Узбекистан': {
        'full_name': 'Republic of Uzbekistan',
        'alpha_2': 'UZ',
        'alpha_3': 'UZB'
    },
    'Украйна': {
        'full_name': 'Ukraine',
        'alpha_2': 'UA',
        'alpha_3': 'UKR'
    },
    'Унгария': {
        'full_name': 'Hungary',
        'alpha_2': 'HU',
        'alpha_3': 'HUN'
    },
    'Уолис и Футуна': {
        'full_name': 'Wallis and Futuna',
        'alpha_2': 'WF',
        'alpha_3': 'WLF'
    },
    'Уругвай': {
        'full_name': 'Eastern Republic of Uruguay',
        'alpha_2': 'UY',
        'alpha_3': 'URY'
    },
    'Ферьорски о-ви': {
        'full_name': 'Faroe Islands',
        'alpha_2': 'FO',
        'alpha_3': 'FRO'
    },
    'Фиджи': {
        'full_name': 'Republic of Fiji',
        'alpha_2': 'FJ',
        'alpha_3': 'FJI'
    },
    'Филипини': {
        'full_name': 'Republic of the Philippines',
        'alpha_2': 'PH',
        'alpha_3': 'PHL'
    },
    'Финландия': {
        'full_name': 'Republic of Finland',
        'alpha_2': 'FI',
        'alpha_3': 'FIN'
    },
    'Фолкландски (Малвински) о-ви': {
        'full_name': 'Falkland Islands (Malvinas)',
        'alpha_2': 'FK',
        'alpha_3': 'FLK'
    },
    'Франция': {
        'full_name': 'French Republic',
        'alpha_2': 'FR',
        'alpha_3': 'FRA'
    },
    'Френска Полинезия': {
        'full_name': 'French Polynesia',
        'alpha_2': 'PF',
        'alpha_3': 'PYF'
    },
    'Френски южни територии': {
        'full_name': 'French Southern Territories',
        'alpha_2': 'TF',
        'alpha_3': 'ATF'
    },
    'Хаити': {
        'full_name': 'Republic of Haiti',
        'alpha_2': 'HT',
        'alpha_3': 'HTI'
    },
    'Хондурас': {
        'full_name': 'Republic of Honduras',
        'alpha_2': 'HN',
        'alpha_3': 'HND'
    },
    'Хонконг': {
        'full_name': 'Hong Kong Special Administrative Region of China',
        'alpha_2': 'HK',
        'alpha_3': 'HKG'
    },
    'Хърватско (893)': {
        'full_name': 'Republic of Croatia',
        'alpha_2': 'HR',
        'alpha_3': 'HRV'
    },
    'Хърд и Макдоналд, о-ви': {
        'full_name': 'Heard Island and McDonald Islands',
        'alpha_2': 'HM',
        'alpha_3': 'HMD'
    },
    'Централна африканска република': {
        'full_name': 'Central African Republic',
        'alpha_2': 'CF',
        'alpha_3': 'CAF'
    },
    'Чад': {
        'full_name': 'Republic of Chad',
        'alpha_2': 'TD',
        'alpha_3': 'TCD'
    },
    'Черна гора': {
        'full_name': 'Montenegro',
        'alpha_2': 'ME',
        'alpha_3': 'MNE'
    },
    'Чехска република': {
        'full_name': 'Czech Republic',
        'alpha_2': 'CZ',
        'alpha_3': 'CZE'
    },
    'Чили': {
        'full_name': 'Republic of Chile',
        'alpha_2': 'CL',
        'alpha_3': 'CHL'
    },
    'Швейцария': {
        'full_name': 'Swiss Confederation',
        'alpha_2': 'CH',
        'alpha_3': 'CHE'
    },
    'Швеция': {
        'full_name': 'Kingdom of Sweden',
        'alpha_2': 'SE',
        'alpha_3': 'SWE'
    },
    'Шри Ланка': {
        'full_name': 'Democratic Socialist Republic of Sri Lanka',
        'alpha_2': 'LK',
        'alpha_3': 'LKA'
    },
    'Южна Джорджия и Южни С-еви о-ви': {
        'full_name': 'South Georgia and the South Sandwich Islands',
        'alpha_2': 'GS',
        'alpha_3': 'SGS'
    },
    'Ямайка': {
        'full_name': 'Jamaica',
        'alpha_2': 'JM',
        'alpha_3': 'JAM'
    },
    'Ян Майен': {
        'full_name': 'Jan Mayen',
        'alpha_2': 'SJ',
        'alpha_3': 'SJM'
    },
    'Япония': {
        'full_name': 'Japan',
        'alpha_2': 'JP',
        'alpha_3': 'JPN'
    }
}



