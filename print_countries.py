#!/usr/bin/python3

import re

html = '<option value="България">България</option><option value="Австралия">Австралия</option><option value="Австрия">Австрия</option><option value="Азербайджан">Азербайджан</option><option value="Албания">Албания</option><option value="Алжир">Алжир</option><option value="Ангола">Ангола</option><option value="Ангуила">Ангуила</option><option value="Андора">Андора</option><option value="Антарктида">Антарктида</option><option value="Антигуа и Барбуда">Антигуа и Барбуда</option><option value="Аржентина">Аржентина</option><option value="Армения">Армения</option><option value="Аруба">Аруба</option><option value="Афганистан">Афганистан</option><option value="Бангладеш">Бангладеш</option><option value="Барбадос">Барбадос</option><option value="Бахамски о-ви">Бахамски о-ви</option><option value="Бахрейн">Бахрейн</option><option value="Беларус">Беларус</option><option value="Белгия">Белгия</option><option value="Белиз">Белиз</option><option value="Бенин">Бенин</option><option value="Бермудски о-ви">Бермудски о-ви</option><option value="Боливия">Боливия</option><option value="Босна и Херцеговина">Босна и Херцеговина</option><option value="Ботсуана">Ботсуана</option><option value="Бразилия">Бразилия</option><option value="Брит. територия в Индийския океан">Брит. територия в Индийския океан</option><option value="Бруней">Бруней</option><option value="Буве">Буве</option><option value="Буркина фасо">Буркина фасо</option><option value="Бурунди">Бурунди</option><option value="Бутан">Бутан</option><option value="Вануату">Вануату</option><option value="Ватикана">Ватикана</option><option value="Великобритания">Великобритания</option><option value="Венецуела">Венецуела</option><option value="Виетнам">Виетнам</option><option value="Виржински о-ви (Брит.)">Виржински о-ви (Брит.)</option><option value="Виржински о-ви (САЩ)">Виржински о-ви (САЩ)</option><option value="Габон">Габон</option><option value="Гамбия">Гамбия</option><option value="Гана">Гана</option><option value="Гаяна">Гаяна</option><option value="Гваделупа">Гваделупа</option><option value="Гватемала">Гватемала</option><option value="Гвинея">Гвинея</option><option value="Гвинея-Бисау">Гвинея-Бисау</option><option value="Германия">Германия</option><option value="Гиана(Фр.)">Гиана(Фр.)</option><option value="Гибралтар">Гибралтар</option><option value="Гренада">Гренада</option><option value="Гренландия">Гренландия</option><option value="Грузия">Грузия</option><option value="Гуам">Гуам</option><option value="Гърция">Гърция</option><option value="Дания">Дания</option><option value="Джибути">Джибути</option><option value="Доминика">Доминика</option><option value="Доминиканска република">Доминиканска република</option><option value="Египет">Египет</option><option value="Ейре (Ирландия)">Ейре (Ирландия)</option><option value="Еквадор">Еквадор</option><option value="Екваториална Гвинея">Екваториална Гвинея</option><option value="Еритрея">Еритрея</option><option value="Естония">Естония</option><option value="Етиопия">Етиопия</option><option value="Заир">Заир</option><option value="Замбия">Замбия</option><option value="Западна Сахара">Западна Сахара</option><option value="Зимбабве">Зимбабве</option><option value="Израел">Израел</option><option value="Източен Тимор">Източен Тимор</option><option value="Източни Самоа (САЩ)">Източни Самоа (САЩ)</option><option value="Индия">Индия</option><option value="Индонезия">Индонезия</option><option value="Ирак">Ирак</option><option value="Иран">Иран</option><option value="Ирландия">Ирландия</option><option value="Исландия">Исландия</option><option value="Испания">Испания</option><option value="Италия">Италия</option><option value="Йемен">Йемен</option><option value="Йордания">Йордания</option><option value="Кабо Верде">Кабо Верде</option><option value="Казахстан">Казахстан</option><option value="Кайманови о-ви">Кайманови о-ви</option><option value="Камбоджа">Камбоджа</option><option value="Камерун">Камерун</option><option value="Канада">Канада</option><option value="Катар">Катар</option><option value="Кения">Кения</option><option value="Кипър">Кипър</option><option value="Киргизтан">Киргизтан</option><option value="Кирибати">Кирибати</option><option value="Китай">Китай</option><option value="КНДР">КНДР</option><option value="Кокосови о-ви">Кокосови о-ви</option><option value="Колумбия">Колумбия</option><option value="Коморски о-ви">Коморски о-ви</option><option value="Конго">Конго</option><option value="Косово">Косово</option><option value="Коста Рика">Коста Рика</option><option value="Кот д`Ивоар">Кот д`Ивоар</option><option value="Куба">Куба</option><option value="Кувейт">Кувейт</option><option value="Лаос">Лаос</option><option value="Латвия ">Латвия </option><option value="Лесото">Лесото</option><option value="Либерия">Либерия</option><option value="Либия">Либия</option><option value="Ливан">Ливан</option><option value="Литва">Литва</option><option value="Лихтенщайн">Лихтенщайн</option><option value="Люксембург">Люксембург</option><option value="Мавритания">Мавритания</option><option value="Мавриций">Мавриций</option><option value="Мадагаскар">Мадагаскар</option><option value="Макао">Макао</option><option value="Малави">Малави</option><option value="Малайзия">Малайзия</option><option value="Малдиви">Малдиви</option><option value="Мали">Мали</option><option value="Малки далечни о-ви на САЩ">Малки далечни о-ви на САЩ</option><option value="Малта">Малта</option><option value="Мариански о-ви">Мариански о-ви</option><option value="Мароко">Мароко</option><option value="Мартиника">Мартиника</option><option value="Маршалски о-ви">Маршалски о-ви</option><option value="Мексико">Мексико</option><option value="Мианмар (Бирма)">Мианмар (Бирма)</option><option value="Микронезия">Микронезия</option><option value="Майот">Майот</option><option value="Мозамбик">Мозамбик</option><option value="Молдова">Молдова</option><option value="Монако">Монако</option><option value="Монголия">Монголия</option><option value="Монтсерат">Монтсерат</option><option value="Намибия">Намибия</option><option value="Науру">Науру</option><option value="Непал">Непал</option><option value="Неутрална зона">Неутрална зона</option><option value="Нигер">Нигер</option><option value="Нигерия">Нигерия</option><option value="Нидерландия (Холандия)">Нидерландия (Холандия)</option><option value="Нидерландски Антили">Нидерландски Антили</option><option value="Никарагуа">Никарагуа</option><option value="Ниуе">Ниуе</option><option value="Нова Заландия">Нова Заландия</option><option value="Нова Келедония">Нова Келедония</option><option value="Норвегия">Норвегия</option><option value="Норфолк">Норфолк</option><option value="Обединени арабски емирства">Обединени арабски емирства</option><option value="Оман">Оман</option><option value="Остров Джърси (Великобритания)">Остров Джърси (Великобритания)</option><option value="Остров Кук">Остров Кук</option><option value="Остров Кюрасао">Остров Кюрасао</option><option value="Остров Ман">Остров Ман</option><option value="о-ви Аланд">о-ви Аланд</option><option value="Пакистан">Пакистан</option><option value="Палау">Палау</option><option value="Палестина">Палестина</option><option value="Панама">Панама</option><option value="Папуа - Нова Гвинея">Папуа - Нова Гвинея</option><option value="Парагвай">Парагвай</option><option value="Перу">Перу</option><option value="Питкерн">Питкерн</option><option value="Полша">Полша</option><option value="Португалия">Португалия</option><option value="Пуерто Рико">Пуерто Рико</option><option value="Република Корея">Република Корея</option><option value="Република Македония">Република Македония</option><option value="Република Южна Африка">Република Южна Африка</option><option value="Реюнион">Реюнион</option><option value="Рождественски о-ви">Рождественски о-ви</option><option value="Руанда">Руанда</option><option value="Румъния">Румъния</option><option value="Русия">Русия</option><option value="Салвадор">Салвадор</option><option value="Самоа">Самоа</option><option value="Сан Марино">Сан Марино</option><option value="Санта Лусия">Санта Лусия</option><option value="Сао Томе и Принсипи">Сао Томе и Принсипи</option><option value="Саудитска Арабия">Саудитска Арабия</option><option value="САЩ">САЩ</option><option value="Свазиленд">Свазиленд</option><option value="Света Елена Остров">Света Елена Остров</option><option value="Сейнт Винсенти Гренадини">Сейнт Винсенти Гренадини</option><option value="Сейнт Кристофър и Нейвис">Сейнт Кристофър и Нейвис</option><option value="Сейшелски о-ви">Сейшелски о-ви</option><option value="Сен Пиер и Микелон">Сен Пиер и Микелон</option><option value="Сенегал">Сенегал</option><option value="Сиера Леоне">Сиера Леоне</option><option value="Сингапур">Сингапур</option><option value="Сирия">Сирия</option><option value="Словашка Република">Словашка Република</option><option value="Словения">Словения</option><option value="Соломонови о-ви">Соломонови о-ви</option><option value="Сомалия">Сомалия</option><option value="Суазиленд">Суазиленд</option><option value="Судан">Судан</option><option value="Суринам">Суринам</option><option value="Сърбия">Сърбия</option><option value="Таджикистан">Таджикистан</option><option value="Тайван">Тайван</option><option value="Тайланд">Тайланд</option><option value="Танзания">Танзания</option><option value="Того">Того</option><option value="Токелау">Токелау</option><option value="Тонга">Тонга</option><option value="Тринидад и Тобаго">Тринидад и Тобаго</option><option value="Тувалу">Тувалу</option><option value="Тунис">Тунис</option><option value="Туркменистан">Туркменистан</option><option value="Турция">Турция</option><option value="Търкс и Кайкос о-ви">Търкс и Кайкос о-ви</option><option value="Уганда">Уганда</option><option value="Узбекистан">Узбекистан</option><option value="Украйна">Украйна</option><option value="Унгария">Унгария</option><option value="Уолис и Футуна">Уолис и Футуна</option><option value="Уругвай">Уругвай</option><option value="Ферьорски о-ви">Ферьорски о-ви</option><option value="Фиджи">Фиджи</option><option value="Филипини">Филипини</option><option value="Финландия">Финландия</option><option value="Фолкландски (Малвински) о-ви">Фолкландски (Малвински) о-ви</option><option value="Франция">Франция</option><option value="Френска Полинезия">Френска Полинезия</option><option value="Френски южни територии">Френски южни територии</option><option value="Хаити">Хаити</option><option value="Хондурас">Хондурас</option><option value="Хонконг">Хонконг</option><option value="Хърватско (893)">Хърватско (893)</option><option value="Хърд и Макдоналд, о-ви">Хърд и Макдоналд, о-ви</option><option value="Централна африканска република">Централна африканска република</option><option value="Чад">Чад</option><option value="Черна гора">Черна гора</option><option value="Чешка република">Чешка република</option><option value="Чили">Чили</option><option value="Швейцария">Швейцария</option><option value="Швеция">Швеция</option><option value="Шри Ланка">Шри Ланка</option><option value="Южна Джорджия и Южни С-еви о-ви">Южна Джорджия и Южни С-еви о-ви</option><option value="Ямайка">Ямайка</option><option value="Ян Майен">Ян Майен</option><option value="Япония">Япония</option>'

# Use regex to find all values
values = re.findall(r'value="([^"]+)"', html)

print(values)
