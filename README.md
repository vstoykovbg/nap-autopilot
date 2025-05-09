> [!NOTE]  
> НАП направиха промени в системата. След кратко дебъгване и корекции на скрипта успях да го подкарам с Chrome и сега (февруари 2025 година) би трябвало да работи ([на моя компютър работи](https://www.google.com/search?q=it+works+on+my+computer)).  Към 18 март 2025 година го тествах и установих, че НАП са оправили проблема с Firefox, скриптът работи и с Firefox. Вероятно през 2026 година ще се наложи пак да коригирам скрипта за да работи попълването на декларацията за 2025 година.

# nap-autopilot: Въвеждане на данни в годишната данъчна декларация автоматично

Скриптът взима данните в CSV формат от директорията `import` (намираща се в директорията, където се намира скрипта) и въвежда данните от тях автоматично в уеб формуляра (годишната данъчна декларация) от портала на НАП.

В идеалния случай потребителят ще инсталира каквото е необходимо, ще запише данните в директорията `import`, ще пусне скрипта и ще се логне в портала на НАП (с ПИК или електронен подпис). Допълнителна намеса от страна на потребителя се изисква само ако има грешки.

## Защо да ползвам този скрипт вместо направо да въвеждам данните си в данъчната декларация?

Намаляват се грешките като се интегрира с други скриптове за автоматична обработка на данните. Има гличове при въвеждане на данните с copy/paste, ръчното въвеждане крие рискове от грешки (например може да копирате по невнимание данните от съседен ред).

Скриптът е полезен ако имате множество дивиденти и сте ги обработили автоматично (инвестиционният посредник ви дава данните във формат, който лесно се копира в електронна таблица за последваща обработка).

Полезен е също така ако имате множество притежавани акции и дялове, данните за които ги имате обработени в електронна таблица. Особено в случая когато искате да подадете данъчната декларация преди НАП да са активирали бутона за пренасяне на данните за притежавани акции и дялове от предишната данъчна декларация.

Дори и да не сте обработили данните автоматично пак е полезно и удобно първо да ги въведете във ваша електронна таблица вместо направо да ги въвеждате в портала на НАП. Понякога бутонът за потвърждаване не работи или сесията изтича и може да изгубите въведените данни. След като имате данните за притежавани акции във ваша електронна таблица може да ги ползвате следващата година (само триете редовете с продадени акции или ги коригирате ако сте правили частична продажба на данъчните лотове).

## Възможности

### Валидира данните преди да започне въвеждането

Скриптът проверява за често срещани грешки, но не може напълно да ви гарантира, че нямате грешки. Отделните функции за попълване на съответните таблици правят втора проверка и малки корекции на данните (ако потребителят е решил да продължи въпреки предупрежденията за невалидни данни).

### Може да попълва следните части:

* Приложение 5 Таблица 2 (доходите от продажба на финансови активи).

* Приложение 8 част I - таблицата с притежаваните акции.

* Приложение 8 част I - таблицата с притежаваните дялове.

* Приложение 8 част III - доходите от дивиденти (доходи с код 8141).

В приложение 8 част III скриптът избира код за прилагане на метод за двойното данъчно облагане 1 или 3 и попълва всички колони в таблицата само на база данните за колони 6 и 9 (които прочита от .csv файла). Ако е имало удържан данък в чужбина въвежда код 1 и прилага обикновен данъчен кредит, ако е нямало удържан данък в чужбина въвежда код 3. Винаги въвежда код 8141 в колона 4 и 0.00 в колона 7.

Ако е имало смислени данни на някой ред (сложни критерии какво е "смислени данни") не го презаписва, а продължава на следващия. В някои редки случаи презаписва редове, където прецени, че данните нямат смисъл.

### Работи с леко грешни данни

Ако все пак потвърдите въвеждането да стане с невалидните данни прави опити да оправи грешките като например закръглява числата, които са с повече цифри след десетичната точка, отколкото трябва. За да не възникват грешки избягвайте да потвърждавате въвеждане на невалидни данни.

### Добавя данни в таблици, в които има вече добавени данни.

Имайте предвид обаче какво може да се обърка, по-надолу обяснявам подробно.

### Може да изберете в една сесия да попълни само една таблица или част от нея

Достатъчно е просто да сложите само един .csv файл с данни в директорията `import`. По-късно може да преместите този файл другаде и да сложите друг файл, с който да бъде допълнена същата или друга таблица.

### Проверява дали въведените данни са тези, които е трябвало да бъдат въведени

На [това демонстрационно видео](https://www.youtube.com/watch?v=joMjdnGNkFg) се вижда как заради JavaScript-а за валидиране на въведените числови данни системата гличва и се налага повтаряне въвеждането на данни. В модерните браузъри има начин [без JavaScript да се ограничи](https://stackoverflow.com/questions/34057595/allow-2-decimal-places-in-input-type-number) въвеждането на данни само до цифрови данни с определен брой цифри след десетичната точка.

При гличване обикновено грешката е, че числата след десетичната точка ги няма.

Преди да се опита да въведе данни в някое поле проверява дали вече няма въведени коректни данни. Ако например стойността по подразбиране в полето е вярна (типично 0.00) - продължава с въвеждане на следващите данни.

Проверява дали данните в съответното поле са математически идентични за да реши дали да опита пак въвеждането. Например ако във файла има 0 за числови полета няма как данните в полето да съвпадат като знаков низ (има JavaScript скрипт, който обръща нулите на 0.00). Ако я нямаше тази функция щеше да зацикли на опити да въведе данни след като въведените данни не съвпадат напълно като знаков низ.

### Проверява дали датата е валидна

Скриптът проверява дали съответната дата съществува - например 29 февруари 2023 година не съществува и скриптът засича тази грешка. Но все пак внимавайте да не объркате месеца с числото, защото в някои случаи тази грешка не води до математически невалидна дата.

### Приема няколко начина на изписване на държавите

* Приема имената на държавите дори и когато се различават от тези в падащото меню на формуляра.
* Може да напишете стандартните двубуквени и трибуквени кодове вместо името на държавата.
* Ако сложите интервал преди или след името на държавата не е пречка.

Например може да въведете MH, MHL, Маршалови острови, Маршалски острови.

За Британските виржински острови примема нестандартния код BVI (освен стандартните VG и VGB), Виржински о-ви (Брит.) (както е в менюто на НАП), Вир**дж**ински острови, Вир**ж**ински острови, Британски Вир**дж**ински острови, Британски Вир**ж**ински острови.

Има и едни други Виржински острови с кодове VI и VIR (US Virgin Islands), но те не са много популярна дестинация за регистрация на корпорации, затова заех псевдонима Виржински острови за британските.

Няма да имате проблеми и ако объркате името на HK - приема Hong Kong, Honk Konk, Хонконг, Хонг Конг, Хонг Конк, Хонконк.

Не мисля, че има много смисъл да се добавят още псевдоними на държави, защото е достатъчно лесно просто да се ползват стандартните двубуквени или трибуквени кодове.

## Какво не може този скрипт

Скриптът не може да вземе извлечението ви от инвестиционния посредник, да го анализира и да въведе данните.

(Една част от автоматизирането на обработката на данните може да го направите с [моите електронни таблици за предварителна обработка на данните](https://github.com/vstoykovbg/BNB_currency_rates).)

Скриптът не може да се справи с оправянето или засичането на някои грешки в данните.

Скриптът не може да работи ако сайтът на НАП гличва твърде много. 

Скриптът не може да разпознае кога трябва да напише код 2 вместо код 1 в таблицата за дивидентите (но е много малко вероятно това да има значение).

По непотвърдени данни само с Индонезия и Япония има СИДДО за "освобождаване с прогресия" за дивидентите (така беше по данни на НАП от 2017 година). Дори и да отделите време да потвърдите, че за дивидентите от съответната държава са пише код 2, и се научите как се попълва таблицата с дивидентите, в този случай няма да има разлика в дължимия данък (той ще бъде нула, независимо дали напишете код 2 или код 3). Не съм сигурен само дали при необичайния и невероятен казус, когато в чужбина е удържан данък под 5% и се прилага "Освобождаване с прогресия", трябва да не се плаща изобщо български данък или да се доплати до 5%, но и в двата случая ако се приеме попълване с код 1 няма да има основание за глоба (при попълване все едно има "Обикновен данъчен кредит"). Но за да се провери това трябва да се четат договорите (СИДДО) между държавите и да се анализират.

Като избера от менюто метод с код 2 излиза съобщение:

> Не може да попълвате колони 9,10,11 и 12 на ред 1.1 на Част ІV, когато се прилага метод Освобождаване с прогресия (код за прилагане на метод 2)

Прекалено много работа е да търся информация за да потвърдя, че за доходите от дивиденти от Индонезия и Япония се избира в колона 5 метод 2. Затова оставям скрипта така, а който иска да търси допълнително информация и да коригира редовете, където смята, че скриптът е сгрешил с попълването.

Тъй като няма укрит данък грешното попълване (код 1 весто код 3) не е проблем (не е основание за глоба).

Разбира се горното не е данъчен съвет, а просто мое мнение. Гаранция за правилно тълкуване не мога да дам, скриптът също е без каквито и да е гаранции (вж. лиценза).

## Инсталиране

* Инсталирайте Python 3
  * Потребителите на Windows изтеглят инсталационния файл от [тук](https://www.python.org/downloads/windows/).
  * Потребителите на Linux ползват специфичния начин за тяхната дистрибуция - например `sudo apt install python3`.
* Изтеглете архив на това хранилище (например от Code -> Download zip или [директно от този линк](https://github.com/vstoykovbg/nap-autopilot/archive/refs/heads/main.zip)) и го  разархивирайте.
* Инсталирайте изискваните модули от requirements.txt:
  * Потребителите на Windows може да цъкнат на install_requirements.bat (което изпълнява командата `python.exe -m pip install -r requirements.txt`).
  * Потребителите на Linux пишат в конзолата `pip3 install -r requirements.txt` (след като влязат в директорията `nap-autopilot`, където са разархивираните файлове).

## Ползване

Запишете файловете във формат CSV, които съдържат данните за данъчната декларация в директорията `import`. Първоначално там има празни файлове само със заглавна част. Може да ги отворите с програма за електронни таблици и да добавите данните.

> [!NOTE]  
> Премахнете празните файлове от директорията `import` преди да пуснете скрипта (оставете само тези файлове, които сте редактирали или добавили).

Числата трябва да са с десетична точка, а не с десетична запетая.

За потребителите на Windows направих .bat файла `run_in_autopilot_mode.bat` като после забелязах, че скриптът тръгва в конзолата дори и когато директно се кликне `autopilot.py`.

Потребителите на Linux трябва да влязат в конзолата, да сменят текущата директория да стане `nap-autopilot` и да напишат `python3 autopilot.py` (а може и `./autopilot.py` и евентуално `chmod +x autopilot.py` предварително ако вече не е направено).

Тествах на Ubuntu 22 с Nautilus да кликна върху `autopilot.py`, отваря се в текстов редактор. Иначе с десен бутон мога да избера от менюто "Run as a Program" и тръгва в конзолата. Но аз предпочитам да пускам скрипта като първо пусна конзолата, вляза в директорията и стартирам скрипта.

Пускането на скрипта за работа с браузъра Chrome става от `autopilot_chrome.py` (или `autopilot_slow_chrome.py` в бавен режим - ползвайте този ако има проблем с бързия). Иначе с `autopilot.py` (или `autopilot_slow.py` за бавен режим) се ползва браузъра Firefox.

### Заглавната част на файловете във формат CSV и техните имена

Скриптът разпознава сам кой файл с данните за коя таблица е (по заглавната му част), но тъй като файловете с данни за дялове и за акции имат еднаква заглавна част трябва да сложите в името на файла с данни за притежаваните дялове "shares". Тоест може да сложите в името на файла за притежаваните акции примерно "stocks", а в името на файла с данни за притежаваните дялове трябва да има "shares" (например "shares1.csv", "my-shares.csv").

Името на файла с продажбите на криптовалути (които се декларират с код 5082) трябва да съдържа crypto (напр. `sales_crypto.csv`). Името на файла, който съдържа продажби с код 508 не трябва да съдържа crypto.

> [!NOTE]  
> Възможно е да ползвате [моите електронни таблици от тук](https://github.com/vstoykovbg/BNB_currency_rates) за да генерирате CSV файловете за притежаваните акции/дялове, доходите от дивиденти и доходите с код 508 и 5082. Но е възможно и ръчно да напишете тези CSV файлове или да си напишете свои скриптове за това.

Заглавията на колоните са взети директно от уникалните части в имената на полетата, които се въвеждат.

За числовите данни във файловете важат същите общи правила както обясних [в тази статия (директна връка към раздела)](https://redtapepayments.blogspot.com/2020/10/blog-post_4.html#%D0%BE%D0%B1%D1%89%D0%B8-%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D0%B0-%D0%B7%D0%B0%D0%BA%D1%80%D1%8A%D0%B3%D0%BB%D1%8F%D0%B2%D0%B0%D0%BD%D0%B5). Накратко: пишат се сумите в лева освен само на едно място, където е изрично написано в инструкциите за попълване на данъчната деларация, че се пише сумата в оригиналната валута.

Числовите данни ползват разделител десетична точка, а не десетична запетая. Числовите данни имат ограничение да имат до два знака след десетичната точка с изключение на `count`, където ограничението е до 8 знака след десетичната точка (това е полето за брой акции/дялове - за да може да се поддържат fractional shares).

В директорията `import` има шаблони (само със заглавната част, без данни). Отворете ги с програма за електронни таблици, копирайте колоните там и запазете. При отваряне внимавайте какви настройки избирате, защото записът ще стане с тези настройки. Колоните с имена (на държави и на платци на доходи) трябва да са с кодиране UTF-8. Тествал съм как работи скрипта ако не се ползват кавички (тоест за разделител на полетата се ползва само запетая). Не съм правил подробни тестове какво може да се обърка ако не избера правилния формат на файла. Ако изписвате наименованията (на държави и платци на доходи) на латиница ще избегнете проблеми с избора на правилното кодиране.

Ако ползвате LibreOffice (напр. [таблците от тук](https://github.com/vstoykovbg/BNB_currency_rates)), селектирайте sheet-а с данните за импортиране, от менюто "File" изберете "Save a copy" и след като потвърдите записване на .csv файл ще ви излезе такъв диалог:

![снимка на екрана](screenshots/libreoffice-export-csv-utf-8.png)

Уверете се, че кодирането е UTF-8.

При ползване на функцията "Save a copy" ще бъде записан само текущо избрания sheet в нов файл, като продължавате редакцията на съществуващия .ods файл.

#### Файловете за притежаваните акции и дялове (приложение 8 част I)

```
country,count,date,price_in_currency,price
```

* country: Колона 2. Държавата, където е регистрирана компанията или където е регистрирано дружеството (фонда). Обясних подробно [тук](https://redtapepayments.blogspot.com/2020/02/31.html) и [тук](https://redtapepayments.blogspot.com/2020/10/blog-post_4.html#%D0%BF%D1%80%D0%B8%D1%82%D0%B5%D0%B6%D0%B0%D0%BD%D0%B8%D0%B5).
* count: Колона 3. Брой дялове/акции. Ограничението е до 8 знака след десетичната точка.
* date: Колона 4. Датата на придобиване на акциите/дяловете. Форматът е DD.MM.YYYY (Две цифри за деня, две цифри за месеца, четири цифри за годината - отделени с точка).
* price_in_currency: Колона 5. Цената на придобиване в "съответната валута". Това е от малкото изключения когато сумата може да не е в лева, а в друга валута (ако е ползвана друга валута за придобиването). Ако придобиването е на бартер се пише цената в лева на това, което е дадено в замяна.
* price: Колона 6. Левовата равностойност на сумата от колона 5 (тоест цената на придобиване, преизчислена в лева).

Форматът на датата е този, който е на видимото поле от формуляра. Иначе вътрешно системата ползва датата в друг формат, скриптът се грижи за конвертирането на датата в съответния формат.

#### Файловете за доходите от дивиденти (приложение 8 част III):

```
name,country,sum,paidtax
```

Всички числови полета от този файл са суми в левове и трябва да имат не повече от два знака след десетичната точка.

* name: Колона 2. Наименованието на лицето, което е изплатило дохода. Подробно кое е това лице писах [тук](https://redtapepayments.blogspot.com/2021/02/blog-post.html) и [тук](https://redtapepayments.blogspot.com/2020/10/blog-post_4.html). Накратко: емитента на акциите (ако е дивидент от акции) или управляващото дружество на фонда, който изплаща дивидентите (ако е фонд).
* country: Колона 3. Пише се съответната държава Подробно писах коя е съответната държава в цитираните статии по-горе. Накратко: държавата, в която е установен за данъчни цели платеца на дохода.
* sum: Колона 6. Брутния размер на дивидента, определен с решението за дивидент.
* paidtax: Колона 9. Удържаният данък върху дивидента в чужбина за този дивидент.

#### Файловете за доходите от продажба на финансови активи (Таблица 2 от приложение 5):

```
sellvalue,buyvalue,profit,loss
```

Всички числови полета от този файл са суми в левове и трябва да имат не повече от два знака след десетичната точка.

* sellvalue: Колона 3. Сумата от всички продажби.
* buyvalue: Колона 4. Сумата от цените на придобиване на продадените активи.
* profit: Колона 5. Сумата от всички печалби от продажби на финансови активи през годината.
* loss: Колона 6. Сумата от всички загуби от продажби на финансови активи през годината.

Подробно как се изчисляват обясних [в тази статия (директен линк към съответната част от статията, където има илюстрация)](https://redtapepayments.blogspot.com/2020/10/blog-post_4.html#%D0%BF%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5-5-%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D1%80).

Може да въведете само първите две колони, тогава скриптът си измисля третата и четвъртата (ако сте на загуба я попълва в колоната със загубите, ако сте на печалба я попълва в колоната с печалбите).

Но технически е правилно да попълните и четирите колони както обясних.

Скриптът има валидация, така че ще изведе съобщение за грешка ако въведете данни, които нямат математическа съгласуваност.

## Бъгове, проблеми и превантивни мерки

Ширината на прозореца на браузъра (вътрешната - т.е. без да броим скролерите) трябва да е поне 960 пиксела за да работи началната фаза на скрипта (когато избира ЕГН от меню). По принцп трябва да работи и при по-малък прозорец, защото има инструкции да превърта, но го пускайте на малък прозорец само за тестове. Когато скриптът достигне до момента когато изисква от потребителя да се логне може преди логването да промените размера на прозореца за да го разположите така, че хем да виждате прозореца, хем да виждате поне последните 10-тина реда от конзолата.

Излязоха и нови бъгове като минах на нова версия на Firefox - когато определен елемент е покрит със скролер това обърква автоматичното взаимодействие. Сложих инструкции преди да вкарва данни да превърти така, че елементът да е колкото се може по-всредата. Не съм сложил инструкции да се пуска браузъра с други настройки (с външни скролери), защото това може да направи скрипта неработещ при евентуално обновяване на браузърите (и смяна на API-то).

След като се стартира скрипта не взаимодействайте с браузъра (не пипайте клавиатурата и мишката, не отваряйте нови табове). Освен в случаите когато скриптът изведе съобщение, с което ви подканва да извършите някакво действие. Възможни действия, които скриптът може да ви подкане да извършите:

* Да се логнете (да въведете ПИК код и да натиснете бутона за вход или да натиснете бутона за вход и да потвърдите влизане с електронен подпис).

* Да натиснете Enter или да напишете нещо и да натиснете Enter (това с писането е с цел да не натиснете Enter по невнимание без да сте прочели текста в конзолата)

Дори и да отидете в друго работно пространство (workspace) [поради бъг](https://bugs.launchpad.net/ubuntu/+source/firefox/+bug/2056642) е възможно dropdown менютата да се отварят в този друг workspace и това да повлияе на работата на скрипта.

Не бъркайте кога трябва да извършите действие в конзолата (да напишете нещо и да натиснете Enter или само да натиснете Enter) и кога трябва да извършите действие в браузъра (да се логнете след като скриптът в подкани). Не правете нищо друго освен това, което скриптът ви подканва, защото ако примерно затворите някой диалог това ще го обърка (скриптът очаква диалогът да не се затвори сам).

Макар че скриптът може да се ползва за добавяне на допълнителни редове към вече попълнени таблици е по-добре да не ползвате тази функция ако искате да работи гладко (на автопилот без допълнителна интервенция от страна на потребителя освен логването). Ако все пак решите да я ползвате имайте предвид следното:

Не е желателно да запазвате редове като например пишете само държава в таблицата с дивидентите. Въпреки че няма въведен данък скриптът ще уважи желанието ви да запазите реда и ще продължи на следващия. Ако обаче другите колони от този ред са невалидни накрая ще се получи грешка при потвърждаването на частта и скриптът ще иска потвърждение дали да продължи. Затова избягвайте да въвеждате невалидни редове, ако въвеждате някакви данни предварително нека са валидни. Най-добре е обаче да не въвеждате никакви данни ръчно в съответните таблици предварително, така лесно ще можете да изтриете всичко и да продължите отначало (ако нещо се обърка).

Ако все пак ползвате скрипта с предварително ръчно попълнени редове направете снимки на екрана и обърнете внимание до кой ред е стигнало въвеждането (за да може после ако нещо се обърка да се ориентирате да изтриете само новите редове). Скриптът не би трябвало да променя вече въведени редове ако те са с очевидно смислени данни.

Различните отчети на инвестиционните посредници имат различен начин за изписване на датите, внимавайте когато конвертирате датите от един формат в друг. Въпреки, че скриптът валидира датите, тази валидация е чисто математическа, няма как да знае, че сте объркали 10 февурари с 2 октомври.

За автоматично конвертиране на датите и попълване на курса на БНБ в таблицата, в която правите обработката на данните, може да ползвате моите скриптове [от тук](https://github.com/vstoykovbg/BNB_currency_rates).

Да не вземе някой да се обърка да извади `autopilot.py` за да го ползва самостоятелно, този файл е няколко реда (ползва подпрограми от други файлове от текущата директория).

Когато скриптът се оплаква, че не може да натисне бутона за запазване на данните да не се объркате да натиснете някой друг бутон, натиска се бутона, с който се потвърждава приложението, не бутона за потвърждаване на цялата данъчна декларация. Бутони в браузъра натискайте само когато скриптът прекъсне работа и ви подкани да го направите (това става само в случай на грешка).

Ако имате достъп с акаунта си до данъчната декларация на повече от едно ЕГН скриптът няма как да знае кое е правилното ЕГН (затова оставя на потребителя да избере правилното).

Не съм тествал какво става когато се появи прозорецът за "предварително попълнени данни", може да се наложи ръчно да затворите този прозорец за да не влияе на работата на скрипта.

В предишните версии се обновяваше само скритото поле за дата, в новата версия се обновява и видимото поле.

Бях забравил да направя проверка дали датата е въведена коректно, тя се въвежда с друга функция по технически причини (не е с общата функция fill_input). В новата версия това е коригирано.

Новата версия работи по-бързо, обаче по време на тестовете понякога браузърът забива. Не знам дали е от скоростта или по друга причина. Ако имате проблем пуснете бавната версия с `autopilot_slow.py` или `run_in_autopilot_mode_slow.bat`.

Към 5 февруари 2025 г. попълването на годишната данъчна декларация с Firefox не работеше. Но може да се ползва Google Chrome. За да стартирате nap-autopilot в режим Google Chrome ползвате стартиращия файл с Chrome в наименованието (`autopilot_chrome.py` или `autopilot_slow_chrome.py`).

Към 18 март 2025 г. попълването на годишната данъчна декларация с Firefox отново работи.

Добавих проверка за съобщението за липса на данни от работодатели и платци на доходи, скриптът автоматично затваря това съобщение и продължава работа (това съобщение се появи през месец март 2025 година, преди не бях се натъквал на него, защото имах доходи, съобщени от платци на доходи).

![снимка на екрана на съобщението](https://i.imgur.com/euJhJlH.png)

Ако случайно имате някакво съобщение, което не е предвидено да бъде затворено от скрипта, ще имате шанс да го затворите. Наблюдавайте конзолата за такъв текст:

> Too many attempts. Прекалено много опити.
> 
> Натиснете Enter за да продължим с опитите.
> 
> If the portal is not working wait and go to the yearly declaration.
> 
> Ако порталът не работи изчакайте и след като заработи (преди да натиснете Enter) отидете в годишната данъчна декларация.
>
> Press Enter to continue. Натиснете Enter за да продължим.

След като затворите неочакваните съобщения (диалогови прозорци), които пречат на скрипта да продължи, натиснете Enter в конзолата. После върнете фокуса върху браузъра и не пипайте нищо, докато скрипта работи (пипането на мишката и клавиатурата, премахването на фокуса от прозореца на браузъра, в който се попълва декларацията, може да наруши работата на скрипта).

По-късно през месец март 2025 година (на 20 март) започна да се появява **диалогов прозорец за налични данни, подадени от платци на доходи** (а дни преди това излизаше съобщение, че няма такива данни):

![снимка на екрана на съобщението](https://i.imgur.com/K8YPwNk.png)

За този диалог реших да не добавям функционалност за автоматичното му затваряне.

Ако не жалаете да се занимавате с диалога за въвеждане на данни, подадени от платци на доходи, затворете диалога с натискане на бутона "Отказ" или бутона " x " в горния десен ъгъл на диалоговия прозорец.

При желаните за взаимодействие с диалога за въвеждане на данни, подадени от платци на доходи, изчакайте в конзолата да излезе `Press Enter to continue. Натиснете Enter за да продължим`.

След като приключите с процеса по въвеждане на данни, подадени от платци на доходи, може да натистнете Enter в конзолата за да сигнализирате на nap-autopilot да продължи работата си.


## Тестови данни

В директорията `examples-mock-data` сложих примерни данни за тестване.

Ако искате само да проверите как валидаторът ги обработва може да ги преместите в директорията import и да напишете командата:

`python3 ./validator_test.py`

За файла `sales-mathematically-contradictory.csv` валидаторът извежда съобщение "Inconsistent values: (sellvalue - buyvalue) is not equal to (profit - loss) ...". Тоест няма математически смисъл разликата между сумите от продажните цени и сумите от цените на придобиване да е различна от разликата между сумата на печалбите и сумата на загубите.

Файлът `sales-not-correct-but-accepted.csv` няма данни за печалбите и загубите, ако потвърдите скрипта да продължи с невалидни данни после функцията за попълване на таблица 5 смята печалбата или загубата и я попълва в съответната колона (което няма да е коректно в някои случаи - ако не всички резултати са само печалби или само загуби).

## Платени услуги по обработка на данните за данъчната декларация (не е реклама, не е препоръка да се ползват)

Има и други начини (платени услуги) за автоматизиране на обработката на данните за данъчната декларация, но не съм ги ползвал и проверявал обстойно как работят: [NRA Assist](https://nra-assist.com/), [Tax Wizard](https://tax-wizard.eu/en), [Taxable.bg](https://www.taxable.bg/). За Tax Wizard [имах забележки](https://redtapepayments.blogspot.com/2021/03/blog-post_10.html) последния път като проверявах как смята данъците, дали са го оправили не знам. (NRA Assist мисля, че имаше възможност да генерира csv файлове за nap-autopilot, но не намирам информация на сайта им за това в момента.)

**Давам този списък само за информация, не е препоръка да се ползват, защото не съм запознат детайлно с това как правят изчисленията.**

## Без общинско, държавно или европейско финансиране

Проектът е напълно частен - осъществен е без каквото и да е публично финансиране (общинско, европейско, държавно). И въпреки, че от страна на държавата има само пречки - не само, че не публикуваха спецификациите на XML формата за импорт на данни, но изобщо премахнаха тази функция (преди я имаше заради това, че беше възможно да се попълва данъчната декларация в PDF формуляр).
