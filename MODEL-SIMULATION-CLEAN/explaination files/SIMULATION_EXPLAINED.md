# `simulation.py` — The Complete Line-by-Line Walkthrough (Clean Edition)

> A monkey-level explanation of the 481-line simulation engine.
> No prior Python knowledge required. Every keyword, every operator, every
> function explained with worked examples.
>
> This is the **CLEAN-rebuild** version — fewer functions (20 vs 35), real
> data from the World Bank, BLS-calibrated wages, and per-country support.

---

## Table of Contents

- [Part 0 — Python Basics You Need First](#part-0--python-basics-you-need-first)
- [Part 1 — File Anatomy](#part-1--file-anatomy)
- [Part 2 — Imports & File Header (lines 1-16)](#part-2--imports--file-header-lines-1-16)
- [SECTION A — CONSTANTS (lines 19-68)](#section-a--constants-lines-19-68)
- [SECTION B — LIVE DATA: World Bank Fetchers (lines 71-151)](#section-b--live-data-world-bank-fetchers-lines-71-151)
- [SECTION C — CORE MATH (lines 154-192)](#section-c--core-math-lines-154-192)
- [SECTION D — DERIVED BREAKDOWNS (lines 195-243)](#section-d--derived-breakdowns-lines-195-243)
- [SECTION E — SCENARIO RUNNER (lines 246-368)](#section-e--scenario-runner-lines-246-368)
- [SECTION F — HISTORICAL DATA + VALIDATION (lines 371-429)](#section-f--historical-data--validation-lines-371-429)
- [SECTION G — OUTPUTS (lines 432-481)](#section-g--outputs-lines-432-481)
- [Connections Between Sections](#connections-between-sections)
- [What Changed vs. the Original `simulation.py`](#what-changed-vs-the-original-simulationpy)
- [Common Python Patterns Used in This File](#common-python-patterns-used-in-this-file)
- [Glossary of Every Symbol](#glossary-of-every-symbol)

---

## Part 0 — Python Basics You Need First

Before you can read any line of code, you need to recognize these building blocks. Spend 5 minutes here and the rest of the file becomes readable.

### 0.1 Variables — Labels on boxes

```python
x = 5
name = "Tech"
```
**Read:** "Take the value on the right and put it in a box labeled with the name on the left."

The `=` sign is **assignment**, not equality (equality is `==`).

### 0.2 Numbers

```python
3_400_000_000   # integer (underscores are cosmetic)
105.0           # float (decimal)
0.05            # float
1e12            # scientific notation: 1 × 10¹² = 1,000,000,000,000
```

### 0.3 Strings

```python
"World"
'WLD'
f"hello {name}"   # f-string — embeds the variable's value
```

### 0.4 Lists, Dictionaries, Tuples

```python
[10, 20, 30]                       # list (ordered, mutable)
{"jobs": 150, "workforce": 160}    # dictionary (labeled box)
(0.20, 33_000, 0.75, -0.15)        # tuple (ordered, IMMUTABLE)
```

**Tuples** look like lists but use **round parentheses** and can't be modified after creation. The `SKILLS` constant uses tuples to pack 4 values per skill tier.

### 0.5 Functions

```python
def add_two(a: int, b: int) -> int:
    return a + b
```

- `def` starts a function.
- `(a, b)` are parameters.
- `-> int` says the return type (just documentation — Python doesn't enforce).
- `return` sends back a value.

### 0.6 Type Hints (just labels)

```python
def fetch(country: str = "WLD") -> Dict[str, Any]:
    ...
```

Reads: "takes a string named `country` with default `WLD`, returns a dictionary with string keys and any-type values." Python ignores these — they're documentation.

### 0.7 Math Operators

| Symbol | Meaning |
|---|---|
| `+`  `-`  `*`  `/` | add / subtract / multiply / divide |
| `//` | integer divide (drop decimal): `5//2 = 2` |
| `**` | power: `5**2 = 25` |
| `%`  | remainder: `5%2 = 1` |
| `+=` `-=` `*=` | in-place modify: `x += 5` is `x = x + 5` |
| `==` `!=` `<` `>` `<=` `>=` | comparisons |

### 0.8 Control Flow

```python
if x > 10:
    print("big")
elif x > 5:
    print("medium")
else:
    print("small")

# One-line ternary
result = "big" if x > 10 else "small"

# For loop
for item in [1, 2, 3]:
    print(item)

# Loop with both index and value
for i, value in enumerate(["a", "b", "c"]):
    print(i, value)

# Loop over dict (default = keys)
for k in {"x": 1, "y": 2}:
    print(k)
# Loop over dict items (key, value pairs)
for k, v in {"x": 1, "y": 2}.items():
    print(k, v)

# range(n) produces 0, 1, ..., n-1
for i in range(5):
    print(i)
```

### 0.9 Comprehensions (compact loops)

```python
# Dict comprehension
{k: v * 2 for k, v in {"a": 1, "b": 2}.items()}     # {"a": 2, "b": 4}

# List comprehension
[x * x for x in range(5)]                            # [0, 1, 4, 9, 16]

# Generator expression (no brackets, lazy)
sum(x * 2 for x in [1, 2, 3])                        # 12
```

### 0.10 Try / Except — Graceful failure

```python
try:
    risky_thing()
except Exception:
    fallback()
```

Used for any external call (HTTP, file I/O) that might fail.

### 0.11 None, True, False

```python
True       # boolean: yes
False      # boolean: no
None       # the "nothing" value
x is None  # check if x is None (not x == None)
```

### 0.12 Special Tokens You'll See

| Token | Meaning |
|---|---|
| `_` in numbers | `3_400_000_000` — cosmetic separator |
| `_` as variable | `for _ in ...` — "I don't care about this value" |
| Leading `_` in name | `_wb_latest` — convention: "private, internal use" |
| `f"..."` | f-string (interpolates `{variables}`) |
| `"""..."""` | multi-line string / docstring |
| `# comment` | comment, ignored by Python |
| `Optional[X]` | type hint: could be X or could be None |
| `Dict[str, Any]` | type hint: dictionary with string keys, any values |

---

## Part 1 — File Anatomy

The file `backend/simulation.py` is **481 lines** organized into 7 sections:

| Lines | Section | Functions |
|---|---|---|
| 1-16 | Module docstring + imports | — |
| 19-68 | **A: Constants** | (none — just data) |
| 71-151 | **B: Live Data** (World Bank fetchers) | 4 |
| 154-192 | **C: Core Math** | 3 |
| 195-243 | **D: Derived Breakdowns** | 4 |
| 246-368 | **E: Scenario Runner** | 4 |
| 371-429 | **F: Historical Data + Validation** | 2 |
| 432-481 | **G: Outputs** | 3 |

**20 functions total** (vs 35+ in the original). The reduction comes from:
- Removing 9 dead functions (`apply_automation_by_skill`, `skill_upgrade_rate`, etc.)
- Consolidating 7 tiny macro-update functions into one `step_year`
- Consolidating 4 sector-mutation functions into one `sector_breakdown`

**Architecture style:** Pure procedural code. No classes. Every function takes inputs, transforms them, and returns outputs. Easy to test, easy to read top-to-bottom.

**Mental model:** Think of the file as a 7-station factory:
1. Constants set up the recipes
2. Live Data fetchers grab the real starting ingredients
3. Core Math advances the world by one year
4. Derived Breakdowns slice the world into skills/sectors/wages
5. Scenario Runner is the master loop that runs everything for 20 years
6. Validation backtests the recipe against history
7. Outputs package the results for the API

---

## Part 2 — Imports & File Header (lines 1-16)

```python
1   """
2   AI Labor Market Simulation Engine.
3
4   Runs a year-by-year projection of jobs, GDP, wages, skills, sectors,
5   and inequality under three AI-adoption scenarios (slow / moderate / rapid).
6
7   The yearly loop in `run_scenario` calls `step_year` (macro update),
8   `skill_breakdown`, `sector_breakdown`, `wages_by_skill`, and `gini_index`
9   in sequence — read top-to-bottom to follow how each year evolves.
10  """
```

**Lines 1-10:** **Module docstring**. Triple-quoted string at the top of a file describes what the file is for. Python ignores it; tools and humans read it. Notice it explicitly tells the reader the *reading order* — that's intentional (the file IS the documentation).

```python
11  from __future__ import annotations
```

**Line 11:** Makes type hints lazy — they become plain strings instead of being evaluated at runtime. Lets you reference types that aren't defined yet, and slightly improves startup time. Modern Python boilerplate.

```python
13  import numpy as np
14  import pandas as pd
15  import requests
16  from typing import Any, Dict, Optional
```

**Lines 13-16:** Imports.
- `numpy as np` — fast math (means, percentiles, exp, arrays)
- `pandas as pd` — CSV export only (one use, line 480)
- `requests` — HTTP calls to the World Bank API
- `Any, Dict, Optional` — type-hint vocabulary

---

## SECTION A — CONSTANTS (lines 19-68)

This block defines every "magic number" the simulation uses, all in one place. No code, just data. The cleanup goal: **a reader should be able to tweak any parameter without hunting through the file**.

### Baseline scalars (lines 23-34)

```python
23  BASE_YEAR          = 2026
24  # Fallback baselines (used only if the World Bank API is unreachable).
25  # Defaults are WORLD aggregates calibrated to ~2024 real figures:
26  #   Total employment   ≈ 3.4 B   (was a scaled-down 150 M in v1)
27  #   Labor force        ≈ 3.6 B
28  #   GDP (current US$)  ≈ 105 T
29  INITIAL_JOBS       = 3_400_000_000
30  INITIAL_WORKFORCE  = 3_600_000_000
31  INITIAL_GDP        = 105.0          # trillion USD
32  INITIAL_ADOPTION   = 0.05
33  WORKFORCE_GROWTH   = 0.008           # 0.8 % annual (UN)
34  JOB_CREATION_RATIO = 0.60            # new jobs per displaced job (model assumption)
```

| Constant | Value | Meaning |
|---|---|---|
| `BASE_YEAR` | 2026 | Year 0 of the projection |
| `INITIAL_JOBS` | 3.4 B | Fallback if World Bank API down |
| `INITIAL_WORKFORCE` | 3.6 B | Fallback |
| `INITIAL_GDP` | 105 T | Fallback (trillion USD) |
| `INITIAL_ADOPTION` | 0.05 | Starting AI adoption (5%) |
| `WORKFORCE_GROWTH` | 0.008 | 0.8% per year (matches UN projections) |
| `JOB_CREATION_RATIO` | 0.60 | For every $1 of jobs destroyed, AI creates $0.60 of new ones |

**Key difference from the original:** the fallbacks are now **real-world scale** (billions). The old code used 150M jobs — a toy scaled-down number. If the World Bank API is down, this code still produces realistic outputs.

### `SCENARIO_RATES` (line 36)

```python
36  SCENARIO_RATES = {"slow": 0.03, "moderate": 0.05, "rapid": 0.08}
```

The three scenario knobs. `moderate=5%` means 5% of jobs get automated each year (modulated by AI adoption level).

### `SKILLS` dictionary (lines 38-53) ⭐

```python
38  # Skill tiers — (share_of_workforce, base_wage_usd, ai_risk, wage_pressure).
39  # Wages calibrated to BLS OEWS May 2024 national mean annual wages for
40  # representative occupations per tier:
41  #   L1_basic         food prep / cashiers / janitors        ≈ $33 K
42  #   L2_semi          machine operators / truck drivers     ≈ $49 K
43  #   L3_intermediate  admin assistants / nurses             ≈ $73 K
44  #   L4_advanced      engineers / general managers          ≈ $115 K
45  #   L5_expert        executives / lawyers / surgeons       ≈ $200 K
46  # Source: https://www.bls.gov/oes/  (downloadable OEWS national XLSX).
47  SKILLS: Dict[str, tuple] = {
48      "L1_basic":        (0.20,  33_000, 0.75, -0.15),
49      "L2_semi":         (0.30,  49_000, 0.55, -0.08),
50      "L3_intermediate": (0.25,  73_000, 0.35,  0.02),
51      "L4_advanced":     (0.15, 115_000, 0.15,  0.12),
52      "L5_expert":       (0.10, 200_000, 0.05,  0.22),
53  }
```

Each tier maps to a **tuple of 4 numbers** in this order:

| Position | Name | Meaning |
|---|---|---|
| 0 | `share` | Fraction of workforce in this tier |
| 1 | `base_wage` | Starting annual wage (USD) |
| 2 | `ai_risk` | Probability AI displaces a worker at this tier |
| 3 | `wage_pressure` | Wage change at full AI adoption (negative = pay cut) |

**How to read** `("L1_basic", (0.20, 33_000, 0.75, -0.15))`:
> 20% of workers are L1_basic. They earn $33K/yr. 75% of L1 jobs are at risk. At full AI adoption their wages drop 15%.

The `[0]`, `[1]`, `[2]`, `[3]` indexing pattern is used everywhere these constants are read.

### `SECTORS` dictionary (lines 55-64)

```python
55  # Sector splits — (share_of_jobs, automation_rate, growth_rate, _reserved).
59  SECTORS: Dict[str, tuple] = {
60      "Tech":          (0.10, 0.04, 0.06, 0.0),
61      "Manufacturing": (0.22, 0.08, 0.01, 0.0),
62      "Healthcare":    (0.13, 0.02, 0.04, 0.0),
63      "Services":      (0.55, 0.06, 0.02, 0.0),
64  }
```

Same tuple-packing trick. The `0.0` slot is reserved for future use (e.g., per-sector wage premiums).

| Sector | Share | Automation Rate | Growth |
|---|---|---|---|
| Tech | 10% | 4% (low — they MAKE AI) | 6% (highest) |
| Manufacturing | 22% | 8% (highest — robots) | 1% (lowest) |
| Healthcare | 13% | 2% (lowest — human touch) | 4% |
| Services | 55% | 6% | 2% |

**These shares are FALLBACKS only.** When the World Bank API works, `fetch_world_bank_sectors` overrides them with real per-country data.

### `_BASELINE_CACHE` (line 68)

```python
66  # Per-country baseline cache: {country_code: {jobs, workforce, gdp, sectors}}.
67  # Filled lazily on first request — see `get_country_baseline`.
68  _BASELINE_CACHE: Dict[str, Dict[str, Any]] = {}
```

**Empty dictionary** used as a memory-only cache. The leading underscore signals "private — don't touch from outside this file." When you call `get_country_baseline("USA")` the first time, it fetches from World Bank and stores the result here. Second call returns instantly.

This prevents hitting the World Bank API on every single simulation request.

---

## SECTION B — LIVE DATA: World Bank Fetchers (lines 71-151)

This is the **biggest addition vs. the original**. Four functions that pull real-world data on demand.

### Function 1: `_wb_latest()` (lines 75-87)

```python
75  def _wb_latest(indicator: str, country: str = "WLD") -> Optional[float]:
76      """Return the most-recent non-null value for a World Bank indicator."""
77      url = f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
78      try:
79          resp = requests.get(url, params={"format": "json", "per_page": 20}, timeout=8)
80          resp.raise_for_status()
81          payload = resp.json()
82          for row in payload[1]:
83              if row.get("value") is not None:
84                  return float(row["value"])
85      except Exception:
86          return None
87      return None
```

#### Line-by-line

- **Line 75:** Leading `_` = "private helper, don't import from outside." Takes an indicator code (like `"SL.EMP.TOTL"`) and a country code (default `"WLD"` = whole world). Returns either a number OR `None` (`Optional[float]` says so).
- **Line 77:** Builds the URL. World Bank format: `https://api.worldbank.org/v2/country/USA/indicator/SL.EMP.TOTL`.
- **Line 78:** Start protected block.
- **Line 79:** Send HTTP GET. Wait at most 8 seconds. Ask for JSON, up to 20 rows.
- **Line 80:** Raise an error if HTTP status was 4xx or 5xx.
- **Line 81:** Parse JSON. World Bank returns `[metadata, data_array]`.
- **Lines 82-84:** Walk the data rows in order (newest first). Return the **first non-null** value as a float.
- **Lines 85-86:** Any exception (network, JSON, missing key) → return `None`.
- **Line 87:** If we got through everything without finding a value → also `None`.

**Why this design:** World Bank sometimes has gaps (most recent year might be null). This function skips nulls and grabs the latest actual number.

#### Worked example

`_wb_latest("NY.GDP.MKTP.CD", "USA")` → asks for USA GDP, gets back `~28.75e12` (real 2023 value).

`_wb_latest("INVALID", "USA")` → no data, returns `None`.

### Function 2: `fetch_world_bank_baseline()` (lines 90-112)

```python
90  def fetch_world_bank_baseline(country: str = "WLD") -> Dict[str, Any]:
91      """Total employment, labor force, and GDP for a country (latest year).
92
93      `SL.EMP.TOTL` is only published for the WLD aggregate. For individual
94      countries we derive employment = labor_force × (1 − unemployment_rate/100).
95      """
96      employment  = _wb_latest("SL.EMP.TOTL",    country)
97      labor_force = _wb_latest("SL.TLF.TOTL.IN", country)
98      gdp_usd     = _wb_latest("NY.GDP.MKTP.CD", country)
99      unem_pct    = _wb_latest("SL.UEM.TOTL.ZS", country)
100
101     if employment is None and labor_force is not None and unem_pct is not None:
102         employment = labor_force * (1.0 - unem_pct / 100.0)
103
104     live = bool(labor_force and gdp_usd and (employment or unem_pct))
105     return {
106         "country":      country,
107         "employment":   employment   or float(INITIAL_JOBS),
108         "labor_force":  labor_force  or float(INITIAL_WORKFORCE),
109         "gdp_trillion": (gdp_usd / 1e12) if gdp_usd else INITIAL_GDP,
110         "unemployment_pct": unem_pct,
111         "live":         live,
112     }
```

#### What it does

Fetches **4 World Bank indicators** for one country, then assembles a clean dict.

#### The clever bit (lines 101-102)

`SL.EMP.TOTL` (total employment count) is only published for the World aggregate. If you ask for USA, you get `None`. Workaround:

```python
employment = labor_force × (1 − unemployment_rate / 100)
```

So if labor force is 175M and unemployment is 4.2%, employment is `175M × 0.958 = 167.7M`. Mathematically equivalent — and both inputs ARE available per country.

#### Line 104 — the `live` flag

```python
live = bool(labor_force and gdp_usd and (employment or unem_pct))
```

Reads: "live is True if we got labor_force AND gdp AND at least one of (employment OR unemployment)." The `bool(...)` converts the result to True/False (otherwise Python's `and`/`or` returns the value itself).

#### Lines 107-109 — Fallback chain with `or`

```python
"employment":   employment   or float(INITIAL_JOBS),
```

Python's `or` returns the **first truthy value**. So if `employment` is `None` (falsy), it falls through to `INITIAL_JOBS`. If `employment` has a real number (truthy), that's used.

#### Worked example

`fetch_world_bank_baseline("USA")`:
```python
{
    "country":          "USA",
    "employment":       167_500_000.0,   # derived: 174.8M × (1 - 4.2%)
    "labor_force":      174_800_000.0,   # real
    "gdp_trillion":     28.75,           # real ($28.75T)
    "unemployment_pct": 4.2,             # real
    "live":             True,
}
```

### Function 3: `fetch_world_bank_sectors()` (lines 115-141)

```python
115 def fetch_world_bank_sectors(country: str = "WLD") -> Dict[str, float]:
116     """Sector shares mapped to {Tech, Manufacturing, Healthcare, Services}.
117
118     World Bank exposes 3 broad buckets — Agriculture / Industry / Services.
119     We map:
120         Manufacturing  ←  Industry
121         Services bucket → split into Tech / Healthcare / Services-other
122                           using fixed sub-ratios (Tech 18%, Healthcare 24%,
123                           Services 58%) since the WB doesn't break this out.
124         Agriculture    →  rolled into Services (since the project has no
125                           agriculture sector — kept at 4 categories).
126     """
127     agri = _wb_latest("SL.AGR.EMPL.ZS", country)
128     ind  = _wb_latest("SL.IND.EMPL.ZS", country)
129     srv  = _wb_latest("SL.SRV.EMPL.ZS", country)
130     if not all((agri, ind, srv)):
131         return {sec: SECTORS[sec][0] for sec in SECTORS}
132
133     agri, ind, srv = agri / 100.0, ind / 100.0, srv / 100.0
134     # Roll agriculture into the "Services" bucket then sub-split.
135     services_bucket = srv + agri
136     return {
137         "Tech":          round(services_bucket * 0.18, 4),
138         "Manufacturing": round(ind, 4),
139         "Healthcare":    round(services_bucket * 0.24, 4),
140         "Services":      round(services_bucket * 0.58, 4),
141     }
```

#### The 3→4 sector mapping

World Bank gives you **3 buckets** as percentages of employment:
- `SL.AGR.EMPL.ZS` — Agriculture
- `SL.IND.EMPL.ZS` — Industry (includes manufacturing, mining, utilities)
- `SL.SRV.EMPL.ZS` — Services (everything else)

We need **4 buckets** (Tech, Manufacturing, Healthcare, Services). The mapping:

```
Industry  ──► Manufacturing  (cleanest 1:1 map)
Services  ─┬► Tech         (× 18%)
           ├► Healthcare   (× 24%)
           └► Services     (× 58%)
Agriculture ──► rolled into Services bucket before splitting
```

The 18/24/58 sub-ratios are approximations of how the Services bucket actually breaks down in BLS data.

#### Line 130 — Defensive `all()`

```python
if not all((agri, ind, srv)):
    return {sec: SECTORS[sec][0] for sec in SECTORS}
```

`all((a, b, c))` returns `True` only if every item is truthy. If ANY indicator is `None`, fall back to the hardcoded `SECTORS` shares.

#### Line 133 — Multiple assignment

```python
agri, ind, srv = agri / 100.0, ind / 100.0, srv / 100.0
```

Reads: "divide all three by 100 and reassign in parallel." World Bank returns percentages (like `45.3`), we want fractions (`0.453`).

#### Worked example for USA

WB returns: Agri 1.4%, Industry 18.9%, Services 79.7%.
```
agri=0.014, ind=0.189, srv=0.797
services_bucket = 0.797 + 0.014 = 0.811
Tech         = 0.811 × 0.18 = 0.1460   (14.6%)
Manufacturing = 0.189                   (18.9%)
Healthcare   = 0.811 × 0.24 = 0.1946   (19.5%)
Services     = 0.811 × 0.58 = 0.4703   (47.0%)
                                  Sum = 100.1%  ✓
```

### Function 4: `get_country_baseline()` (lines 144-151) — the cache

```python
144 def get_country_baseline(country: str = "WLD") -> Dict[str, Any]:
145     """Cached per-country baseline (employment, workforce, gdp, sector shares)."""
146     if country in _BASELINE_CACHE:
147         return _BASELINE_CACHE[country]
148     base = fetch_world_bank_baseline(country)
149     base["sectors"] = fetch_world_bank_sectors(country)
150     _BASELINE_CACHE[country] = base
151     return base
```

**Standard cache pattern:**
1. Line 146: Check if we already have it → return immediately.
2. Lines 148-149: Fetch baseline + sectors (each makes 1-4 HTTP calls).
3. Line 150: Store in cache.
4. Line 151: Return.

**Net effect:** the World Bank API is hit at most **once per country**. After that, every simulation reuses the cached result.

---

## SECTION C — CORE MATH (lines 154-192)

Three functions. The heart of the per-year update.

### Function 5: `ai_adoption()` (lines 158-161) ⭐

```python
158 def ai_adoption(year_index: int, speed: float = 1.0) -> float:
159     """Logistic S-curve, midpoint at year 10, returns 0..1."""
160     k = 0.35 * speed
161     return 1.0 / (1.0 + np.exp(-k * (year_index - 10.0)))
```

The **logistic function** — used for every technology adoption curve in history (telephone, TV, internet, smartphones, EVs).

#### The math

```
                 1
adoption =  ─────────────────────────
            1 + e^(-k × (year − 10))
```

- At year 0: returns ~3% (early adopters)
- At year 10: returns exactly 50% (inflection)
- At year 20: returns ~97% (saturation)

#### The `speed` parameter

`speed=0.5` → flatter curve, slower adoption.
`speed=1.5` → steeper curve, explosive adoption.

This is how the 3 scenarios produce different futures. The two `_speed` arguments in `run_scenario` and `monte_carlo` both flow into here.

⚠ **Naming gotcha:** `k` here is a math letter for "steepness" — totally unrelated to the `k, v` in dict comprehensions elsewhere.

### Function 6: `initial_state()` (lines 164-172)

```python
164 def initial_state(country: str = "WLD") -> Dict[str, float]:
165     base = get_country_baseline(country)
166     return {
167         "total_jobs":   float(base["employment"]),
168         "workforce":    float(base["labor_force"]),
169         "ai_adoption":  INITIAL_ADOPTION,
170         "_gdp_base":    float(base["gdp_trillion"]),
171         "_country":     country,
172     }
```

**What changed vs original:** now takes a `country` parameter and pulls live values via `get_country_baseline`.

The leading underscore on `_gdp_base` and `_country` signals "internal state, not part of the public output." They're carried through the loop but not exported to the API.

#### Worked example

`initial_state("IND")` → `{total_jobs: 591.6M, workforce: 617.6M, ai_adoption: 0.05, _gdp_base: 3.91, _country: "IND"}`.

### Function 7: `step_year()` (lines 175-192) ⭐ THE PER-YEAR ENGINE

```python
175 def step_year(state: Dict[str, float], year_index: int,
176               auto_rate: float, speed: float) -> Dict[str, float]:
177     """Advance the macro state by one year. Mutates `state` in place."""
178     state["ai_adoption"] = ai_adoption(year_index, speed)
179     adoption = state["ai_adoption"]
180
181     jobs_lost    = state["total_jobs"] * auto_rate * adoption
182     jobs_created = state["total_jobs"] * auto_rate * adoption * JOB_CREATION_RATIO
183     state["total_jobs"] = max(0.0, state["total_jobs"] - jobs_lost + jobs_created)
184     state["workforce"] *= (1.0 + WORKFORCE_GROWTH)
185
186     gdp_base    = state.get("_gdp_base", INITIAL_GDP)
187     unem        = max(0.0, (state["workforce"] - state["total_jobs"]) / state["workforce"])
188     productivity= 1.0 + (adoption ** 0.7) * 0.85
189     gdp         = gdp_base * (1.0 + (productivity - 1.0) * 0.6 - unem * 0.4)
190     spending    = gdp * max(0.30, 0.68 - unem * 1.2)
191
192     return {"unem": unem, "productivity": productivity, "gdp": gdp, "spending": spending}
```

This **single function replaces 7 functions** from the original codebase (update_jobs, update_workforce, calculate_unemployment, new_ai_jobs_created, productivity_multiplier, calculate_gdp_impact, consumer_spending_impact).

#### Step-by-step

| Line | What |
|---|---|
| 178-179 | Update AI adoption from the S-curve, copy to short variable |
| 181 | Jobs lost = (current jobs) × (scenario rate) × (current AI adoption) |
| 182 | Jobs created = same formula × 0.60 ratio |
| 183 | Net update: `max(0, ...)` floors at zero (can't have negative jobs) |
| 184 | Workforce grows 0.8% per year |
| 186 | Read the country's GDP baseline (or fall back) |
| 187 | Unemployment = (workforce − jobs) / workforce, floored at 0 |
| 188 | Productivity = 1 + adoption^0.7 × 0.85 (diminishing returns) |
| 189 | GDP = baseline × (1 + 0.6 × productivity_gain − 0.4 × unemployment_drag) |
| 190 | Spending = GDP × max(30%, 68% − unemployment × 1.2) |
| 192 | Return all 4 derived metrics in a tidy dict |

#### Mutation note

The function **mutates `state` in place** (modifies `state["ai_adoption"]`, `state["total_jobs"]`, `state["workforce"]` directly). The returned dict has the *derived* metrics only. This is a deliberate split: long-lived state stays in `state`, ephemeral metrics travel back to the caller.

#### Worked example (USA, year 0, moderate scenario)

```
Inputs:
  state["total_jobs"]  = 167,500,000
  state["workforce"]   = 174,800,000
  state["_gdp_base"]   = 28.75
  year_index = 0,  auto_rate = 0.05,  speed = 1.0

adoption       = ai_adoption(0, 1.0) ≈ 0.029
jobs_lost      = 167.5M × 0.05 × 0.029  ≈ 242,875
jobs_created   = 242,875 × 0.60         ≈ 145,725
new total_jobs = 167,500,000 - 242,875 + 145,725 ≈ 167,402,850
new workforce  = 174,800,000 × 1.008    ≈ 176,198,400
unem           = (176.2M − 167.4M) / 176.2M ≈ 0.0499 (5.0%)
productivity   = 1 + 0.029^0.7 × 0.85   ≈ 1.077
gdp            = 28.75 × (1 + 0.077×0.6 − 0.05×0.4) ≈ 28.91
spending       = 28.91 × (0.68 − 0.05×1.2) ≈ 28.91 × 0.62 ≈ 17.92
```

---

## SECTION D — DERIVED BREAKDOWNS (lines 195-243)

Four functions that produce the **per-year breakdowns** the dashboard charts read.

### Function 8: `skill_breakdown()` (lines 204-205)

```python
199 # NOTE: skill distribution is recomputed from fixed shares every year.
200 # The original codebase had a `skill_upgrade_rate` function that moved
201 # workers between tiers, but it was never wired into the main loop —
202 # the actual model has always treated the distribution as fixed. Keeping
203 # it that way intentionally for clarity.
204 def skill_breakdown(state: Dict[str, float]) -> Dict[str, int]:
205     return {tier: int(state["workforce"] * SKILLS[tier][0]) for tier in SKILLS}
```

A **5-line function with a 4-line comment** explaining a deliberate simplification.

The dict comprehension reads: "for each tier in SKILLS, multiply workforce by `SKILLS[tier][0]` (the share, which is the 1st element of the tuple), cast to int."

Result example: `{L1_basic: 35M, L2_semi: 52M, L3_intermediate: 44M, L4_advanced: 26M, L5_expert: 17M}` for a 174M workforce.

### Function 9: `wages_by_skill()` (lines 208-210)

```python
208 def wages_by_skill(adoption: float) -> Dict[str, float]:
209     return {tier: round(SKILLS[tier][1] * (1.0 + SKILLS[tier][3] * adoption), 0)
210             for tier in SKILLS}
```

Same comprehension pattern. For each tier:
- `SKILLS[tier][1]` = base wage (index 1)
- `SKILLS[tier][3]` = wage pressure (index 3)
- Final wage = `base × (1 + pressure × adoption)`

At full adoption (1.0):
- L1: $33K × 0.85 = $28K (15% pay cut)
- L5: $200K × 1.22 = $244K (22% raise)

**This is the inequality engine.** Low-skill wages compress, high-skill wages expand.

### Function 10: `sector_breakdown()` (lines 213-230)

```python
213 def sector_breakdown(state: Dict[str, float], auto_rate: float) -> Dict[str, int]:
214     adoption = state["ai_adoption"]
215     total    = state["total_jobs"]
216     country  = state.get("_country", "WLD")
217     shares   = get_country_baseline(country).get("sectors") or {sec: SECTORS[sec][0] for sec in SECTORS}
218     jobs = {sec: total * shares.get(sec, SECTORS[sec][0]) for sec in SECTORS}
219
220     # automation shrinkage + AI-driven growth (per-sector)
221     for sec, (_, sector_auto, growth, _r) in SECTORS.items():
222         jobs[sec] *= (1.0 - sector_auto * auto_rate * adoption)
223         jobs[sec] *= (1.0 + growth * adoption)
224
225     # Tech spillover: Tech success benefits Services + Healthcare, hurts Manufacturing.
226     spillover = jobs["Tech"] * 0.02 * adoption
227     jobs["Services"]      += spillover * 0.5
228     jobs["Manufacturing"] -= spillover * 0.3
229     jobs["Healthcare"]    += spillover * 0.1
230     return {sec: int(v) for sec, v in jobs.items()}
```

**This single function replaces 4 functions** from the original (distribute_by_sector, apply_sector_automation, calculate_sector_growth, sector_interaction).

#### Line-by-line

- **Lines 214-216:** Pull adoption, total jobs, and country code from state.
- **Line 217:** Get real sector shares from the cache. If missing (or `None`), fall back to `SECTORS[sec][0]`.
- **Line 218:** Apply shares to total: `{Tech: 167M × 0.146, Manufacturing: 167M × 0.189, ...}`.

#### Tuple unpacking in the for loop (line 221)

```python
for sec, (_, sector_auto, growth, _r) in SECTORS.items():
```

This is **dense Python.** Each item in `SECTORS.items()` is a `(key, value)` pair where value is a 4-tuple. We unpack:
- `sec` = the key (e.g. `"Tech"`)
- `(_, sector_auto, growth, _r)` = the 4-tuple, ignoring positions 0 and 3 with `_`

Equivalent expanded form:
```python
for sec in SECTORS:
    _, sector_auto, growth, _r = SECTORS[sec]
```

Lines 222-223 apply both automation shrinkage AND AI growth multiplicatively.

#### Spillover (lines 226-229)

```python
spillover = jobs["Tech"] × 0.02 × adoption
```

A small amount of Tech jobs "spill" into adjacent sectors. The 50%/-30%/10% split says: half of Tech's halo goes to Services, 30% siphons from Manufacturing, 10% goes to Healthcare.

#### Worked example

Tech has 16.4M jobs after automation+growth, adoption is 0.5:
```
spillover = 16,400,000 × 0.02 × 0.5 = 164,000
Services      += 164,000 × 0.5 =  +82,000
Manufacturing -= 164,000 × 0.3 =  -49,200
Healthcare    += 164,000 × 0.1 =  +16,400
```

### Function 11: `gini_index()` (lines 233-243)

```python
233 def gini_index(wages: Dict[str, float], skills: Dict[str, int]) -> float:
234     """Gini coefficient (0=equal, ~1=maximally unequal)."""
235     incomes = []
236     for tier, wage in wages.items():
237         count = max(1, skills.get(tier, 1) // 10_000_000)
238     incomes.extend([wage] * count)
239     if not incomes:
240         return 0.0
241     arr = np.array(sorted(incomes), dtype=float)
242     n   = arr.size
243     return float((2 * np.sum(np.arange(1, n + 1) * arr) / (n * arr.sum())) - (n + 1) / n)
```

#### The clever optimization (line 237)

```python
count = max(1, skills.get(tier, 1) // 10_000_000)
```

Naive approach: one income entry per worker → billions of items, slow Gini math.

This approach: **one sample per 10 million workers**, minimum 1. So 35M L1 workers become 3 samples. Total list size: 15-20 items, microseconds to process.

**Why this works:** Gini measures distribution *shape*, not absolute magnitudes. Proportions are preserved.

#### Line 243 — Standard Gini formula

```
        2 × Σ(i × y_i)       n+1
G = ──────────────────── − ───────
        n × Σy              n
```

NumPy details:
- `np.arange(1, n+1)` = `[1, 2, 3, ..., n]` as an array
- `* arr` = element-wise multiply
- `np.sum(...)` = sum all
- `arr.sum()` = same thing, method form

Output is between 0 (perfect equality) and ~1 (maximum inequality).

---

## SECTION E — SCENARIO RUNNER (lines 246-368)

Four functions that drive the simulation.

### Function 12: `run_scenario()` (lines 250-299) ⭐ THE MASTER FUNCTION

```python
250 def run_scenario(scenario: str = "moderate", horizon: int = 20,
251                  adoption_speed: float = 1.0,
252                  override_rate: Optional[float] = None,
253                  country: str = "WLD") -> Dict[str, Any]:
254     """Run a full N-year simulation and return a JSON-ready results dict."""
255     auto_rate = override_rate if override_rate is not None else SCENARIO_RATES.get(scenario, 0.05)
256     state = initial_state(country)
257
258     results: Dict[str, Any] = {
259         "scenario":         scenario,
260         "country":          country,
261         "automation_rate":  auto_rate,
262         "years":            [],
263         "unemployment":     [],
264         "gdp":              [],
265         "total_jobs":       [],
266         "ai_adoption":      [],
267         "gini":             [],
268         "productivity":     [],
269         "consumer_spending":[],
270         "skills":  {tier: [] for tier in SKILLS},
271         "wages":   {tier: [] for tier in SKILLS},
272         "sectors": {sec:  [] for sec  in SECTORS},
273     }
274
275     for i in range(horizon):
276         step    = step_year(state, i, auto_rate, adoption_speed)
277         skills  = skill_breakdown(state)
278         sectors = sector_breakdown(state, auto_rate)
279         wages   = wages_by_skill(state["ai_adoption"])
280         gini    = gini_index(wages, skills)
281
282         results["years"].append(BASE_YEAR + i)
283         results["unemployment"].append(round(step["unem"] * 100, 2))
284         results["gdp"].append(round(step["gdp"], 3))
285         results["total_jobs"].append(int(state["total_jobs"]))
286         results["ai_adoption"].append(round(state["ai_adoption"] * 100, 2))
287         results["gini"].append(round(gini, 4))
288         results["productivity"].append(round(step["productivity"], 4))
289         results["consumer_spending"].append(round(step["spending"], 3))
290
291         for tier in SKILLS:
292             results["skills"][tier].append(skills[tier])
293             results["wages"][tier].append(wages[tier])
294         for sec in SECTORS:
295             results["sectors"][sec].append(sectors[sec])
296
297     results["summary"] = summarize(results)
298     results["report"]  = report(results)
299     return results
```

The **single function called by the `/api/simulate/{scenario}` endpoint**.

#### Five parameters

- `scenario` — `"slow"`, `"moderate"`, `"rapid"` (default moderate)
- `horizon` — number of years to project (default 20)
- `adoption_speed` — multiplier for the S-curve steepness (default 1.0)
- `override_rate` — optional escape hatch used by `sensitivity()` to test ±20% perturbations
- `country` — World Bank country code (default `"WLD"` = world)

#### Line 255 — Override pattern

```python
auto_rate = override_rate if override_rate is not None else SCENARIO_RATES.get(scenario, 0.05)
```

Reads: "if caller gave an explicit rate, use it; otherwise look up the scenario; if scenario is unknown, default to 5%."

This is what makes `sensitivity()` clean — it can call `run_scenario(..., override_rate=0.06)` without having to define a new function.

#### Lines 258-273 — Pre-allocated result containers

Empty lists/dicts to fill as the loop runs. Pre-allocating with comprehensions like `{tier: [] for tier in SKILLS}` guarantees every expected key exists from the start.

#### The yearly loop (lines 275-295)

```python
for i in range(horizon):
    step    = step_year(state, i, auto_rate, adoption_speed)
    skills  = skill_breakdown(state)
    sectors = sector_breakdown(state, auto_rate)
    wages   = wages_by_skill(state["ai_adoption"])
    gini    = gini_index(wages, skills)
    ...
```

**The order matters:**
1. `step_year` mutates `state` (advances jobs, workforce, adoption).
2. `skill_breakdown` reads the new workforce.
3. `sector_breakdown` reads the new jobs.
4. `wages_by_skill` reads the new adoption.
5. `gini_index` reads the just-computed wages + skills.

Then everything gets appended to the result arrays. After 20 iterations every list has 20 values.

#### Lines 297-298 — Attach summary + report

```python
results["summary"] = summarize(results)
results["report"]  = report(results)
```

These are post-loop computations (mean/std/min/max across all years, headline KPIs). They're attached so the API response is self-contained.

### Function 13: `compare_scenarios()` (lines 302-305)

```python
302 def compare_scenarios(horizon: int = 20, adoption_speed: float = 1.0,
303                        country: str = "WLD") -> Dict[str, Any]:
304     return {name: run_scenario(name, horizon, adoption_speed, country=country)
305             for name in SCENARIO_RATES}
```

A **3-line dict comprehension** that runs `run_scenario` once per scenario. Used by the Scenario Builder page — replaces three parallel HTTP calls with one.

Returns: `{"slow": {...}, "moderate": {...}, "rapid": {...}}`.

### Function 14: `monte_carlo()` (lines 308-339) ⭐

```python
308 def monte_carlo(n_simulations: int = 1000, horizon: int = 20) -> Dict[str, Any]:
309     """N random futures with parameter jitter — returns mean + 95% CI bands."""
310     rng = np.random.default_rng(42)
311     unem_matrix = np.zeros((n_simulations, horizon))
312     gdp_matrix  = np.zeros((n_simulations, horizon))
313
314     for sim in range(n_simulations):
315         auto_rate = rng.uniform(0.02, 0.10)
316         speed     = rng.uniform(0.60, 1.50)
317         state     = initial_state("WLD")
318         state["total_jobs"] *= rng.uniform(0.95, 1.05)
319         state["workforce"]  *= rng.uniform(0.95, 1.05)
320         for i in range(horizon):
321             step = step_year(state, i, auto_rate, speed)
322             unem_matrix[sim, i] = step["unem"] * 100
323             gdp_matrix[sim, i]  = step["gdp"]
324
325     years = list(range(BASE_YEAR, BASE_YEAR + horizon))
326     return {
327         "years":         years,
328         "n_simulations": n_simulations,
329         "unemployment": {
330             "mean":  np.mean(unem_matrix, axis=0).round(2).tolist(),
331             "lower": np.percentile(unem_matrix, 2.5,  axis=0).round(2).tolist(),
332             "upper": np.percentile(unem_matrix, 97.5, axis=0).round(2).tolist(),
333         },
334         "gdp": {
335             "mean":  np.mean(gdp_matrix, axis=0).round(3).tolist(),
336             "lower": np.percentile(gdp_matrix, 2.5,  axis=0).round(3).tolist(),
337             "upper": np.percentile(gdp_matrix, 97.5, axis=0).round(3).tolist(),
338         },
339     }
```

Run the simulation **1000 times with random inputs**, then compute mean + 95% confidence interval bands.

#### Line 310 — Seeded RNG

```python
rng = np.random.default_rng(42)
```

Seed 42 = reproducibility. Same seed → same random numbers → same output every time. Critical for debugging.

#### Lines 311-312 — Pre-allocated matrices

```python
unem_matrix = np.zeros((n_simulations, horizon))   # 1000 × 20 grid of zeros
```

`axis=0` later means "compute statistics down each column" (one value per year, across all sims).

#### Per-simulation randomization (lines 315-319)

- `auto_rate` ∈ uniform[0.02, 0.10] — anywhere from slow to ultra-rapid
- `speed` ∈ uniform[0.60, 1.50] — flat to steep S-curves
- Initial jobs/workforce jittered ±5% — uncertainty about starting state

#### Percentile bands (lines 331-332)

```python
"lower": np.percentile(unem_matrix, 2.5,  axis=0).round(2).tolist(),
"upper": np.percentile(unem_matrix, 97.5, axis=0).round(2).tolist(),
```

`2.5th percentile` = value below which only 2.5% of sims fall.
`97.5th percentile` = value above which only 2.5% of sims fall.

Together they form a **95% confidence interval** — the shaded band on the Validation page.

### Function 15: `sensitivity()` (lines 342-368)

```python
342 def sensitivity(scenario: str = "moderate", country: str = "WLD") -> Dict[str, Any]:
343     """±20% perturbation on each key parameter — impact on final-year unemployment."""
344     base = run_scenario(scenario, country=country)
345     base_unem = base["unemployment"][-1]
346     base_rate = SCENARIO_RATES[scenario]
347
348     high_rate  = run_scenario(scenario, override_rate=base_rate * 1.20, country=country)["unemployment"][-1]
349     low_rate   = run_scenario(scenario, override_rate=base_rate * 0.80, country=country)["unemployment"][-1]
350     high_speed = run_scenario(scenario, adoption_speed=1.20, country=country)["unemployment"][-1]
351     low_speed  = run_scenario(scenario, adoption_speed=0.80, country=country)["unemployment"][-1]
352
353     return {
354         "automation_rate": {
355             "base": round(base_unem, 2),
356             "high": round(high_rate, 2),
357             "low":  round(low_rate, 2),
358             "impact_high": round(high_rate - base_unem, 2),
359             "impact_low":  round(low_rate  - base_unem, 2),
360         },
361         "adoption_speed": { ... },
362     }
```

**Much cleaner than the original.** The trick: `run_scenario` now accepts `override_rate`, so we can perturb the automation rate without duplicating the loop logic. The original had an ugly inline mini-simulation for this; the new version is **5 clean function calls**.

#### What the output means

```python
{
  "automation_rate": {"base": 8.5, "low": 6.1, "high": 11.2, "impact_low": -2.4, "impact_high": +2.7},
  "adoption_speed":  {"base": 8.5, "low": 7.4, "high":  9.8, "impact_low": -1.1, "impact_high": +1.3},
}
```

Reading: "If automation_rate goes up 20%, final unemployment rises 2.7 percentage points." Tells policymakers which knobs matter most.

---

## SECTION F — HISTORICAL DATA + VALIDATION (lines 371-429)

Two functions to ground the simulation in past reality.

### Line 377-379 — `_SYNTHETIC_UNEM` (fallback array)

```python
377 _SYNTHETIC_UNEM = [6.5, 6.3, 5.8, 6.0, 5.5, 5.2, 5.8, 5.6, 5.4, 6.0,
378                    8.5, 7.8, 7.2, 6.8, 6.3, 5.9, 5.6, 5.3, 5.1, 5.0,
379                    8.9, 5.7, 5.4, 5.1, 4.9]
```

25 hand-crafted unemployment values that match the **real World Bank trend** — note the spikes:
- Index 10 (year 2010): **8.5%** = post-financial-crisis peak
- Index 20 (year 2020): **8.9%** = COVID-19 spike

Used only if the World Bank API is unreachable.

### Function 16: `fetch_world_bank_unemployment()` (lines 382-399)

```python
382 def fetch_world_bank_unemployment(start: int = 2000, end: int = 2020) -> Dict[str, list]:
383     """World Bank global unemployment (SL.UEM.TOTL.ZS). Falls back to synthetic on any failure."""
384     url = "https://api.worldbank.org/v2/country/WLD/indicator/SL.UEM.TOTL.ZS"
385     try:
386         resp = requests.get(url, params={"date": f"{start}:{end}", "format": "json", "per_page": 100}, timeout=10)
387         resp.raise_for_status()
388         payload = resp.json()
389         rows = sorted(
390             ((int(r["date"]), r["value"]) for r in payload[1] if r["value"] is not None),
391             key=lambda x: x[0],
392         )
393         if rows:
394             return {"years": [y for y, _ in rows], "values": [v for _, v in rows]}
394     except Exception:
395         pass
397     years  = list(range(start, end + 1))
398     values = _SYNTHETIC_UNEM[: len(years)]
399     return {"years": years, "values": values}
```

**Returns a dict, not a DataFrame** (one of the cleanups vs. the original). Much simpler downstream.

#### The clever line 389-392

```python
rows = sorted(
    ((int(r["date"]), r["value"]) for r in payload[1] if r["value"] is not None),
    key=lambda x: x[0],
)
```

Step by step:
1. **Generator expression** (parentheses, no brackets): yields `(year, value)` tuples for every non-null row.
2. `sorted(..., key=lambda x: x[0])` sorts by the first element (year).
3. Result: `[(2000, 6.5), (2001, 6.3), ...]` in ascending year order.

`lambda x: x[0]` is an **anonymous function** that returns its first argument's first element.

#### Lines 394 (renumbered) — Two list comprehensions over the same data

```python
return {"years": [y for y, _ in rows], "values": [v for _, v in rows]}
```

For each tuple in `rows`, unpack `(y, _)` and keep just `y`, then a separate list of just `v`. Splits one list of pairs into two parallel lists.

#### Line 398 — Slice

```python
values = _SYNTHETIC_UNEM[: len(years)]
```

`array[:n]` = "first n items." Trims the hardcoded array to the requested year range.

### Function 17: `validate()` (lines 402-429) — THE BACKTEST

```python
402 def validate(start: int = 2000, end: int = 2020) -> Dict[str, Any]:
403     """Backtest: run the model from `start` and compare against real unemployment."""
404     real = fetch_world_bank_unemployment(start, end)
405     actual = real["values"]
406     years  = real["years"]
407
408     state = {"total_jobs": 120_000_000.0, "workforce": 130_000_000.0, "ai_adoption": 0.01}
409     predicted = []
410     for i, _ in enumerate(years):
411         # Historical AI adoption was tiny — dampen the S-curve.
412         state["ai_adoption"] = ai_adoption(i, speed=0.8) * 0.5
413         adoption = state["ai_adoption"]
414         lost     = state["total_jobs"] * 0.05 * adoption
415         created  = lost * JOB_CREATION_RATIO
416         state["total_jobs"] = max(0.0, state["total_jobs"] - lost + created)
417         state["workforce"] *= (1.0 + WORKFORCE_GROWTH)
418         unem = max(0.0, (state["workforce"] - state["total_jobs"]) / state["workforce"]) * 100
419         predicted.append(round(unem, 2))
420
421     mae = float(np.mean(np.abs(np.array(actual, dtype=float) - np.array(predicted, dtype=float))))
422     return {
423         "years":     years,
424         "actual":    actual,
425         "predicted": predicted,
426         "mae":       round(mae, 4),
427         "accuracy":  round(max(0.0, 100.0 - mae * 10.0), 2),
428         "label":     f"Model Backtest {start}-{end}",
429     }
```

#### What this function proves

**The same engine that projects forward can recreate the past.** If MAE is low, you trust the projections more.

#### Line 408 — Different starting state

Year 2000 economy was smaller. Different starting jobs/workforce/adoption than 2026.

#### Line 412 — Dampened S-curve

```python
state["ai_adoption"] = ai_adoption(i, speed=0.8) * 0.5
```

AI adoption was tiny pre-2018. Multiplying by 0.5 keeps the historical adoption realistically low.

#### Line 421 — MAE computation

```python
mae = float(np.mean(np.abs(np.array(actual) - np.array(predicted))))
```

1. Convert lists to NumPy arrays
2. Subtract element-wise (gives a vector of errors)
3. `np.abs` → all positive
4. `np.mean` → average

If MAE = 0.5, predictions are off by 0.5% on average — excellent. If MAE = 5, model is poor.

#### Line 427 — Custom accuracy score

```python
"accuracy": round(max(0.0, 100.0 - mae * 10.0), 2),
```

Maps MAE to a friendly percentage:
- MAE 0 → 100% accuracy
- MAE 5 → 50%
- MAE 10+ → 0% (clamped)

Not a standard statistical metric, just an intuitive score for the dashboard.

---

## SECTION G — OUTPUTS (lines 432-481)

Three functions that package results for consumption.

### Function 18: `summarize()` (lines 436-447)

```python
436 def summarize(results: Dict[str, Any]) -> Dict[str, Any]:
437     summary = {}
438     for key in ("unemployment", "gdp", "ai_adoption", "gini", "productivity"):
439         arr = np.array(results.get(key, []), dtype=float)
440         if arr.size:
441             summary[key] = {
442                 "mean": round(float(np.mean(arr)), 4),
443                 "std":  round(float(np.std(arr)),  4),
444                 "min":  round(float(np.min(arr)),  4),
445                 "max":  round(float(np.max(arr)),  4),
446             }
447     return summary
```

For each of 5 metrics: compute mean, standard deviation, min, max.

#### Line 438 — Tuple iteration

```python
for key in ("unemployment", "gdp", ...):
```

Iterating a tuple is identical to iterating a list — but tuples are immutable, signaling "this list won't change."

#### Line 440 — `.size` guard

```python
if arr.size:
```

`arr.size` is the number of elements. `if 0:` is False; `if 5:` is True. Skips empty arrays to avoid mean-of-nothing errors.

### Function 19: `report()` (lines 450-463)

```python
450 def report(results: Dict[str, Any]) -> Dict[str, Any]:
451     years = results.get("years", [])
452     return {
453         "scenario":               results.get("scenario", "unknown"),
454         "automation_rate":        results.get("automation_rate", 0.05),
455         "horizon_years":          len(years),
456         "start_year":             years[0]  if years else BASE_YEAR,
457         "end_year":               years[-1] if years else BASE_YEAR + 19,
458         "final_unemployment_pct": results["unemployment"][-1] if results.get("unemployment") else 0,
459         "final_gdp_trillion":     results["gdp"][-1]          if results.get("gdp")          else 0,
460         "final_ai_adoption_pct":  results["ai_adoption"][-1]  if results.get("ai_adoption")  else 0,
461         "final_gini":             results["gini"][-1]         if results.get("gini")         else 0,
462         "peak_unemployment":      max(results["unemployment"]) if results.get("unemployment") else 0,
463     }
```

The headline dictionary. Feeds the KPI cards on the dashboard, plus the Arabic LLM advisor.

#### Defensive pattern (lines 456-462)

```python
years[0] if years else BASE_YEAR
```

`if years` is True when the list is non-empty. Protects against empty input.

#### `[-1]` everywhere

`list[-1]` = last element. The "final year" values come from this trick.

### Function 20: `export_csv()` (lines 466-481)

```python
466 def export_csv(results: Dict[str, Any], filepath: str = "simulation_output.csv") -> str:
467     rows = []
468     for i, year in enumerate(results["years"]):
469         row = {
470             "year":         year,
471             "unemployment": results["unemployment"][i],
472             "gdp":          results["gdp"][i],
473             "total_jobs":   results["total_jobs"][i],
474             "ai_adoption":  results["ai_adoption"][i],
475             "gini":         results["gini"][i],
476         }
477         for sec in results["sectors"]:
478             row[f"sector_{sec}"] = results["sectors"][sec][i]
479         rows.append(row)
480     pd.DataFrame(rows).to_csv(filepath, index=False)
481     return filepath
```

Build one dict per year. The f-string `f"sector_{sec}"` builds column names like `sector_Tech`, `sector_Manufacturing`, etc.

Line 480: pandas converts list-of-dicts to a table and writes CSV. `index=False` skips pandas's row numbers.

---

## Connections Between Sections

```
┌──────────────────────────────────────────────────────────────────────┐
│                         /api/simulate request                        │
└─────────────────────────────┬────────────────────────────────────────┘
                              ▼
                    ┌─────────────────────┐
                    │   run_scenario()    │  (Section E)
                    └─────────┬───────────┘
                              │
                              ▼
                ┌────────────────────────┐
                │  initial_state(country)│  (Section C)
                └────────────┬───────────┘
                             │
                             ▼
                ┌────────────────────────────┐
                │  get_country_baseline()    │  (Section B — CACHE)
                └────────────┬───────────────┘
                             │ (first time only)
                             ▼
                ┌─────────────────────────────────┐
                │  fetch_world_bank_baseline()    │  (Section B — LIVE HTTP)
                │  fetch_world_bank_sectors()     │
                └─────────────────────────────────┘

         ┌──── loop 20 years ────┐
         │                       │
         ▼                       │
   step_year() ─── ai_adoption() │  (Section C)
         │                       │
         ▼                       │
   skill_breakdown()             │  (Section D)
   sector_breakdown()            │  (Section D)
   wages_by_skill()              │  (Section D)
   gini_index(wages, skills)     │  (Section D)
         │                       │
         ▼                       │
   append to results lists       │
         │                       │
         └───────── i += 1 ──────┘

   After loop:
   ──────────
   summarize(results)   (Section G)
   report(results)      (Section G)
         │
         ▼
   Return JSON to API

   Side branches:
   ──────────────
   compare_scenarios()   → 3× run_scenario()        (Section E)
   monte_carlo()         → 1000× step_year() loops  (Section E)
   sensitivity()         → 5× run_scenario()        (Section E)
   validate()            → fetch + custom loop      (Section F)
```

---

## What Changed vs. the Original `simulation.py`

| Aspect | Original | Clean |
|---|---|---|
| Total lines | 562 | 481 (−14%) |
| Code lines | ~430 | 318 (−26%) |
| Functions | 35+ | 20 (−43%) |
| Dead functions | 9 | 0 |
| Per-year update | 7 separate functions | 1 (`step_year`) |
| Sector update | 4 separate functions | 1 (`sector_breakdown`) |
| Starting baselines | Hardcoded 150M jobs (toy) | Live from World Bank, real billions |
| Country support | None (always world) | Yes (any World Bank code) |
| Sector splits | Hardcoded percentages | Live per-country from World Bank |
| Wage tiers | Author-set | Calibrated to BLS OEWS May 2024 |
| Sensitivity logic | Inline mini-simulation, dead code | Clean reuse of `run_scenario` via `override_rate` |
| Constants location | Scattered inside functions | All at top in `CONSTANTS` section |
| `SKILLS` / `SECTORS` format | Multiple separate dicts | Single dict per concept, tuple-packed |

---

## Common Python Patterns Used in This File

### Pattern 1: Dict comprehension to transform a dict

```python
{tier: SKILLS[tier][1] * (1 + SKILLS[tier][3] * adoption) for tier in SKILLS}
```

**Used by:** `wages_by_skill`, `skill_breakdown`, `compare_scenarios`.

### Pattern 2: Fallback with `or`

```python
employment or float(INITIAL_JOBS)
```

Returns the first truthy value. If `employment` is None/0, uses the fallback. **Used by:** `fetch_world_bank_baseline`, `report`.

### Pattern 3: Optional override parameter

```python
def run_scenario(..., override_rate: Optional[float] = None):
    auto_rate = override_rate if override_rate is not None else SCENARIO_RATES[scenario]
```

Let callers tweak one input without duplicating the function body. **Used by:** `run_scenario`, leveraged by `sensitivity`.

### Pattern 4: Try / Except with silent fallback

```python
try:
    data = fetch_live()
except Exception:
    data = fetch_synthetic()
```

**Used by:** `_wb_latest`, `fetch_world_bank_unemployment`. Critical for resilience.

### Pattern 5: Tuple-packed constants

```python
SKILLS = {"L1_basic": (share, wage, risk, pressure), ...}
SKILLS[tier][0]   # share
SKILLS[tier][1]   # wage
```

Compresses 4 separate dicts into one. **Used by:** `SKILLS`, `SECTORS`.

### Pattern 6: Tuple unpacking in for loops

```python
for sec, (_, sector_auto, growth, _r) in SECTORS.items():
```

Unpack key and tuple value in one line. **Used by:** `sector_breakdown`.

### Pattern 7: Lazy cache

```python
if key in _CACHE:
    return _CACHE[key]
_CACHE[key] = compute()
return _CACHE[key]
```

**Used by:** `get_country_baseline`. Prevents re-fetching expensive data.

### Pattern 8: NumPy axis aggregation

```python
np.mean(matrix, axis=0)
np.percentile(matrix, 2.5, axis=0)
```

`axis=0` = "compute down each column." Turns a 1000×20 matrix into a 20-element array of per-year statistics. **Used by:** `monte_carlo`.

### Pattern 9: F-string interpolation

```python
f"https://api.worldbank.org/v2/country/{country}/indicator/{indicator}"
f"sector_{sec}"
```

**Used by:** every API URL build, CSV column naming.

---

## Glossary of Every Symbol

Quick lookup for anything weird you encounter:

| Symbol | Where you'll see it | What it means |
|---|---|---|
| `:` | After function name, after `if`/`for`/`def` | "Start a code block" |
| `->` | After function parameters | "Returns this type" |
| `=` | Anywhere | Assignment (not equality!) |
| `==` | In conditions | Equality test |
| `!=` | In conditions | Not equal |
| `+`  `-`  `*`  `/` | Math | Add / subtract / multiply / divide |
| `//` | Math | Integer divide (drop decimal) |
| `**` | Math, function calls | Power OR "unpack dict as kwargs" |
| `*=`, `+=`, `-=` | Statements | In-place modify |
| `[]` | Around values | List (or index: `arr[0]`) |
| `{}` | Around values | Dict (if `key: value`) or set |
| `()` | Around values | Tuple OR function call |
| `_` in numbers | `3_400_000_000` | Cosmetic separator |
| `_` as variable | `for _ in ...` | "I don't care" |
| Leading `_` in name | `_wb_latest`, `_BASELINE_CACHE` | Convention: private |
| `f"..."` | String literal | F-string (interpolates `{vars}`) |
| `"""..."""` | String literal | Multi-line string / docstring |
| `lambda x: x[0]` | Inside function calls | Anonymous one-line function |
| `is None` | In conditions | Check for the None value |
| `in` | Conditions / for loops | Membership / iteration |
| `not` | In conditions | Logical NOT |
| `and` / `or` | In conditions | Logical AND / OR |
| `None` / `True` / `False` | Anywhere | The 3 special values |
| `return` | Inside function | Hand back a value |
| `pass` | Inside a block | "Do nothing" (placeholder) |
| `Optional[X]` | Type hints | "Could be X or None" |
| `Dict[K, V]` | Type hints | "Dictionary with K keys, V values" |
| `Any` | Type hints | "Anything goes" |

---

## End Notes

### Line count breakdown

| Category | Lines |
|---|---|
| Total | **481** |
| Blank lines | 79 |
| Hash comments (`#`) | 52 |
| Docstring lines | 36 |
| **Pure executable code** | **318** |

The file is roughly **66% code, 18% comments, 16% whitespace** — a healthy ratio for readable code.

### What you've just read

- Every function in the cleaned `simulation.py` explained line by line
- Every Python keyword, operator, and pattern explained
- Worked numerical examples for every important calculation
- Connection diagram showing data flow between sections
- Glossary of every symbol you might encounter
- Comparison table vs. the original 562-line version

### Reading order recommendation

If you want to **understand the model fastest**:
1. Read SECTION A (constants) — 5 minutes, gives you all the magic numbers
2. Read SECTION C → `step_year` — 5 minutes, this is the per-year engine
3. Read SECTION E → `run_scenario` — 5 minutes, this is the main loop
4. Skim SECTION D for breakdowns
5. Skim SECTION B for live-data fetching
6. Read SECTIONS F & G last (validation, outputs)

If you want to **extend the model**, the easiest entry points are:
- Add a new sector → edit `SECTORS` constant + add to spillover logic in `sector_breakdown`
- Add a new skill tier → edit `SKILLS` constant
- Add a new scenario → add an entry to `SCENARIO_RATES`
- Add a new country → no code change needed, just pass the World Bank code

End of document.
