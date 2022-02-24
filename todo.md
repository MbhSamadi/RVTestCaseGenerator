<!-- - dependency random -->
<!-- - no loops (may not reach the maximum call) -->
<!-- - bug:
    reactiveclass rebeca0(0) {
        knownrebecs {
            rebeca1 kr1;
            rebeca2 kr2;
        }
        msgsrv r0m0() {
            kr0.r0m0() // self
        }
    } -->

<!-- - msgserver & constructor body (if condition & assignment) & statevars -->
<!-- - buffer size based on number of calls -->

<!-- - call some msgservers in body constructor -->

<!-- Session -->

<!-- - if conditions should be boolean -->
<!-- - msgserver call should always reach the maximum (check minimum maximum msgservers) -->
<!-- - run rebec codes (check if they compile) -->
<!-- - get property length and the count of the members of the set from user and print the set of properties with that length -->

<!-- - testcase -->
<!-- - bug: In generating msgservers graph, we're checking all pairs of msgservers but as we add some of them at first, then later pairs can't be added. so we may not reach the max msgserver call sequence! -->

<!-- - بدنه‌ها حداقل یک statement داشته باشند -->
<!-- - the count of the members of the set from user: یعنی طول مجموعه‌ی property -->
<!-- - در کانستراکتور همه‌ی statevar ها رو مقدار اولیه بده -->
<!-- - توی property فرمت خروجی به این شکل باشه: ('r2m1', 'r0m0') -> (rebeca2 . r0m0 . rebeca0) -->
<!-- - در property set باید مسیرهایی که طول بیشتر از مقدار وارد شده دارند رو هم انتخاب کنم، بعد از یال‌هاش به تعداد وارد شده، به صورت رندم انتخاب کنم. الویت اینه که اونایی که پشت سر هم کال نمیشن انتخاب بشه -->
<!-- - یک dfa میخوایم از property set:
در هر property هر عضوش رو به عنوان یال‌های یک dfa در نظر بگیر. و یک property یک مسیر از نود شروع به نود پایان در dfa باشه. dfa رو به صورت یک مجموعه‌ای از (node,edge,node) خروجی بده. که اینجا edge همون عضو‌های property هست. -->
<!-- - تعداد ربکاهایی که در یک property شرکت می‌کنند هم باید از کاربر گرفته بشه ---- Not Needed ---- -->
<!-- - for dfa: https://pypi.org/project/automata-lib/ -->

<!-- - باید یال بکوارد هم داشته باشه: از کل مسج‌ها به صورت رندم یکی انتخاب بشه و توی یه sequence از یه نود به یه نود قبلی یال داشته باشه. تعداد بکواردها رو هم ورودی بگیر -->
<!-- - یه سوال دیگه اینکه قرار شد تو dfa ای که دارم، state ای که trap باشه نداشته باشم؟ یعنی تو هر state به ازای input هایی که به جایی نمیره، توی همون state بمونه. درسته؟ -->
<!-- - جدول باید به ازای هر transition و هر pre-transition یه ردیف داشته باشه.
  transition: یه یال رو انتخاب میکنیم
  pre-transition: یال‌های قبل از یال transition
  vio-transition: یال pre رو در نظر میگیریم بعد دنبال یال‌های بکواردی میگردیم که اون یال pre بین نود ابتدا و انتهای این یال بکوارد قرار بگیره. به این یال‌های بکوارد میگیم vio

  مثلا a -> b -> c -> d و d -> b
  اینجا d -> b یک یال بکوارد هست
  فرض کن c -> d یال transition مون باشه

  - فرض کن b -> c یال pre مون باشه
    در این صورت d -> b یک یال vio هست

  - فرض کن a -> b یال pre مون باشه
    در این صورت یال vio نداره -->

<!-- - بپرسه چندتاش رابطه‌ی علی داشته باشه چندتاش نداشته باشه -->
<!-- - تعداد بکواردها رو هم ورودی بگیر -->
<!-- - self-loop رو حذف کن. و جدول ها رو از روی dfa که minify شده بساز -->
<!-- - اسم state ها رو عوض کن که q0,q1,... باشن -->
<!-- - واسه هر ربکا یه جدول باید بدم. -->
<!-- - یال pre: یال‌هایی که دقیقا یکی قبل از transition هستن. (یعنی ربطی به sequence نداره. کل یال‌های قبلیش) -->
<!-- - تو جدول باید کل tranition نوشته بشه. یعنی (qsender, msg, qreceiver) -->

<!-- یه نکته دیگه اینکه از یال فاینال هیج ترنزیشنی چه بکوارد و چه فوروارد نباید خارج بشه -->

<!-- read from a json file -->
<!-- property set has some duplicastes -->
<!-- rename rebec names in table -->

property max length
