# `simulation.py` — الشرح الكامل سطر بسطر (النسخة المنظّفة)

> شرح مبسّط لمحرّك المحاكاة المكوّن من 481 سطراً.
> لا يُشترط معرفة مسبقة بلغة Python. كل كلمة مفتاحية، كل معامل، كل
> دالة — مشروحة مع أمثلة عملية.
>
> هذه هي نسخة **إعادة البناء المنظّفة** — عدد دوال أقل (20 بدل 35)، بيانات
> حقيقية من البنك الدولي، أجور مُعايَرة وفق BLS، ودعم لكل دولة.

---

## جدول المحتويات

- [الجزء 0 — أساسيات Python التي تحتاجها أولاً](#الجزء-0--أساسيات-python-التي-تحتاجها-أولاً)
- [الجزء 1 — تشريح الملف](#الجزء-1--تشريح-الملف)
- [الجزء 2 — الاستيرادات وترويسة الملف (أسطر 1-16)](#الجزء-2--الاستيرادات-وترويسة-الملف-أسطر-1-16)
- [القسم A — الثوابت (أسطر 19-68)](#القسم-a--الثوابت-أسطر-19-68)
- [القسم B — البيانات الحيّة: جالبات البنك الدولي (أسطر 71-151)](#القسم-b--البيانات-الحيّة-جالبات-البنك-الدولي-أسطر-71-151)
- [القسم C — الرياضيات الأساسية (أسطر 154-192)](#القسم-c--الرياضيات-الأساسية-أسطر-154-192)
- [القسم D — التفصيل المستنتج (أسطر 195-243)](#القسم-d--التفصيل-المستنتج-أسطر-195-243)
- [القسم E — مشغّل السيناريوهات (أسطر 246-368)](#القسم-e--مشغّل-السيناريوهات-أسطر-246-368)
- [القسم F — البيانات التاريخية + التحقق (أسطر 371-429)](#القسم-f--البيانات-التاريخية--التحقق-أسطر-371-429)
- [القسم G — المخرجات (أسطر 432-481)](#القسم-g--المخرجات-أسطر-432-481)
- [الروابط بين الأقسام](#الروابط-بين-الأقسام)
- [ما الذي تغيّر عن `simulation.py` الأصلية](#ما-الذي-تغيّر-عن-simulationpy-الأصلية)
- [أنماط Python الشائعة المستخدمة في هذا الملف](#أنماط-python-الشائعة-المستخدمة-في-هذا-الملف)
- [قاموس كل الرموز](#قاموس-كل-الرموز)

---

## الجزء 0 — أساسيات Python التي تحتاجها أولاً

قبل أن تقرأ أي سطر من الكود، عليك أن تتعرف على هذه المكوّنات الأساسية. أمضِ 5 دقائق هنا وسيصبح باقي الملف مقروءاً.

### 0.1 المتغيّرات — تسميات على صناديق

```python
x = 5
name = "Tech"
```
**اقرأها:** "خذ القيمة على اليمين وضعها في صندوق يحمل الاسم الموجود على اليسار."

علامة `=` تعني **التعيين**، وليس المساواة (المساواة هي `==`).

### 0.2 الأرقام

```python
3_400_000_000   # عدد صحيح (الشرطات السفلية للتنسيق فقط)
105.0           # عدد عشري (float)
0.05            # عدد عشري
1e12            # تدوين علمي: 1 × 10¹² = 1,000,000,000,000
```

### 0.3 النصوص (Strings)

```python
"World"
'WLD'
f"مرحبا {name}"   # f-string — تُدرج قيمة المتغير مباشرة
```

### 0.4 القوائم والقواميس والأصناف المرتّبة

```python
[10, 20, 30]                       # list (مرتّب، قابل للتعديل)
{"jobs": 150, "workforce": 160}    # dictionary (صندوق مُسمَّى)
(0.20, 33_000, 0.75, -0.15)        # tuple (مرتّب، غير قابل للتعديل)
```

**الـ Tuples** تبدو كالقوائم لكنها تستخدم **أقواساً مستديرة** ولا يمكن تعديلها بعد الإنشاء. ثابت `SKILLS` يستخدم tuples لتحزيم 4 قيم لكل مستوى مهاري.

### 0.5 الدوال

```python
def add_two(a: int, b: int) -> int:
    return a + b
```

- `def` تبدأ الدالة.
- `(a, b)` هي المعاملات.
- `-> int` تحدّد نوع القيمة المُعادة (توثيق فقط — Python لا تُطبّقه).
- `return` تُعيد قيمة.

### 0.6 تلميحات النوع (مجرّد تسميات)

```python
def fetch(country: str = "WLD") -> Dict[str, Any]:
    ...
```

تُقرأ: "تأخذ نصاً اسمه `country` بقيمة افتراضية `WLD`، وتُعيد قاموساً بمفاتيح نصية وقيم من أي نوع." Python تتجاهلها — هي مجرد توثيق.

### 0.7 معاملات الرياضيات

| الرمز | المعنى |
|---|---|
| `+`  `-`  `*`  `/` | جمع / طرح / ضرب / قسمة |
| `//` | قسمة صحيحة (تتجاهل الكسر): `5//2 = 2` |
| `**` | الأس: `5**2 = 25` |
| `%`  | الباقي: `5%2 = 1` |
| `+=` `-=` `*=` | تعديل في المكان: `x += 5` أي `x = x + 5` |
| `==` `!=` `<` `>` `<=` `>=` | مقارنات |

### 0.8 التحكم في التدفق

```python
if x > 10:
    print("كبير")
elif x > 5:
    print("متوسط")
else:
    print("صغير")

# الشكل المختصر في سطر واحد
result = "كبير" if x > 10 else "صغير"

# حلقة for
for item in [1, 2, 3]:
    print(item)

# حلقة مع الفهرس والقيمة معاً
for i, value in enumerate(["a", "b", "c"]):
    print(i, value)

# الدوران على مفاتيح القاموس (الافتراضي)
for k in {"x": 1, "y": 2}:
    print(k)
# الدوران على أزواج (مفتاح، قيمة)
for k, v in {"x": 1, "y": 2}.items():
    print(k, v)

# range(n) يُنتج 0, 1, ..., n-1
for i in range(5):
    print(i)
```

### 0.9 تعبيرات الضغط (حلقات مُدمجة)

```python
# تعبير قاموس
{k: v * 2 for k, v in {"a": 1, "b": 2}.items()}     # {"a": 2, "b": 4}

# تعبير قائمة
[x * x for x in range(5)]                            # [0, 1, 4, 9, 16]

# تعبير مُولِّد (بدون أقواس، كسول)
sum(x * 2 for x in [1, 2, 3])                        # 12
```

### 0.10 Try / Except — الفشل بأمان

```python
try:
    risky_thing()
except Exception:
    fallback()
```

يُستخدم لأي استدعاء خارجي (HTTP، ملفات) قد يفشل.

### 0.11 None و True و False

```python
True       # منطقي: نعم
False      # منطقي: لا
None       # قيمة "لا شيء"
x is None  # تحقق من أن x هي None (وليس x == None)
```

### 0.12 رموز خاصة ستراها

| الرمز | المعنى |
|---|---|
| `_` في الأرقام | `3_400_000_000` — فاصل للتنسيق فقط |
| `_` كمتغير | `for _ in ...` — "لا أهتم بهذه القيمة" |
| `_` في بداية الاسم | `_wb_latest` — تقليد: "خاص، للاستخدام الداخلي" |
| `f"..."` | f-string (تُدمج `{المتغيرات}`) |
| `"""..."""` | نص متعدد الأسطر / وثائق الدالة |
| `# تعليق` | تعليق، تتجاهله Python |
| `Optional[X]` | تلميح النوع: يمكن أن يكون X أو None |
| `Dict[str, Any]` | تلميح النوع: قاموس بمفاتيح نصية وقيم من أي نوع |

---

## الجزء 1 — تشريح الملف

الملف `backend/simulation.py` مكوّن من **481 سطراً** منظّمة في 7 أقسام:

| الأسطر | القسم | الدوال |
|---|---|---|
| 1-16 | وثيقة الوحدة + الاستيرادات | — |
| 19-68 | **A: الثوابت** | (لا شيء — بيانات فقط) |
| 71-151 | **B: البيانات الحيّة** (جالبات البنك الدولي) | 4 |
| 154-192 | **C: الرياضيات الأساسية** | 3 |
| 195-243 | **D: التفصيل المستنتج** | 4 |
| 246-368 | **E: مشغّل السيناريوهات** | 4 |
| 371-429 | **F: البيانات التاريخية + التحقق** | 2 |
| 432-481 | **G: المخرجات** | 3 |

**20 دالة إجمالاً** (مقابل 35+ في الأصل). جاء التقليص من:
- حذف 9 دوال ميتة (`apply_automation_by_skill`، `skill_upgrade_rate`، إلخ)
- دمج 7 دوال تحديث ماكرو صغيرة في دالة واحدة `step_year`
- دمج 4 دوال تعديل قطاع في دالة واحدة `sector_breakdown`

**أسلوب المعمارية:** كود إجرائي بحت. لا فئات (classes). كل دالة تأخذ مدخلات وتحوّلها وتُعيد مخرجات. سهل الاختبار، سهل القراءة من أعلى لأسفل.

**التصوّر الذهني:** فكّر في الملف كمصنع من 7 محطات:
1. الثوابت تضع الوصفات
2. جالبات البيانات الحيّة تجلب المكوّنات الحقيقية
3. الرياضيات الأساسية تُقدّم العالم بسنة واحدة
4. التفصيل المستنتج يقطّع العالم إلى مهارات/قطاعات/أجور
5. مشغّل السيناريوهات هو الحلقة الرئيسية التي تشغّل كل شيء لـ 20 سنة
6. التحقق يختبر الوصفة مقابل التاريخ
7. المخرجات تُعبّئ النتائج للـ API

---

## الجزء 2 — الاستيرادات وترويسة الملف (أسطر 1-16)

```python
1   """
2   محرّك محاكاة سوق العمل للذكاء الاصطناعي.
3
4   يُشغّل إسقاطاً سنوياً للوظائف والناتج المحلي والأجور والمهارات والقطاعات
5   واللامساواة في ظل ثلاثة سيناريوهات لتبنّي الذكاء الاصطناعي (بطيء / متوسط / سريع).
6
7   الحلقة السنوية في `run_scenario` تستدعي `step_year` (التحديث الكلي)،
8   `skill_breakdown`، `sector_breakdown`، `wages_by_skill`، و`gini_index`
9   بالتسلسل — اقرأ من أعلى لأسفل لتتابع كيف تتطوّر كل سنة.
10  """
```

**الأسطر 1-10:** **وثيقة الوحدة**. نص بثلاثة اقتباسات في أعلى الملف يصف ما الغرض منه. Python تتجاهله؛ الأدوات والبشر يقرؤونه. لاحظ أنه يخبر القارئ صراحةً بـ *ترتيب القراءة* — هذا مقصود (الملف هو التوثيق).

```python
11  from __future__ import annotations
```

**السطر 11:** يجعل تلميحات النوع كسولة — تصبح نصوصاً عادية بدل تقييمها أثناء التشغيل. يسمح بالإشارة إلى أنواع لم تُعرَّف بعد، ويحسّن قليلاً وقت البدء. كود نمطي في Python الحديث.

```python
13  import numpy as np
14  import pandas as pd
15  import requests
16  from typing import Any, Dict, Optional
```

**الأسطر 13-16:** الاستيرادات.
- `numpy as np` — رياضيات سريعة (متوسطات، مئينيات، exp، مصفوفات)
- `pandas as pd` — تصدير CSV فقط (استخدام واحد، السطر 480)
- `requests` — استدعاءات HTTP لـ API البنك الدولي
- `Any, Dict, Optional` — مفردات تلميحات النوع

---

## القسم A — الثوابت (أسطر 19-68)

هذه الكتلة تُعرّف كل "رقم سحري" تستخدمه المحاكاة، كلها في مكان واحد. لا كود، بيانات فقط. الهدف من التنظيف: **يجب أن يتمكن القارئ من ضبط أي معامل دون البحث في الملف**.

### المقاييس الأساسية (أسطر 23-34)

```python
23  BASE_YEAR          = 2026
24  # القيم الاحتياطية (تُستخدم فقط إذا كان API البنك الدولي غير متاح).
25  # الافتراضيات هي إجماليات عالمية مُعايَرة لأرقام 2024 الحقيقية:
26  #   إجمالي التوظيف   ≈ 3.4 مليار
27  #   القوى العاملة    ≈ 3.6 مليار
28  #   الناتج المحلي    ≈ 105 تريليون دولار
29  INITIAL_JOBS       = 3_400_000_000
30  INITIAL_WORKFORCE  = 3_600_000_000
31  INITIAL_GDP        = 105.0          # تريليون دولار
32  INITIAL_ADOPTION   = 0.05
33  WORKFORCE_GROWTH   = 0.008           # 0.8% سنوياً (أمم متحدة)
34  JOB_CREATION_RATIO = 0.60            # وظائف جديدة لكل وظيفة مُهجَّرة
```

| الثابت | القيمة | المعنى |
|---|---|---|
| `BASE_YEAR` | 2026 | السنة 0 للإسقاط |
| `INITIAL_JOBS` | 3.4 مليار | احتياطي إذا API البنك الدولي معطّل |
| `INITIAL_WORKFORCE` | 3.6 مليار | احتياطي |
| `INITIAL_GDP` | 105 تريليون | احتياطي (تريليون دولار) |
| `INITIAL_ADOPTION` | 0.05 | نسبة تبنّي الذكاء الاصطناعي عند البداية (5%) |
| `WORKFORCE_GROWTH` | 0.008 | 0.8% سنوياً (يتطابق مع توقعات الأمم المتحدة) |
| `JOB_CREATION_RATIO` | 0.60 | لكل $1 من الوظائف المُدمَّرة، الذكاء الاصطناعي يخلق $0.60 جديدة |

**الفرق الرئيسي عن الأصل:** القيم الاحتياطية الآن بـ **مقياس العالم الحقيقي** (المليارات). الكود القديم كان يستخدم 150 مليون وظيفة — رقم مُصغَّر للعب. إذا كان API البنك الدولي معطّلاً، هذا الكود لا يزال يُنتج مخرجات واقعية.

### `SCENARIO_RATES` (السطر 36)

```python
36  SCENARIO_RATES = {"slow": 0.03, "moderate": 0.05, "rapid": 0.08}
```

مقابض السيناريوهات الثلاثة. `moderate=5%` تعني 5% من الوظائف تتأتمت كل سنة (مُعدَّلة بمستوى تبنّي الذكاء الاصطناعي).

### قاموس `SKILLS` (أسطر 38-53) ⭐

```python
38  # المستويات المهارية — (حصة_القوى_العاملة، الأجر_الأساسي_دولار، خطر_الذكاء_الاصطناعي، ضغط_الأجر).
39  # الأجور مُعايَرة لمتوسط الأجور السنوية الوطنية OEWS مايو 2024 من BLS
40  # لمهن تمثيلية لكل مستوى:
41  #   L1_basic         تحضير الطعام / الصراف / عمال النظافة    ≈ $33K
42  #   L2_semi          مشغّلو الآلات / سائقو الشاحنات          ≈ $49K
43  #   L3_intermediate  مساعدو إداريون / ممرّضون               ≈ $73K
44  #   L4_advanced      مهندسون / مديرون عامون                 ≈ $115K
45  #   L5_expert        مديرون تنفيذيون / محامون / جراحون       ≈ $200K
46  # المصدر: https://www.bls.gov/oes/
SKILLS: Dict[str, tuple] = {
    "L1_basic":        (0.20,  33_000, 0.75, -0.15),
    "L2_semi":         (0.30,  49_000, 0.55, -0.08),
    "L3_intermediate": (0.25,  73_000, 0.35,  0.02),
    "L4_advanced":     (0.15, 115_000, 0.15,  0.12),
    "L5_expert":       (0.10, 200_000, 0.05,  0.22),
}
```

كل مستوى يُعيَّن بـ **tuple من 4 أرقام** بهذا الترتيب:

| الموضع | الاسم | المعنى |
|---|---|---|
| 0 | `share` | نسبة القوى العاملة في هذا المستوى |
| 1 | `base_wage` | الأجر السنوي الأساسي (دولار) |
| 2 | `ai_risk` | احتمالية أن يُحلّ الذكاء الاصطناعي محل عامل في هذا المستوى |
| 3 | `wage_pressure` | تغيّر الأجر عند التبنّي الكامل (سالب = انخفاض في الأجر) |

**كيف تقرأ** `("L1_basic", (0.20, 33_000, 0.75, -0.15))`:
> 20% من العمّال هم L1_basic. يكسبون $33K سنوياً. 75% من وظائف L1 في خطر. عند التبنّي الكامل للذكاء الاصطناعي تنخفض أجورهم 15%.

نمط الفهرسة `[0]`، `[1]`، `[2]`، `[3]` يُستخدم في كل مكان يُقرأ فيه هذا الثابت.

### قاموس `SECTORS` (أسطر 55-64)

```python
SECTORS: Dict[str, tuple] = {
    "Tech":          (0.10, 0.04, 0.06, 0.0),
    "Manufacturing": (0.22, 0.08, 0.01, 0.0),
    "Healthcare":    (0.13, 0.02, 0.04, 0.0),
    "Services":      (0.55, 0.06, 0.02, 0.0),
}
```

نفس خدعة تحزيم الـ tuple. خانة `0.0` محجوزة للاستخدام المستقبلي.

| القطاع | الحصة | معدّل الأتمتة | النمو |
|---|---|---|---|
| تقنية | 10% | 4% (منخفض — هم من يصنع الذكاء الاصطناعي) | 6% (الأعلى) |
| تصنيع | 22% | 8% (الأعلى — الروبوتات) | 1% (الأدنى) |
| صحة | 13% | 2% (الأدنى — اللمسة الإنسانية) | 4% |
| خدمات | 55% | 6% | 2% |

**هذه الحصص احتياطية فقط.** عندما يعمل API البنك الدولي، تُستبدَل بـ `fetch_world_bank_sectors` ببيانات حقيقية لكل دولة.

### `_BASELINE_CACHE` (السطر 68)

```python
_BASELINE_CACHE: Dict[str, Dict[str, Any]] = {}
```

**قاموس فارغ** يُستخدم كذاكرة تخزين مؤقت في الذاكرة. الشرطة السفلية الأولى تُشير إلى "خاص — لا تلمسه من خارج هذا الملف." عند استدعاء `get_country_baseline("USA")` لأول مرة، يجلب من البنك الدولي ويخزّن النتيجة هنا. الاستدعاء الثاني يعود فوراً.

هذا يمنع الوصول إلى API البنك الدولي في كل طلب محاكاة.

---

## القسم B — البيانات الحيّة: جالبات البنك الدولي (أسطر 71-151)

هذه هي **الإضافة الكبرى مقارنة بالأصل**. أربع دوال تسحب بيانات العالم الحقيقي عند الطلب.

### الدالة 1: `_wb_latest()` (أسطر 75-87)

```python
def _wb_latest(indicator: str, country: str = "WLD") -> Optional[float]:
    """تُعيد أحدث قيمة غير فارغة لمؤشر البنك الدولي."""
    url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
    try:
        resp = requests.get(url, params={"format": "json", "per_page": 20}, timeout=8)
        resp.raise_for_status()
        payload = resp.json()
        for row in payload[1]:
            if row.get("value") is not None:
                return float(row["value"])
    except Exception:
        return None
    return None
```

#### سطر بسطر

- **السطر الأول:** `_` في البداية = "مساعد خاص، لا تستورده من الخارج." تأخذ رمز المؤشر (مثل `"SL.EMP.TOTL"`) ورمز الدولة (افتراضي `"WLD"` = العالم كله). تُعيد إما رقماً أو `None`.
- **رابع سطر:** يبني الرابط. تنسيق البنك الدولي: `https://api.worldbank.org/v2/country/USA/indicator/SL.EMP.TOTL`.
- **طلب HTTP:** يُرسل GET. ينتظر 8 ثوانٍ كحد أقصى. يطلب JSON، حتى 20 صفاً.
- **raise_for_status:** يُثير خطأ إذا كان رمز HTTP من 4xx أو 5xx.
- **تحليل JSON:** البنك الدولي يُعيد `[البيانات_الوصفية، مصفوفة_البيانات]`.
- **الحلقة:** يمرّ على صفوف البيانات بالترتيب (الأحدث أولاً). يُعيد **أول قيمة غير فارغة** كـ float.
- **الاستثناء:** أي خطأ (شبكة، JSON، مفتاح مفقود) → يُعيد `None`.

**لماذا هذا التصميم:** البنك الدولي أحياناً يكون فيه فجوات (أحدث سنة قد تكون فارغة). هذه الدالة تتخطى الفارغة وتأخذ آخر رقم فعلي.

#### مثال عملي

`_wb_latest("NY.GDP.MKTP.CD", "USA")` → يسأل عن ناتج USA، يُعيد `~28.75e12` (قيمة 2023 الحقيقية).

`_wb_latest("INVALID", "USA")` → لا بيانات، يُعيد `None`.

### الدالة 2: `fetch_world_bank_baseline()` (أسطر 90-112)

```python
def fetch_world_bank_baseline(country: str = "WLD") -> Dict[str, Any]:
    employment  = _wb_latest("SL.EMP.TOTL",    country)
    labor_force = _wb_latest("SL.TLF.TOTL.IN", country)
    gdp_usd     = _wb_latest("NY.GDP.MKTP.CD", country)
    unem_pct    = _wb_latest("SL.UEM.TOTL.ZS", country)

    if employment is None and labor_force is not None and unem_pct is not None:
        employment = labor_force * (1.0 - unem_pct / 100.0)

    live = bool(labor_force and gdp_usd and (employment or unem_pct))
    return {
        "country":          country,
        "employment":       employment   or float(INITIAL_JOBS),
        "labor_force":      labor_force  or float(INITIAL_WORKFORCE),
        "gdp_trillion":     (gdp_usd / 1e12) if gdp_usd else INITIAL_GDP,
        "unemployment_pct": unem_pct,
        "live":             live,
    }
```54

#### ما تفعله

تجلب **4 مؤشرات من البنك الدولي** لدولة واحدة، ثم تُجمّع قاموساً نظيفاً.

#### الجزء الذكي

`SL.EMP.TOTL` (إجمالي عدد الوظائف) يُنشَر فقط للمجموع العالمي. إذا سألت عن USA تحصل على `None`. الحلّ:

```python
employment = labor_force × (1 − unemployment_rate / 100)
```

إذا كانت القوى العاملة 175 مليون ومعدّل البطالة 4.2%، فالتوظيف هو `175M × 0.958 = 167.7M`. مكافئ رياضياً.

#### علامة `live`

```python
live = bool(labor_force and gdp_usd and (employment or unem_pct))
```

تُقرأ: "`live` هي True إذا حصلنا على قوة عاملة وناتج محلي وعلى الأقل واحد من (التوظيف أو البطالة)."

#### سلسلة الاحتياط مع `or`

```python
"employment": employment or float(INITIAL_JOBS),
```

`or` في Python يُعيد **أول قيمة صحيحة**. إذا كان `employment` هو `None` (خاطئ)، يتراجع إلى `INITIAL_JOBS`.

#### مثال عملي

`fetch_world_bank_baseline("USA")`:
```python
{
    "country":          "USA",
    "employment":       167_500_000.0,   # مشتق: 174.8M × (1 - 4.2%)
    "labor_force":      174_800_000.0,   # حقيقي
    "gdp_trillion":     28.75,           # حقيقي ($28.75 تريليون)
    "unemployment_pct": 4.2,             # حقيقي
    "live":             True,
}
```

### الدالة 3: `fetch_world_bank_sectors()` (أسطر 115-141)

```python
def fetch_world_bank_sectors(country: str = "WLD") -> Dict[str, float]:
    agri = _wb_latest("SL.AGR.EMPL.ZS", country)
    ind  = _wb_latest("SL.IND.EMPL.ZS", country)
    srv  = _wb_latest("SL.SRV.EMPL.ZS", country)
    if not all((agri, ind, srv)):
        return {sec: SECTORS[sec][0] for sec in SECTORS}

    agri, ind, srv = agri / 100.0, ind / 100.0, srv / 100.0
    services_bucket = srv + agri
    return {
        "Tech":          round(services_bucket * 0.18, 4),
        "Manufacturing": round(ind, 4),
        "Healthcare":    round(services_bucket * 0.24, 4),
        "Services":      round(services_bucket * 0.58, 4),
    }
```

#### تحويل 3 قطاعات → 4 قطاعات

البنك الدولي يعطيك **3 دلاء** كنسب مئوية من التوظيف:
- `SL.AGR.EMPL.ZS` — الزراعة
- `SL.IND.EMPL.ZS` — الصناعة
- `SL.SRV.EMPL.ZS` — الخدمات (كل شيء آخر)

نحتاج **4 دلاء** (تقنية، تصنيع، صحة، خدمات). التحويل:

```
الصناعة  ──► تصنيع  (مطابقة 1:1)
الخدمات  ─┬► تقنية         (× 18%)
           ├► صحة           (× 24%)
           └► خدمات         (× 58%)
الزراعة   ──► تُدرج في دلو الخدمات قبل التقسيم
```

نسب 18/24/58 تقريبات لكيفية انقسام دلو الخدمات في بيانات BLS.

#### الدفاع بـ `all()`

```python
if not all((agri, ind, srv)):
    return {sec: SECTORS[sec][0] for sec in SECTORS}
```

`all((a, b, c))` تُعيد `True` فقط إذا كان كل عنصر صحيحاً. إذا كان أي مؤشر `None`، يتراجع للحصص المُرمَّزة في `SECTORS`.

#### تعيين متعدد

```python
agri, ind, srv = agri / 100.0, ind / 100.0, srv / 100.0
```

يقسم الثلاثة على 100 ويُعيد تعيينهم بالتوازي. البنك الدولي يُعيد نسباً مئوية (مثل `45.3`)، نحن نريد كسوراً (`0.453`).

#### مثال عملي لـ USA

البنك الدولي يُعيد: زراعة 1.4%، صناعة 18.9%، خدمات 79.7%.
```
agri=0.014, ind=0.189, srv=0.797
services_bucket = 0.797 + 0.014 = 0.811
تقنية         = 0.811 × 0.18 = 0.1460   (14.6%)
تصنيع         = 0.189                   (18.9%)
صحة           = 0.811 × 0.24 = 0.1946   (19.5%)
خدمات         = 0.811 × 0.58 = 0.4703   (47.0%)
                                  المجموع = 100.1%  ✓
```

### الدالة 4: `get_country_baseline()` (أسطر 144-151) — ذاكرة التخزين المؤقت

```python
def get_country_baseline(country: str = "WLD") -> Dict[str, Any]:
    """القيم الأساسية المخزّنة مؤقتاً لكل دولة."""
    if country in _BASELINE_CACHE:
        return _BASELINE_CACHE[country]
    base = fetch_world_bank_baseline(country)
    base["sectors"] = fetch_world_bank_sectors(country)
    _BASELINE_CACHE[country] = base
    return base
```

**نمط التخزين المؤقت القياسي:**
1. تحقق إذا كانت لدينا البيانات مسبقاً → أعد فوراً.
2. جلب الأساس + القطاعات (كل منها يُجري 1-4 استدعاءات HTTP).
3. خزّن في الذاكرة المؤقتة.
4. أعد.

**الأثر الصافي:** يُضرَب API البنك الدولي مرة واحدة بالكثير **لكل دولة**. بعد ذلك كل محاكاة تعيد استخدام النتيجة المخزّنة.

---

## القسم C — الرياضيات الأساسية (أسطر 154-192)

ثلاث دوال. قلب التحديث السنوي.

### الدالة 5: `ai_adoption()` (أسطر 158-161) ⭐

```python
def ai_adoption(year_index: int, speed: float = 1.0) -> float:
    """منحنى S لوجستي، نقطة وسطى عند السنة 10، يُعيد قيمة بين 0 و1."""
    k = 0.35 * speed
    return 1.0 / (1.0 + np.exp(-k * (year_index - 10.0)))
```

**الدالة اللوجستية** — تُستخدم لكل منحنى تبنّي تقنية في التاريخ (الهاتف، التلفاز، الإنترنت، الهواتف الذكية، السيارات الكهربائية).

#### الرياضيات

```
                 1
adoption =  ─────────────────────────
            1 + e^(-k × (year − 10))
```

- عند السنة 0: تُعيد ~3% (المتبنّون الأوائل)
- عند السنة 10: تُعيد بالضبط 50% (نقطة الانعطاف)
- عند السنة 20: تُعيد ~97% (التشبع)

#### معامل `speed`

`speed=0.5` → منحنى أكثر انبساطاً، تبنّي أبطأ.
`speed=1.5` → منحنى أكثر حدة، تبنّي متفجّر.

هكذا تُنتج السيناريوهات الثلاثة مستقبلات مختلفة.

⚠ **تنبيه تسمية:** `k` هنا حرف رياضي لـ "الانحدار" — لا علاقة له بـ `k, v` في تعبيرات القاموس في أماكن أخرى.

### الدالة 6: `initial_state()` (أسطر 164-172)

```python
def initial_state(country: str = "WLD") -> Dict[str, float]:
    base = get_country_baseline(country)
    return {
        "total_jobs":   float(base["employment"]),
        "workforce":    float(base["labor_force"]),
        "ai_adoption":  INITIAL_ADOPTION,
        "_gdp_base":    float(base["gdp_trillion"]),
        "_country":     country,
    }
```

**ما تغيّر عن الأصل:** الآن تأخذ معامل `country` وتسحب قيماً حيّة عبر `get_country_baseline`.

الشرطة السفلية في `_gdp_base` و`_country` تُشير إلى "حالة داخلية، ليست جزءاً من المخرجات العامة."

#### مثال عملي

`initial_state("IND")` → `{total_jobs: 591.6M, workforce: 617.6M, ai_adoption: 0.05, _gdp_base: 3.91, _country: "IND"}`.

### الدالة 7: `step_year()` (أسطر 175-192) ⭐ محرّك السنة الواحدة

```python
def step_year(state: Dict[str, float], year_index: int,
              auto_rate: float, speed: float) -> Dict[str, float]:
    """يُقدّم الحالة الكلية بسنة واحدة. يُعدّل `state` في مكانه."""
    state["ai_adoption"] = ai_adoption(year_index, speed)
    adoption = state["ai_adoption"]

    jobs_lost    = state["total_jobs"] * auto_rate * adoption
    jobs_created = state["total_jobs"] * auto_rate * adoption * JOB_CREATION_RATIO
    state["total_jobs"] = max(0.0, state["total_jobs"] - jobs_lost + jobs_created)
    state["workforce"] *= (1.0 + WORKFORCE_GROWTH)

    gdp_base    = state.get("_gdp_base", INITIAL_GDP)
    unem        = max(0.0, (state["workforce"] - state["total_jobs"]) / state["workforce"])
    productivity= 1.0 + (adoption ** 0.7) * 0.85
    gdp         = gdp_base * (1.0 + (productivity - 1.0) * 0.6 - unem * 0.4)
    spending    = gdp * max(0.30, 0.68 - unem * 1.2)

    return {"unem": unem, "productivity": productivity, "gdp": gdp, "spending": spending}
```

هذه **الدالة الواحدة تحلّ محل 7 دوال** من الكود الأصلي.

#### خطوة بخطوة

| السطر | ما يفعله |
|---|---|
| 1-2 | تحديث تبنّي الذكاء الاصطناعي من منحنى S، نسخ لمتغير قصير |
| 3 | الوظائف المفقودة = (الوظائف الحالية) × (معدّل السيناريو) × (تبنّي الذكاء الاصطناعي الحالي) |
| 4 | الوظائف المُنشأة = نفس الصيغة × نسبة 0.60 |
| 5 | التحديث الصافي: `max(0, ...)` يضع حداً أدنى عند الصفر (لا يمكن أن تكون الوظائف سالبة) |
| 6 | القوى العاملة تنمو 0.8% سنوياً |
| 7 | قراءة قاعدة الناتج المحلي للدولة (أو الاحتياط) |
| 8 | البطالة = (القوى العاملة − الوظائف) / القوى العاملة، حدّ أدنى 0 |
| 9 | الإنتاجية = 1 + تبنّي^0.7 × 0.85 (عوائد متناقصة) |
| 10 | الناتج المحلي = الأساس × (1 + 0.6 × مكسب_الإنتاجية − 0.4 × ثقل_البطالة) |
| 11 | الإنفاق = الناتج المحلي × max(30%, 68% − البطالة × 1.2) |
| 12 | إعادة جميع المقاييس الأربعة المشتقة في قاموس أنيق |

#### ملاحظة التعديل في المكان

الدالة **تُعدّل `state` في مكانه** (تُعدّل `state["ai_adoption"]`، `state["total_jobs"]`، `state["workforce"]` مباشرةً). القاموس المُعاد يحتوي فقط على المقاييس *المشتقة*. هذا انفصال مقصود.

#### مثال عملي (USA، السنة 0، السيناريو المتوسط)

```
المدخلات:
  state["total_jobs"]  = 167,500,000
  state["workforce"]   = 174,800,000
  state["_gdp_base"]   = 28.75
  year_index = 0,  auto_rate = 0.05,  speed = 1.0

adoption       = ai_adoption(0, 1.0) ≈ 0.029
jobs_lost      = 167.5M × 0.05 × 0.029  ≈ 242,875
jobs_created   = 242,875 × 0.60         ≈ 145,725
total_jobs جديد = 167,500,000 - 242,875 + 145,725 ≈ 167,402,850
workforce جديد  = 174,800,000 × 1.008    ≈ 176,198,400
unem           = (176.2M − 167.4M) / 176.2M ≈ 0.0499 (5.0%)
productivity   = 1 + 0.029^0.7 × 0.85   ≈ 1.077
gdp            = 28.75 × (1 + 0.077×0.6 − 0.05×0.4) ≈ 28.91
spending       = 28.91 × (0.68 − 0.05×1.2) ≈ 28.91 × 0.62 ≈ 17.92
```

---

## القسم D — التفصيل المستنتج (أسطر 195-243)

أربع دوال تُنتج **التفاصيل السنوية** التي تقرأها مخططات لوحة التحكم.

### الدالة 8: `skill_breakdown()` (أسطر 204-205)

```python
def skill_breakdown(state: Dict[str, float]) -> Dict[str, int]:
    return {tier: int(state["workforce"] * SKILLS[tier][0]) for tier in SKILLS}
```

**دالة بسطر واحد** (بعد تعليق من 4 أسطر يشرح تبسيطاً مقصوداً).

تعبير القاموس يُقرأ: "لكل مستوى في SKILLS، اضرب القوى العاملة في `SKILLS[tier][0]` (الحصة، وهي العنصر الأول من الـ tuple)، وحوّل لعدد صحيح."

نتيجة مثال: `{L1_basic: 35M, L2_semi: 52M, L3_intermediate: 44M, L4_advanced: 26M, L5_expert: 17M}` لقوى عاملة 174M.

### الدالة 9: `wages_by_skill()` (أسطر 208-210)

```python
def wages_by_skill(adoption: float) -> Dict[str, float]:
    return {tier: round(SKILLS[tier][1] * (1.0 + SKILLS[tier][3] * adoption), 0)
            for tier in SKILLS}
```

نفس نمط تعبير القاموس. لكل مستوى:
- `SKILLS[tier][1]` = الأجر الأساسي (الفهرس 1)
- `SKILLS[tier][3]` = ضغط الأجر (الفهرس 3)
- الأجر النهائي = `الأساس × (1 + الضغط × التبنّي)`

عند التبنّي الكامل (1.0):
- L1: $33K × 0.85 = $28K (انخفاض 15%)
- L5: $200K × 1.22 = $244K (ارتفاع 22%)

**هذا هو محرّك اللامساواة.** أجور المهارات المنخفضة تنكمش، أجور المهارات العالية تتوسّع.

### الدالة 10: `sector_breakdown()` (أسطر 213-230)

```python
def sector_breakdown(state: Dict[str, float], auto_rate: float) -> Dict[str, int]:
    adoption = state["ai_adoption"]
    total    = state["total_jobs"]
    country  = state.get("_country", "WLD")
    shares   = get_country_baseline(country).get("sectors") or {sec: SECTORS[sec][0] for sec in SECTORS}
    jobs = {sec: total * shares.get(sec, SECTORS[sec][0]) for sec in SECTORS}

    # انكماش الأتمتة + النمو بدفع الذكاء الاصطناعي (لكل قطاع)
    for sec, (_, sector_auto, growth, _r) in SECTORS.items():
        jobs[sec] *= (1.0 - sector_auto * auto_rate * adoption)
        jobs[sec] *= (1.0 + growth * adoption)

    # التأثير التسرّبي: نجاح التقنية يُفيد الخدمات والصحة، يضرّ التصنيع.
    spillover = jobs["Tech"] * 0.02 * adoption
    jobs["Services"]      += spillover * 0.5
    jobs["Manufacturing"] -= spillover * 0.3
    jobs["Healthcare"]    += spillover * 0.1
    return {sec: int(v) for sec, v in jobs.items()}
```

**هذه الدالة الواحدة تحلّ محل 4 دوال** من الأصل.

#### فكّ التعبئة في الـ for loop

```python
for sec, (_, sector_auto, growth, _r) in SECTORS.items():
```

هذا **Python مكثّف.** كل عنصر في `SECTORS.items()` هو زوج `(مفتاح، قيمة)` حيث القيمة هي tuple رباعي. نفكّ:
- `sec` = المفتاح (مثل `"Tech"`)
- `(_, sector_auto, growth, _r)` = الـ tuple الرباعي، نتجاهل الموضعين 0 و3 بـ `_`

#### التأثير التسرّبي

```python
spillover = jobs["Tech"] × 0.02 × adoption
```

كمية صغيرة من وظائف التقنية "تتسرّب" للقطاعات المجاورة. انقسام 50%/-30%/10% يعني: نصف هالة التقنية يذهب للخدمات، 30% يُقلّص من التصنيع، 10% يذهب للصحة.

#### مثال عملي

التقنية لديها 16.4 مليون وظيفة بعد الأتمتة+النمو، التبنّي 0.5:
```
spillover = 16,400,000 × 0.02 × 0.5 = 164,000
الخدمات      += 164,000 × 0.5 =  +82,000
التصنيع      -= 164,000 × 0.3 =  -49,200
الصحة        += 164,000 × 0.1 =  +16,400
```

### الدالة 11: `gini_index()` (أسطر 233-243)

```python
def gini_index(wages: Dict[str, float], skills: Dict[str, int]) -> float:
    """معامل جيني (0=متساوٍ، ~1=أقصى لامساواة)."""
    incomes = []
    for tier, wage in wages.items():
        count = max(1, skills.get(tier, 1) // 10_000_000)
    incomes.extend([wage] * count)
    if not incomes:
        return 0.0
    arr = np.array(sorted(incomes), dtype=float)
    n   = arr.size
    return float((2 * np.sum(np.arange(1, n + 1) * arr) / (n * arr.sum())) - (n + 1) / n)
```

#### التحسين الذكي

```python
count = max(1, skills.get(tier, 1) // 10_000_000)
```

النهج الساذج: مدخل دخل واحد لكل عامل → مليارات العناصر، رياضيات جيني بطيئة.

هذا النهج: **عيّنة واحدة لكل 10 ملايين عامل**، حدّ أدنى 1. إذاً 35 مليون عامل L1 يصبحون 3 عيّنات. حجم القائمة الكلي: 15-20 عنصراً، ميكروثوانٍ للمعالجة.

**لماذا يعمل:** جيني يقيس *شكل* التوزيع، وليس الحجم المطلق. النسب تُحفَظ.

#### معادلة جيني القياسية

```
        2 × Σ(i × y_i)       n+1
G = ──────────────────── − ───────
        n × Σy              n
```

المخرج بين 0 (مساواة تامة) و~1 (أقصى لامساواة).

---

## القسم E — مشغّل السيناريوهات (أسطر 246-368)

أربع دوال تقود المحاكاة.

### الدالة 12: `run_scenario()` (أسطر 250-299) ⭐ الدالة الرئيسية

```python
def run_scenario(scenario: str = "moderate", horizon: int = 20,
                 adoption_speed: float = 1.0,
                 override_rate: Optional[float] = None,
                 country: str = "WLD") -> Dict[str, Any]:
    """يشغّل محاكاة N سنة ويُعيد قاموس نتائج جاهزاً لـ JSON."""
    auto_rate = override_rate if override_rate is not None else SCENARIO_RATES.get(scenario, 0.05)
    state = initial_state(country)

    results: Dict[str, Any] = {
        "scenario":         scenario,
        "country":          country,
        "automation_rate":  auto_rate,
        "years":            [],
        "unemployment":     [],
        "gdp":              [],
        "total_jobs":       [],
        "ai_adoption":      [],
        "gini":             [],
        "productivity":     [],
        "consumer_spending":[],
        "skills":  {tier: [] for tier in SKILLS},
        "wages":   {tier: [] for tier in SKILLS},
        "sectors": {sec:  [] for sec  in SECTORS},
    }

    for i in range(horizon):
        step    = step_year(state, i, auto_rate, adoption_speed)
        skills  = skill_breakdown(state)
        sectors = sector_breakdown(state, auto_rate)
        wages   = wages_by_skill(state["ai_adoption"])
        gini    = gini_index(wages, skills)

        results["years"].append(BASE_YEAR + i)
        results["unemployment"].append(round(step["unem"] * 100, 2))
        results["gdp"].append(round(step["gdp"], 3))
        results["total_jobs"].append(int(state["total_jobs"]))
        results["ai_adoption"].append(round(state["ai_adoption"] * 100, 2))
        results["gini"].append(round(gini, 4))
        results["productivity"].append(round(step["productivity"], 4))
        results["consumer_spending"].append(round(step["spending"], 3))

        for tier in SKILLS:
            results["skills"][tier].append(skills[tier])
            results["wages"][tier].append(wages[tier])
        for sec in SECTORS:
            results["sectors"][sec].append(sectors[sec])

    results["summary"] = summarize(results)
    results["report"]  = report(results)
    return results
```

**الدالة الوحيدة التي يستدعيها نقطة الوصول `/api/simulate/{scenario}`**.

#### خمسة معاملات

- `scenario` — `"slow"` أو `"moderate"` أو `"rapid"` (افتراضي متوسط)
- `horizon` — عدد السنوات للإسقاط (افتراضي 20)
- `adoption_speed` — مضاعف لانحدار منحنى S (افتراضي 1.0)
- `override_rate` — هروب اختياري تستخدمه `sensitivity()` لاختبار تشويشات ±20%
- `country` — رمز دولة البنك الدولي (افتراضي `"WLD"` = العالم)

#### نمط التجاوز

```python
auto_rate = override_rate if override_rate is not None else SCENARIO_RATES.get(scenario, 0.05)
```

"إذا أعطى المستدعي معدلاً صريحاً، استخدمه؛ وإلا ابحث عن السيناريو؛ إذا كان السيناريو مجهولاً، افتراض 5%."

#### الحاويات المُخصّصة مسبقاً

قوائم/قواميس فارغة لملئها أثناء الحلقة. التخصيص المسبق يضمن وجود كل مفتاح متوقّع من البداية.

#### الحلقة السنوية

**الترتيب مهم:**
1. `step_year` يُعدّل `state` (يُقدّم الوظائف والقوى العاملة والتبنّي).
2. `skill_breakdown` يقرأ القوى العاملة الجديدة.
3. `sector_breakdown` يقرأ الوظائف الجديدة.
4. `wages_by_skill` يقرأ التبنّي الجديد.
5. `gini_index` يقرأ الأجور+المهارات المحسوبة للتو.

بعد 20 تكرار، كل قائمة فيها 20 قيمة.

### الدالة 13: `compare_scenarios()` (أسطر 302-305)

```python
def compare_scenarios(horizon: int = 20, adoption_speed: float = 1.0,
                       country: str = "WLD") -> Dict[str, Any]:
    return {name: run_scenario(name, horizon, adoption_speed, country=country)
            for name in SCENARIO_RATES}
```

**تعبير قاموس من 3 أسطر** يشغّل `run_scenario` مرة لكل سيناريو.

يُعيد: `{"slow": {...}, "moderate": {...}, "rapid": {...}}`.

### الدالة 14: `monte_carlo()` (أسطر 308-339) ⭐

```python
def monte_carlo(n_simulations: int = 1000, horizon: int = 20) -> Dict[str, Any]:
    """N مستقبل عشوائي بتشويش المعاملات — يُعيد المتوسط + فرق ثقة 95%."""
    rng = np.random.default_rng(42)
    unem_matrix = np.zeros((n_simulations, horizon))
    gdp_matrix  = np.zeros((n_simulations, horizon))

    for sim in range(n_simulations):
        auto_rate = rng.uniform(0.02, 0.10)
        speed     = rng.uniform(0.60, 1.50)
        state     = initial_state("WLD")
        state["total_jobs"] *= rng.uniform(0.95, 1.05)
        state["workforce"]  *= rng.uniform(0.95, 1.05)
        for i in range(horizon):
            step = step_year(state, i, auto_rate, speed)
            unem_matrix[sim, i] = step["unem"] * 100
            gdp_matrix[sim, i]  = step["gdp"]

    years = list(range(BASE_YEAR, BASE_YEAR + horizon))
    return {
        "years":         years,
        "n_simulations": n_simulations,
        "unemployment": {
            "mean":  np.mean(unem_matrix, axis=0).round(2).tolist(),
            "lower": np.percentile(unem_matrix, 2.5,  axis=0).round(2).tolist(),
            "upper": np.percentile(unem_matrix, 97.5, axis=0).round(2).tolist(),
        },
        "gdp": {
            "mean":  np.mean(gdp_matrix, axis=0).round(3).tolist(),
            "lower": np.percentile(gdp_matrix, 2.5,  axis=0).round(3).tolist(),
            "upper": np.percentile(gdp_matrix, 97.5, axis=0).round(3).tolist(),
        },
    }
```

تشغّل المحاكاة **1000 مرة بمدخلات عشوائية**، ثم تحسب المتوسط + فرق ثقة 95%.

#### مولّد الأرقام العشوائية بـ seed ثابت

```python
rng = np.random.default_rng(42)
```

الـ seed 42 = قابلية التكرار. نفس الـ seed → نفس الأرقام العشوائية → نفس المخرجات دائماً. حيوي للتصحيح.

#### المصفوفات المُخصّصة مسبقاً

```python
unem_matrix = np.zeros((n_simulations, horizon))   # شبكة 1000 × 20 من الأصفار
```

`axis=0` لاحقاً تعني "احسب الإحصاءات لأسفل كل عمود" (قيمة واحدة لكل سنة، عبر جميع المحاكاة).

#### عشوائية كل محاكاة

- `auto_rate` ∈ uniform[0.02, 0.10] — من بطيء لفائق السرعة
- `speed` ∈ uniform[0.60, 1.50] — من منبسط لحاد
- وظائف/قوى عاملة أولية تتأرجح ±5% — لامعرفتنا بالحالة الأولية

#### نطاقات المئيني

```python
"lower": np.percentile(unem_matrix, 2.5,  axis=0).round(2).tolist(),
"upper": np.percentile(unem_matrix, 97.5, axis=0).round(2).tolist(),
```

`المئيني 2.5` = القيمة التي تحتها 2.5% فقط من المحاكاة.
`المئيني 97.5` = القيمة التي فوقها 2.5% فقط من المحاكاة.

معاً يشكّلان **فرق ثقة 95%** — النطاق المظلّل في صفحة التحقق.

### الدالة 15: `sensitivity()` (أسطر 342-368)

```python
def sensitivity(scenario: str = "moderate", country: str = "WLD") -> Dict[str, Any]:
    """تشويش ±20% على كل معامل رئيسي — التأثير على بطالة السنة الأخيرة."""
    base = run_scenario(scenario, country=country)
    base_unem = base["unemployment"][-1]
    base_rate = SCENARIO_RATES[scenario]

    high_rate  = run_scenario(scenario, override_rate=base_rate * 1.20, country=country)["unemployment"][-1]
    low_rate   = run_scenario(scenario, override_rate=base_rate * 0.80, country=country)["unemployment"][-1]
    high_speed = run_scenario(scenario, adoption_speed=1.20, country=country)["unemployment"][-1]
    low_speed  = run_scenario(scenario, adoption_speed=0.80, country=country)["unemployment"][-1]

    return {
        "automation_rate": {
            "base": round(base_unem, 2),
            "high": round(high_rate, 2),
            "low":  round(low_rate, 2),
            "impact_high": round(high_rate - base_unem, 2),
            "impact_low":  round(low_rate  - base_unem, 2),
        },
        "adoption_speed": { ... },
    }
```

**أنظف بكثير من الأصل.** الحيلة: `run_scenario` الآن يقبل `override_rate`، فيمكننا تشويش معدّل الأتمتة دون تكرار منطق الحلقة.

#### ما تعنيه المخرجات

```python
{
  "automation_rate": {"base": 8.5, "low": 6.1, "high": 11.2, "impact_low": -2.4, "impact_high": +2.7},
  "adoption_speed":  {"base": 8.5, "low": 7.4, "high":  9.8, "impact_low": -1.1, "impact_high": +1.3},
}
```

القراءة: "إذا ارتفع معدّل الأتمتة 20%، ترتفع البطالة النهائية 2.7 نقطة مئوية." يُخبر صانعي السياسات أي المقابض أكثر أهمية.

---

## القسم F — البيانات التاريخية + التحقق (أسطر 371-429)

دالتان لتأريض المحاكاة في الواقع الماضي.

### `_SYNTHETIC_UNEM` (مصفوفة احتياطية)

```python
_SYNTHETIC_UNEM = [6.5, 6.3, 5.8, 6.0, 5.5, 5.2, 5.8, 5.6, 5.4, 6.0,
                   8.5, 7.8, 7.2, 6.8, 6.3, 5.9, 5.6, 5.3, 5.1, 5.0,
                   8.9, 5.7, 5.4, 5.1, 4.9]
```

25 قيمة بطالة مصنوعة يدوياً تتطابق مع **اتجاه البنك الدولي الحقيقي** — لاحظ القمم:
- الفهرس 10 (سنة 2010): **8.5%** = ذروة ما بعد الأزمة المالية
- الفهرس 20 (سنة 2020): **8.9%** = صدمة COVID-19

تُستخدم فقط إذا كان API البنك الدولي غير متاح.

### الدالة 16: `fetch_world_bank_unemployment()` (أسطر 382-399)

```python
def fetch_world_bank_unemployment(start: int = 2000, end: int = 2020) -> Dict[str, list]:
    url = "https://api.worldbank.org/v2/country/WLD/indicator/SL.UEM.TOTL.ZS"
    try:
        resp = requests.get(url, params={"date": f"{start}:{end}", "format": "json", "per_page": 100}, timeout=10)
        resp.raise_for_status()
        payload = resp.json()
        rows = sorted(
            ((int(r["date"]), r["value"]) for r in payload[1] if r["value"] is not None),
            key=lambda x: x[0],
        )
        if rows:
            return {"years": [y for y, _ in rows], "values": [v for _, v in rows]}
    except Exception:
        pass
    years  = list(range(start, end + 1))
    values = _SYNTHETIC_UNEM[: len(years)]
    return {"years": years, "values": values}
```

**تُعيد قاموساً، وليس DataFrame** (أحد التنظيفات عن الأصل). أبسط بكثير للمعالجة اللاحقة.

#### التعبير المولّد ثم الفرز

```python
rows = sorted(
    ((int(r["date"]), r["value"]) for r in payload[1] if r["value"] is not None),
    key=lambda x: x[0],
)
```

خطوة بخطوة:
1. **تعبير مولّد** (أقواس مستديرة): يُنتج أزواج `(سنة، قيمة)` لكل صف غير فارغ.
2. `sorted(..., key=lambda x: x[0])` يرتّب حسب العنصر الأول (السنة).
3. النتيجة: `[(2000, 6.5), (2001, 6.3), ...]` بترتيب تصاعدي.

#### فصل القائمة الواحدة لقائمتين

```python
return {"years": [y for y, _ in rows], "values": [v for _, v in rows]}
```

لكل زوج في `rows`، افكّ `(y, _)` واحتفظ بـ `y` فقط، ثم قائمة منفصلة من `v` فقط.

### الدالة 17: `validate()` (أسطر 402-429) — الاختبار الرجعي

```python
def validate(start: int = 2000, end: int = 2020) -> Dict[str, Any]:
    """اختبار رجعي: شغّل النموذج من `start` وقارن مع البطالة الحقيقية."""
    real = fetch_world_bank_unemployment(start, end)
    actual = real["values"]
    years  = real["years"]

    state = {"total_jobs": 120_000_000.0, "workforce": 130_000_000.0, "ai_adoption": 0.01}
    predicted = []
    for i, _ in enumerate(years):
        state["ai_adoption"] = ai_adoption(i, speed=0.8) * 0.5
        adoption = state["ai_adoption"]
        lost     = state["total_jobs"] * 0.05 * adoption
        created  = lost * JOB_CREATION_RATIO
        state["total_jobs"] = max(0.0, state["total_jobs"] - lost + created)
        state["workforce"] *= (1.0 + WORKFORCE_GROWTH)
        unem = max(0.0, (state["workforce"] - state["total_jobs"]) / state["workforce"]) * 100
        predicted.append(round(unem, 2))

    mae = float(np.mean(np.abs(np.array(actual, dtype=float) - np.array(predicted, dtype=float))))
    return {
        "years":     years,
        "actual":    actual,
        "predicted": predicted,
        "mae":       round(mae, 4),
        "accuracy":  round(max(0.0, 100.0 - mae * 10.0), 2),
        "label":     f"الاختبار الرجعي للنموذج {start}-{end}",
    }
```

#### ما تُثبته هذه الدالة

**نفس المحرّك الذي يُسقط للأمام يستطيع إعادة تكوين الماضي.** إذا كان MAE منخفضاً، تثق بالإسقاطات أكثر.

#### حالة بداية مختلفة

اقتصاد سنة 2000 كان أصغر. وظائف/قوى عاملة/تبنّي أولية مختلفة عن 2026.

#### منحنى S مُخمَّد

```python
state["ai_adoption"] = ai_adoption(i, speed=0.8) * 0.5
```

تبنّي الذكاء الاصطناعي كان ضئيلاً قبل 2018. الضرب في 0.5 يُبقي التبنّي التاريخي منخفضاً بشكل واقعي.

#### حساب MAE

```python
mae = float(np.mean(np.abs(np.array(actual) - np.array(predicted))))
```

1. تحويل القوائم لمصفوفات NumPy
2. الطرح عنصراً بعنصر (يُنتج متجه الأخطاء)
3. `np.abs` → كلها موجبة
4. `np.mean` → المتوسط

إذا MAE = 0.5، التوقعات خاطئة بـ 0.5% في المتوسط — ممتاز. إذا MAE = 5، النموذج ضعيف.

#### درجة الدقة المخصّصة

```python
"accuracy": round(max(0.0, 100.0 - mae * 10.0), 2),
```

يحوّل MAE لنسبة مئوية مألوفة:
- MAE 0 → دقة 100%
- MAE 5 → دقة 50%
- MAE 10+ → دقة 0% (مُقيَّدة)

ليست مقياساً إحصائياً قياسياً، مجرد درجة حدسية للوحة التحكم.

---

## القسم G — المخرجات (أسطر 432-481)

ثلاث دوال تُعبّئ النتائج للاستهلاك.

### الدالة 18: `summarize()` (أسطر 436-447)

```python
def summarize(results: Dict[str, Any]) -> Dict[str, Any]:
    summary = {}
    for key in ("unemployment", "gdp", "ai_adoption", "gini", "productivity"):
        arr = np.array(results.get(key, []), dtype=float)
        if arr.size:
            summary[key] = {
                "mean": round(float(np.mean(arr)), 4),
                "std":  round(float(np.std(arr)),  4),
                "min":  round(float(np.min(arr)),  4),
                "max":  round(float(np.max(arr)),  4),
            }
    return summary
```

لكل مقياس من 5 مقاييس: يحسب المتوسط والانحراف المعياري والحد الأدنى والأقصى.

#### التكرار على tuple

```python
for key in ("unemployment", "gdp", ...):
```

التكرار على tuple مطابق للتكرار على قائمة — لكن الـ tuples غير قابلة للتعديل، مما يُشير إلى "هذه القائمة لن تتغيّر."

#### حارس `.size`

```python
if arr.size:
```

`arr.size` هو عدد العناصر. `if 0:` خاطئ؛ `if 5:` صحيح. يتخطى المصفوفات الفارغة لتجنّب أخطاء متوسط-لا-شيء.

### الدالة 19: `report()` (أسطر 450-463)

```python
def report(results: Dict[str, Any]) -> Dict[str, Any]:
    years = results.get("years", [])
    return {
        "scenario":               results.get("scenario", "unknown"),
        "automation_rate":        results.get("automation_rate", 0.05),
        "horizon_years":          len(years),
        "start_year":             years[0]  if years else BASE_YEAR,
        "end_year":               years[-1] if years else BASE_YEAR + 19,
        "final_unemployment_pct": results["unemployment"][-1] if results.get("unemployment") else 0,
        "final_gdp_trillion":     results["gdp"][-1]          if results.get("gdp")          else 0,
        "final_ai_adoption_pct":  results["ai_adoption"][-1]  if results.get("ai_adoption")  else 0,
        "final_gini":             results["gini"][-1]         if results.get("gini")         else 0,
        "peak_unemployment":      max(results["unemployment"]) if results.get("unemployment") else 0,
    }
```

القاموس الرئيسي. يُغذّي بطاقات KPI في لوحة التحكم، وكذلك المستشار اللغوي.

#### النمط الدفاعي

```python
years[0] if years else BASE_YEAR
```

`if years` صحيح عندما القائمة غير فارغة. يحمي من المدخلات الفارغة.

#### `[-1]` في كل مكان

`list[-1]` = آخر عنصر. قيم "السنة الأخيرة" تأتي من هذه الحيلة.

### الدالة 20: `export_csv()` (أسطر 466-481)

```python
def export_csv(results: Dict[str, Any], filepath: str = "simulation_output.csv") -> str:
    rows = []
    for i, year in enumerate(results["years"]):
        row = {
            "year":         year,
            "unemployment": results["unemployment"][i],
            "gdp":          results["gdp"][i],
            "total_jobs":   results["total_jobs"][i],
            "ai_adoption":  results["ai_adoption"][i],
            "gini":         results["gini"][i],
        }
        for sec in results["sectors"]:
            row[f"sector_{sec}"] = results["sectors"][sec][i]
        rows.append(row)
    pd.DataFrame(rows).to_csv(filepath, index=False)
    return filepath
```

تبني قاموساً واحداً لكل سنة. الـ f-string `f"sector_{sec}"` يبني أسماء أعمدة مثل `sector_Tech`، `sector_Manufacturing`، إلخ.

pandas تحوّل قائمة من القواميس لجدول وتكتب CSV. `index=False` يتخطى أرقام الصفوف التلقائية من pandas.

---

## الروابط بين الأقسام

```
┌──────────────────────────────────────────────────────────────────────┐
│                      طلب /api/simulate                              │
└─────────────────────────────┬────────────────────────────────────────┘
                              ▼
                    ┌─────────────────────┐
                    │   run_scenario()    │  (القسم E)
                    └─────────┬───────────┘
                              │
                              ▼
                ┌────────────────────────┐
                │  initial_state(country)│  (القسم C)
                └────────────┬───────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │  get_country_baseline()    │  (القسم B — تخزين مؤقت)
                └────────────┬───────────────┘
                             │ (أول مرة فقط)
                             ▼
                ┌─────────────────────────────────┐
                │  fetch_world_bank_baseline()    │  (القسم B — HTTP حي)
                │  fetch_world_bank_sectors()     │
                └─────────────────────────────────┘

         ┌──── حلقة 20 سنة ────┐
         │                      │
         ▼                      │
   step_year() ─── ai_adoption() │  (القسم C)
         │                      │
         ▼                      │
   skill_breakdown()            │  (القسم D)
   sector_breakdown()           │  (القسم D)
   wages_by_skill()             │  (القسم D)
   gini_index(wages, skills)    │  (القسم D)
         │                      │
         ▼                      │
   إضافة لقوائم النتائج         │
         │                      │
         └───────── i += 1 ─────┘

   بعد الحلقة:
   ──────────
   summarize(results)   (القسم G)
   report(results)      (القسم G)
         │
         ▼
   إعادة JSON للـ API

   الفروع الجانبية:
   ──────────────
   compare_scenarios()   → 3× run_scenario()        (القسم E)
   monte_carlo()         → 1000× حلقات step_year()  (القسم E)
   sensitivity()         → 5× run_scenario()        (القسم E)
   validate()            → جلب + حلقة مخصّصة       (القسم F)
```

---

## ما الذي تغيّر عن `simulation.py` الأصلية

| الجانب | الأصلية | المنظّفة |
|---|---|---|
| إجمالي الأسطر | 562 | 481 (−14%) |
| أسطر الكود | ~430 | 318 (−26%) |
| الدوال | 35+ | 20 (−43%) |
| الدوال الميتة | 9 | 0 |
| التحديث السنوي | 7 دوال منفصلة | 1 (`step_year`) |
| تحديث القطاع | 4 دوال منفصلة | 1 (`sector_breakdown`) |
| القيم الأساسية | مُرمَّزة (150M وظيفة — لعبة) | حيّة من البنك الدولي، مليارات حقيقية |
| دعم الدول | لا (العالم دائماً) | نعم (أي رمز بنك دولي) |
| انقسامات القطاعات | نسب مُرمَّزة | حيّة لكل دولة من البنك الدولي |
| مستويات الأجور | مُعيَّنة من المؤلف | مُعايَرة لـ BLS OEWS مايو 2024 |
| منطق الحساسية | محاكاة مُدمجة صغيرة، كود ميت | إعادة استخدام نظيفة لـ `run_scenario` عبر `override_rate` |
| موقع الثوابت | مُبعثر داخل الدوال | الكل في الأعلى في قسم `CONSTANTS` |
| تنسيق `SKILLS` / `SECTORS` | قواميس منفصلة متعددة | قاموس واحد لكل مفهوم، مُحزَّم بـ tuple |

---

## أنماط Python الشائعة المستخدمة في هذا الملف

### النمط 1: تعبير قاموس لتحويل قاموس

```python
{tier: SKILLS[tier][1] * (1 + SKILLS[tier][3] * adoption) for tier in SKILLS}
```

**تستخدمه:** `wages_by_skill`، `skill_breakdown`، `compare_scenarios`.

### النمط 2: الاحتياط بـ `or`

```python
employment or float(INITIAL_JOBS)
```

يُعيد أول قيمة صحيحة. إذا كان `employment` هو None/0، يستخدم الاحتياط. **تستخدمه:** `fetch_world_bank_baseline`، `report`.

### النمط 3: معامل تجاوز اختياري

```python
def run_scenario(..., override_rate: Optional[float] = None):
    auto_rate = override_rate if override_rate is not None else SCENARIO_RATES[scenario]
```

يسمح للمستدعين بضبط مدخل واحد دون تكرار جسم الدالة. **تستخدمه:** `run_scenario`، تُوظّفه `sensitivity`.

### النمط 4: Try / Except بتراجع صامت

```python
try:
    data = fetch_live()
except Exception:
    data = fetch_synthetic()
```

**تستخدمه:** `_wb_latest`، `fetch_world_bank_unemployment`. حيوي للمرونة.

### النمط 5: ثوابت مُحزَّمة بـ tuple

```python
SKILLS = {"L1_basic": (share, wage, risk, pressure), ...}
SKILLS[tier][0]   # الحصة
SKILLS[tier][1]   # الأجر
```

يضغط 4 قواميس منفصلة في قاموس واحد. **تستخدمه:** `SKILLS`، `SECTORS`.

### النمط 6: فكّ التعبئة من tuple في حلقات for

```python
for sec, (_, sector_auto, growth, _r) in SECTORS.items():
```

يفكّ المفتاح وقيمة الـ tuple في سطر واحد. **تستخدمه:** `sector_breakdown`.

### النمط 7: التخزين المؤقت الكسول

```python
if key in _CACHE:
    return _CACHE[key]
_CACHE[key] = compute()
return _CACHE[key]
```

**تستخدمه:** `get_country_baseline`. يمنع إعادة جلب البيانات المكلفة.

### النمط 8: تجميع محاور NumPy

```python
np.mean(matrix, axis=0)
np.percentile(matrix, 2.5, axis=0)
```

`axis=0` = "احسب لأسفل كل عمود." يحوّل مصفوفة 1000×20 لمصفوفة من 20 عنصراً لإحصاءات كل سنة. **تستخدمه:** `monte_carlo`.

### النمط 9: تداخل f-string

```python
f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
f"sector_{sec}"
```

**تستخدمه:** كل بناء URL للـ API، تسمية أعمدة CSV.

---

## قاموس كل الرموز

جدول بحث سريع لأي شيء غريب تصادفه:

| الرمز | أين تراه | ما يعنيه |
|---|---|---|
| `:` | بعد اسم الدالة، بعد `if`/`for`/`def` | "ابدأ كتلة كود" |
| `->` | بعد معاملات الدالة | "تُعيد هذا النوع" |
| `=` | في أي مكان | التعيين (ليس المساواة!) |
| `==` | في الشروط | اختبار المساواة |
| `!=` | في الشروط | غير متساوٍ |
| `+`  `-`  `*`  `/` | رياضيات | جمع / طرح / ضرب / قسمة |
| `//` | رياضيات | قسمة صحيحة (تتجاهل الكسر) |
| `**` | رياضيات، استدعاءات دوال | الأس أو "افكّ القاموس كـ kwargs" |
| `*=`, `+=`, `-=` | عبارات | تعديل في المكان |
| `[]` | حول القيم | قائمة (أو فهرس: `arr[0]`) |
| `{}` | حول القيم | قاموس (إذا `key: value`) أو مجموعة |
| `()` | حول القيم | tuple أو استدعاء دالة |
| `_` في الأرقام | `3_400_000_000` | فاصل للتنسيق |
| `_` كمتغير | `for _ in ...` | "لا أهتم" |
| `_` في بداية الاسم | `_wb_latest`, `_BASELINE_CACHE` | تقليد: خاص |
| `f"..."` | نص حرفي | f-string (تُدمج `{المتغيرات}`) |
| `"""..."""` | نص حرفي | نص متعدد الأسطر / وثيقة |
| `lambda x: x[0]` | داخل استدعاءات دوال | دالة مجهولة من سطر واحد |
| `is None` | في الشروط | تحقق من قيمة None |
| `in` | شروط / حلقات for | العضوية / التكرار |
| `not` | في الشروط | NOT منطقي |
| `and` / `or` | في الشروط | AND / OR منطقي |
| `None` / `True` / `False` | في أي مكان | القيم الثلاث الخاصة |
| `return` | داخل دالة | إعادة قيمة |
| `pass` | داخل كتلة | "لا تفعل شيئاً" (عنصر نائب) |
| `Optional[X]` | تلميحات النوع | "يمكن أن يكون X أو None" |
| `Dict[K, V]` | تلميحات النوع | "قاموس بمفاتيح K وقيم V" |
| `Any` | تلميحات النوع | "أي شيء مقبول" |

---

## ملاحظات ختامية

### توزيع عدد الأسطر

| الفئة | الأسطر |
|---|---|
| الإجمالي | **481** |
| الأسطر الفارغة | 79 |
| تعليقات الهاش (`#`) | 52 |
| أسطر الوثائق | 36 |
| **كود قابل للتنفيذ الصافي** | **318** |

الملف تقريباً **66% كود، 18% تعليقات، 16% مسافات بيضاء** — نسبة صحية لكود مقروء.

### ما قرأته للتو

- كل دالة في `simulation.py` المنظّفة مشروحة سطراً بسطر
- كل كلمة مفتاحية Python ومعامل ونمط مشروحة
- أمثلة عددية عملية لكل حساب مهم
- مخطط الروابط يُظهر تدفق البيانات بين الأقسام
- قاموس كل رمز قد تصادفه
- جدول مقارنة مع النسخة الأصلية من 562 سطراً

### ترتيب القراءة الموصى به

إذا أردت **فهم النموذج بأسرع وقت**:
1. اقرأ القسم A (الثوابت) — 5 دقائق، يعطيك كل الأرقام السحرية
2. اقرأ القسم C → `step_year` — 5 دقائق، هذا محرّك كل سنة
3. اقرأ القسم E → `run_scenario` — 5 دقائق، هذه الحلقة الرئيسية
4. تصفّح القسم D للتفاصيل
5. تصفّح القسم B لجلب البيانات الحيّة
6. اقرأ القسمين F و G أخيراً (التحقق والمخرجات)

إذا أردت **توسيع النموذج**، نقاط الدخول الأسهل هي:
- إضافة قطاع جديد → عدّل ثابت `SECTORS` + أضف لمنطق التأثير التسرّبي في `sector_breakdown`
- إضافة مستوى مهاري جديد → عدّل ثابت `SKILLS`
- إضافة سيناريو جديد → أضف مدخلاً في `SCENARIO_RATES`
- إضافة دولة جديدة → لا تغيير في الكود مطلوب، فقط مرّر رمز البنك الدولي

نهاية الوثيقة.
