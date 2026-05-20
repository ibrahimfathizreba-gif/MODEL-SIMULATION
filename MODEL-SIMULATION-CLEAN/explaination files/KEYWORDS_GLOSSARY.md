# `simulation.py` — Keywords, Codes & Jargon Decoder

> **What this file is:** A companion to `SIMULATION_EXPLAINED.md`. Where that file walks through code line by line, this file decodes every **name**, **code**, **abbreviation**, and **unit** that appears in the simulation engine.
>
> Use this when you see something like `unem_pct` or `SL.AGR.EMPL.ZS` and think "what does that actually stand for?"

---

## Table of Contents

1. [How to Read This File](#1-how-to-read-this-file)
2. [Variable Names — What Every Name Stands For](#2-variable-names--what-every-name-stands-for)
3. [World Bank Indicator Codes — Letter by Letter](#3-world-bank-indicator-codes--letter-by-letter)
4. [Constants — What Every Magic Number Means](#4-constants--what-every-magic-number-means)
5. [Economic & Math Terms](#5-economic--math-terms)
6. [Units Cheat Sheet](#6-units-cheat-sheet)
7. [Function Parameter Decoder](#7-function-parameter-decoder)
8. [Acronyms (BLS, OEWS, WLD, GDP, etc.)](#8-acronyms-bls-oews-wld-gdp-etc)
9. [Python Naming Conventions Used in This File](#9-python-naming-conventions-used-in-this-file)

---

## 1. How to Read This File

The simulation engine uses short variable names like `unem`, `srv`, `ind`, `agri`, `gdp_usd`. These aren't arbitrary — every one is an abbreviation of an economic term. This file expands every one of them.

**Example:** `unem_pct = 5.0`
- `unem` → short for **unemployment**
- `_pct` → suffix meaning **percent**
- Combined meaning: "the unemployment rate, expressed as a percent" — so `5.0` means 5%, not 5 people or 0.05.

Once you internalize the naming pattern, the code reads itself.

---

## 2. Variable Names — What Every Name Stands For

### A — Adoption, automation, agri

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `adoption` | AI **adoption** rate (% of work automated by AI) | fraction (0.0–1.0) | `0.42` = 42% adopted | `step_year`, `sector_breakdown`, `wages_by_skill` |
| `ai_adoption` | Same as `adoption` — stored on the `state` dict | fraction (0.0–1.0) | `0.05` (start), `0.95` (year 20) | Everywhere |
| `agri` | **Agriculture** share of employment | fraction (0.0–1.0) after divide by 100 | `0.014` = 1.4% of jobs | `fetch_world_bank_sectors` |
| `auto_rate` | **Automation rate** — base annual job displacement | fraction (0.0–1.0) | `0.05` for "moderate" scenario | `step_year`, `sector_breakdown`, `run_scenario` |
| `automation_rate` | Same as `auto_rate` — full name in results dict | fraction (0.0–1.0) | `0.05` | `run_scenario` results |

### B — Baseline

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `base` | **Baseline** values (initial economic state) | dict | `{employment: 3.4e9, ...}` | `fetch_world_bank_baseline`, `get_country_baseline` |
| `base_rate` | **Baseline automation rate** for sensitivity tests | fraction | `0.05` | `sensitivity` |
| `base_unem` | **Baseline unemployment** for sensitivity comparison | percent | `8.2` | `sensitivity` |
| `BASE_YEAR` | The year the simulation **starts** | year (integer) | `2026` | top-level constant |
| `_BASELINE_CACHE` | In-memory **cache** of fetched country baselines (the leading underscore means "private — don't access from outside this file") | dict | `{"USA": {...}, "WLD": {...}}` | module-level |

### C — Country, count, created

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `count` | **Count** of people in a wage bucket (for Gini math) | integer | `42` | `gini_index` |
| `country` | World Bank **country code** | 3-letter string | `"USA"`, `"WLD"`, `"DEU"` | most functions |
| `created` | Number of jobs **created** by AI (in a year) | count of jobs | `8_500_000` | `step_year`, `validate` |

### E — Employment, end

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `employment` | Total number of people **employed** | count of people | `3.4e9` (3.4 billion) | `fetch_world_bank_baseline` |
| `end` | **End year** for the backtest range | year (integer) | `2020` | `validate`, `fetch_world_bank_unemployment` |

### G — GDP, growth, gini

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `gdp` | **Gross Domestic Product** — total economic output | trillion USD | `108.5` = $108.5 trillion | `step_year`, `run_scenario` |
| `gdp_base` | Starting GDP before the AI multiplier is applied | trillion USD | `105.0` | `step_year` |
| `gdp_trillion` | GDP **in trillions** of USD | trillion USD | `105.3` | `fetch_world_bank_baseline` |
| `gdp_usd` | GDP **in raw USD** (un-divided) | dollars | `105_000_000_000_000` | `fetch_world_bank_baseline` |
| `gini` | **Gini coefficient** — inequality measure (0=equal, 1=max unequal) | fraction (0.0–1.0) | `0.38` | `gini_index`, `run_scenario` |
| `growth` | Annual **growth rate** of a sector | fraction | `0.06` = 6% per year | `sector_breakdown` |

### H — High, horizon

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `high_rate`, `high_speed` | **High-perturbation** result in sensitivity test (+20%) | percent (unemployment) | `9.5` | `sensitivity` |
| `horizon` | How many years to **simulate forward** | years (integer) | `20` | `run_scenario`, `monte_carlo` |

### I — Income, ind, indicator

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `i` | Loop **index** counter | integer | `0, 1, 2, ..., 19` | every `for` loop |
| `incomes` | Synthetic list of **incomes** for Gini calculation | list of floats | `[33000, 33000, 49000, ...]` | `gini_index` |
| `ind` | **Industry** share of employment | fraction | `0.194` = 19.4% | `fetch_world_bank_sectors` |
| `indicator` | World Bank **indicator code** string | string | `"SL.EMP.TOTL"` | `_wb_latest` |
| `INITIAL_*` constants | **Starting values** (fallbacks if WB API fails) | varies | see Constants section | module-level |

### J — Jobs

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `jobs` | Dict of **jobs per sector** | dict[str, float/int] | `{"Tech": 340e6, ...}` | `sector_breakdown` |
| `jobs_created` | Number of jobs **AI creates** in a year | count | `8.5e7` | `step_year` |
| `jobs_lost` | Number of jobs **AI destroys** in a year | count | `1.4e8` | `step_year` |
| `JOB_CREATION_RATIO` | Ratio of jobs **created per job lost** | fraction (0.0–1.0+) | `0.60` = 60 created per 100 lost | module-level constant |

### K — Speed coefficient

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `k` | **Steepness coefficient** of the S-curve (mathematical convention) | float | `0.35 * speed` | `ai_adoption` |

### L — Labor, low, live, lost

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `labor_force` | Total **labor force** (employed + actively job-seeking) | count of people | `3.6e9` | `fetch_world_bank_baseline` |
| `live` | Flag: did we get **real-time data** (vs fallback)? | boolean | `True` or `False` | `fetch_world_bank_baseline` |
| `lost` | Jobs **lost** to automation in `validate` | count | `1.2e6` | `validate` |
| `low_rate`, `low_speed` | **Low-perturbation** result in sensitivity (-20%) | percent | `7.1` | `sensitivity` |

### M — Mae, matrix

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `mae` | **Mean Absolute Error** (backtest accuracy metric) | percent points | `0.85` | `validate` |
| `unem_matrix`, `gdp_matrix` | 2D array storing **all simulation runs** | numpy array | shape `(1000, 20)` | `monte_carlo` |

### N — N (count)

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `n` | **Number** of items (size of an array) | integer | `42` | `gini_index` |
| `n_simulations` | **Number of Monte Carlo runs** | integer | `1000` | `monte_carlo` |

### P — Predicted, productivity, payload

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `payload` | The **JSON response body** from the WB API | parsed JSON (list/dict) | `[{...meta...}, [{...rows...}]]` | `_wb_latest`, `fetch_world_bank_unemployment` |
| `predicted` | Model's **predicted** unemployment values in backtest | list of percents | `[5.5, 5.7, ...]` | `validate` |
| `productivity` | Output per worker, scaled by AI **productivity** boost | multiplier | `1.65` = 65% boost | `step_year` |

### R — Real, resp, row, rows

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `real` | **Real-world** (historical) unemployment data | dict | `{years: [...], values: [...]}` | `validate` |
| `resp` | HTTP **response** object from the requests library | `requests.Response` | (an object) | `_wb_latest`, `fetch_world_bank_unemployment` |
| `row`, `rows` | A **record** (or list of records) from the WB API | dict / list | `{"date": "2024", "value": 5.0}` | data fetchers |
| `results` | Full **results** dict returned from a scenario run | dict | `{years: [...], gdp: [...], ...}` | `run_scenario` |

### S — Sector, share, skill, sim, speed, spending, srv, start, state

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `sec` | A **sector** name (loop variable) | string | `"Tech"`, `"Healthcare"` | `sector_breakdown` |
| `sector_auto` | Per-sector **automation factor** (how exposed it is) | fraction | `0.04` (Tech), `0.08` (Mfg) | `sector_breakdown` |
| `services_bucket` | Combined **Services + Agriculture** share | fraction | `0.806` = 80.6% | `fetch_world_bank_sectors` |
| `shares` | Dict of **sector shares** | dict[str, float] | `{"Tech": 0.14, ...}` | `sector_breakdown` |
| `sim` | Loop variable for **simulation number** in Monte Carlo | integer | `0..999` | `monte_carlo` |
| `skill_breakdown` returns `skills` | Dict of **skill tier sizes** | dict[str, int] | `{"L1_basic": 720e6, ...}` | `run_scenario` |
| `speed`, `adoption_speed` | **Multiplier on the S-curve steepness** | float | `1.0` = default, `1.5` = faster | `ai_adoption`, `step_year` |
| `spending` | Consumer **spending** | trillion USD | `73.5` | `step_year` |
| `spillover` | Tech sector's **spillover effect** on other sectors | jobs count | `1.2e7` | `sector_breakdown` |
| `srv` | **Services** share of employment | fraction | `0.792` = 79.2% | `fetch_world_bank_sectors` |
| `start` | **Start year** for backtest range | year | `2000` | `validate`, `fetch_world_bank_unemployment` |
| `state` | The **mutable model state** dict passed year-to-year | dict | `{total_jobs, workforce, ai_adoption}` | most core functions |
| `step` | Output of `step_year()` for **one year** | dict | `{unem, productivity, gdp, spending}` | `run_scenario` |
| `summary` | **Summary statistics** dict (mean/std/min/max) | dict | `{unemployment: {mean: 7.2, ...}}` | `summarize` |

### T — Tier, total

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `tier` | A **skill tier** name (loop variable) | string | `"L1_basic"`, `"L5_expert"` | `skill_breakdown`, `wages_by_skill`, `gini_index` |
| `total` | **Total jobs** (alias for `state["total_jobs"]`) | count | `3.4e9` | `sector_breakdown` |
| `total_jobs` | **Total employed** workers | count | `3.4e9` | `state` dict |

### U — Unem, url

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `unem` | **Unemployment rate** as a **fraction** (0.0–1.0) | fraction | `0.08` = 8% | `step_year`, `validate` |
| `unem_pct` | **Unemployment rate** as a **percent** (0–100) | percent | `8.0` = 8% | `fetch_world_bank_baseline` |
| `url` | The HTTP request **URL** (web address) | string | `"https://api.worldbank.org/..."` | data fetchers |

### V — Value, values

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `v` | Generic **value** in a comprehension | any | varies | `sector_breakdown` (`for sec, v in jobs.items()`) |
| `value` | A single data point's **value** from WB API | float | `5.4` | `_wb_latest` |
| `values` | List of **values** | list | `[5.5, 5.7, 6.0]` | `fetch_world_bank_unemployment` |

### W — Wage, workforce

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `wage` | A skill tier's **annual wage** in USD | dollars | `49_000` | `gini_index` |
| `wages` | Dict of **wages by skill tier** | dict[str, float] | `{"L1_basic": 28_050, ...}` | `wages_by_skill`, `gini_index` |
| `WORKFORCE_GROWTH` | Annual **growth rate of labor force** | fraction | `0.008` = 0.8%/yr | module-level constant |
| `workforce` | Total **labor force** (working + looking) | count of people | `3.6e9` | `state` dict |

### Y — Year

| Name in code | Stands for | Unit | Example value | Where it appears |
|---|---|---|---|---|
| `year` | A specific calendar **year** | integer | `2030` | loops |
| `year_index` | **Years since `BASE_YEAR`** (0-based) | integer | `0..19` | `ai_adoption`, `step_year` |
| `years` | List of **years** in the result | list of integers | `[2026, 2027, ..., 2045]` | `run_scenario`, `validate` |

### Special characters

| Name in code | Stands for | Where |
|---|---|---|
| `_` (single underscore) | "I don't care about this value" (throwaway loop variable) | `for i, _ in enumerate(years)` |
| `_r` (underscore-r) | "**Reserved**" — placeholder slot, currently unused | `for sec, (_, sector_auto, growth, _r) in SECTORS.items()` |
| `_gdp_base` (leading underscore) | **Private** state key (model-internal, not public output) | `state` dict |
| `_country` | **Private** state key | `state` dict |

---

## 3. World Bank Indicator Codes — Letter by Letter

The World Bank uses dotted codes like `SL.AGR.EMPL.ZS`. Every segment has meaning. Here's the **decoding key**, then every code used in `simulation.py`.

### Decoding key

Every indicator code follows the pattern `<TOPIC>.<SUBJECT>.<MEASURE>.<UNIT>`.

**Topic prefix** (first segment):

| Code | Stands for | Topic |
|---|---|---|
| `SL` | **Social: Labor** | Employment, labor force, unemployment |
| `NY` | **National accounts: Income** | GDP, GNI, value added |
| `SP` | **Social: Population** | Demographics |
| `EN` | **Environment** | Emissions, energy |
| `SE` | **Social: Education** | Schooling, literacy |

**Subject** (second segment) — varies by topic. Common ones in `SL`:

| Code | Stands for |
|---|---|
| `EMP` | **Employment** (people working) |
| `UEM` | **Unemployment** |
| `TLF` | **Total Labor Force** |
| `AGR` | **Agriculture** (sector) |
| `IND` | **Industry** (sector) |
| `SRV` | **Services** (sector) |

**Measure** (third segment) — what's actually being counted:

| Code | Stands for |
|---|---|
| `TOTL` | **Total** count |
| `EMPL` | **Employment in** (this sector) |
| `MKTP` | **Market Price** value |
| `IN` | "**In**" (raw count of persons) |

**Unit** (last segment):

| Code | Stands for | Example |
|---|---|---|
| `CD` | **Current US Dollar** | GDP in today's dollars |
| `CN` | **Current National** currency | GDP in local currency |
| `KD` | **Constant Dollar** (inflation-adjusted) | Real GDP |
| `ZS` | **Share (Zero-Share)** → **percent of total** | Unemployment as % of labor force |
| `IN` | Sometimes raw count (`TOTL.IN` = total in persons) | |
| `KG` | Kilograms | |

### Every code used in `simulation.py`

#### `SL.EMP.TOTL` — Total Employment

- **`SL`** = Social: **L**abor
- **`EMP`** = **Emp**loyment
- **`TOTL`** = **Tot**a**l**
- (no `.ZS` or `.IN`) = raw count of people

**Full meaning:** "Employment, total" — the number of people currently working, globally or in a region.

**Where it's used:** `_wb_latest("SL.EMP.TOTL", country)` in [simulation.py:96](backend/simulation.py#L96).

**Catch:** Only published for `country="WLD"` (the world aggregate). For individual countries, it returns nothing — see the fallback math in line 101-102.

**Example value:** `3_400_000_000` (3.4 billion people).

---

#### `SL.TLF.TOTL.IN` — Total Labor Force, in Persons

- **`SL`** = Social: **L**abor
- **`TLF`** = **T**otal **L**abor **F**orce
- **`TOTL`** = **Tot**a**l**
- **`IN`** = **I**n persons (raw count, not percent)

**Full meaning:** "Labor force, total" — the number of people working + actively looking for work.

**Where it's used:** `_wb_latest("SL.TLF.TOTL.IN", country)` in [simulation.py:97](backend/simulation.py#L97).

**Example value:** `3_600_000_000` (3.6 billion).

**How it differs from `SL.EMP.TOTL`:** Labor force = employed + unemployed-but-looking. Employment = employed only. The difference is the unemployed.

---

#### `SL.UEM.TOTL.ZS` — Unemployment Rate (% of Labor Force)

- **`SL`** = Social: **L**abor
- **`UEM`** = **U**n**em**ployment
- **`TOTL`** = **Tot**a**l**
- **`ZS`** = % share of total

**Full meaning:** "Unemployment, total (% of total labor force)" — the percent of the labor force that's unemployed.

**Where it's used:** `_wb_latest("SL.UEM.TOTL.ZS", country)` in [simulation.py:99](backend/simulation.py#L99) and again in `fetch_world_bank_unemployment` [L384](backend/simulation.py#L384).

**Example value:** `5.4` (meaning 5.4% unemployment).

**Why the model needs it:** For individual countries (where `SL.EMP.TOTL` isn't published), the code derives employment from `labor_force × (1 − unem_pct / 100)`.

---

#### `NY.GDP.MKTP.CD` — GDP at Market Prices, Current US Dollar

- **`NY`** = **N**ational accounts: income (the "Y" is for "income" in economics notation)
- **`GDP`** = **G**ross **D**omestic **P**roduct
- **`MKTP`** = at **M**ar**k**e**t** **P**rices (market valuation, not factor cost)
- **`CD`** = **C**urrent **D**ollar (US dollars, not inflation-adjusted)

**Full meaning:** "GDP (current US$)" — total economic output for the year, in today's US dollars.

**Where it's used:** `_wb_latest("NY.GDP.MKTP.CD", country)` in [simulation.py:98](backend/simulation.py#L98).

**Example value:** `105_000_000_000_000` (about $105 trillion for the world in 2024).

**Note on units:** The raw API value is in **dollars** — line 109 converts to **trillions** by dividing by `1e12`. The model stores GDP in trillions throughout.

---

#### `SL.AGR.EMPL.ZS` — Employment in Agriculture (% of Total Employment)

- **`SL`** = Social: **L**abor
- **`AGR`** = **Ag**ricultu**r**e
- **`EMPL`** = **Empl**oyment in (this sector)
- **`ZS`** = % share of total employment

**Full meaning:** "Employment in agriculture (% of total employment)" — the share of all workers who are in agriculture, forestry, or fishing.

**Where it's used:** `_wb_latest("SL.AGR.EMPL.ZS", country)` in [simulation.py:127](backend/simulation.py#L127).

**Example value:** `27.5` (27.5% of workers, e.g. for a developing country), or `1.4` (1.4%, e.g. for the USA).

**In this model:** Agriculture is rolled into the "Services" bucket on line 135 (`services_bucket = srv + agri`) because the model doesn't have an Agriculture sector category.

---

#### `SL.IND.EMPL.ZS` — Employment in Industry (% of Total Employment)

- **`SL`** = Social: **L**abor
- **`IND`** = **Ind**ustry
- **`EMPL`** = **Empl**oyment in (this sector)
- **`ZS`** = % share of total employment

**Full meaning:** "Employment in industry (% of total employment)" — workers in mining, manufacturing, construction, electricity, gas, water.

**Where it's used:** `_wb_latest("SL.IND.EMPL.ZS", country)` in [simulation.py:128](backend/simulation.py#L128).

**Example value:** `19.4` (about 19% of workers, typical for the USA).

**In this model:** Industry maps **directly** to the "Manufacturing" sector — see line 138.

---

#### `SL.SRV.EMPL.ZS` — Employment in Services (% of Total Employment)

- **`SL`** = Social: **L**abor
- **`SRV`** = **S**e**rv**ices
- **`EMPL`** = **Empl**oyment in (this sector)
- **`ZS`** = % share of total employment

**Full meaning:** "Employment in services (% of total employment)" — workers in trade, transport, hospitality, finance, education, health, public admin, etc.

**Where it's used:** `_wb_latest("SL.SRV.EMPL.ZS", country)` in [simulation.py:129](backend/simulation.py#L129).

**Example value:** `79.2` (about 79% of workers, typical for the USA).

**In this model:** The Services bucket is **subdivided** into Tech / Healthcare / Services-other using fixed ratios (18%/24%/58%) on lines 137-140, because the World Bank doesn't break Services down further.

---

### Why all this matters

The simulation needs **employment, labor force, GDP, and sector shares** to start. The World Bank publishes the most authoritative free numbers for all four. Each indicator code is just a stable identifier — once you know the decoding pattern, you can find any indicator you want (e.g., `SL.EMP.TOTL.SP.ZS` for "employment % of population," `EN.ATM.CO2E.PC` for "CO2 emissions per capita").

You can browse the full list at: https://data.worldbank.org/indicator

---

## 4. Constants — What Every Magic Number Means

These are the numbers that drive the whole simulation. Tweak any of them and the model's predictions shift.

| Constant | Value | Unit | Meaning | Why this value |
|---|---|---|---|---|
| `BASE_YEAR` | `2026` | year | First year of the simulation | Project assumes simulation starts in 2026 |
| `INITIAL_JOBS` | `3_400_000_000` | people | Fallback global employment | ~2024 real figure from WB `SL.EMP.TOTL` |
| `INITIAL_WORKFORCE` | `3_600_000_000` | people | Fallback global labor force | ~2024 real figure from WB `SL.TLF.TOTL.IN` |
| `INITIAL_GDP` | `105.0` | trillion USD | Fallback global GDP | ~2024 real figure from WB `NY.GDP.MKTP.CD` |
| `INITIAL_ADOPTION` | `0.05` | fraction | Starting AI-adoption level | Modeling assumption — ~5% of work AI-assisted in 2026 |
| `WORKFORCE_GROWTH` | `0.008` | fraction/yr | Annual growth of labor force | 0.8% — matches UN demographic projections |
| `JOB_CREATION_RATIO` | `0.60` | ratio | New jobs created per job lost | 60 created per 100 destroyed — model assumption |
| `SCENARIO_RATES["slow"]` | `0.03` | fraction/yr | Base annual displacement, slow rollout | 3% baseline |
| `SCENARIO_RATES["moderate"]` | `0.05` | fraction/yr | Base annual displacement, moderate rollout | 5% baseline |
| `SCENARIO_RATES["rapid"]` | `0.08` | fraction/yr | Base annual displacement, rapid rollout | 8% baseline |

### `SKILLS` dict — what each tuple means

Format: `tier_name: (share_of_workforce, base_wage_usd, ai_risk, wage_pressure)`

| Tier | Share | Wage (USD/yr) | AI risk | Wage pressure | Real-world example |
|---|---|---|---|---|---|
| `L1_basic` | 20% | $33,000 | 75% | -15% | Cashiers, janitors, food prep |
| `L2_semi` | 30% | $49,000 | 55% | -8% | Truck drivers, machine operators |
| `L3_intermediate` | 25% | $73,000 | 35% | +2% | Admin assistants, nurses |
| `L4_advanced` | 15% | $115,000 | 15% | +12% | Engineers, general managers |
| `L5_expert` | 10% | $200,000 | 5% | +22% | Executives, lawyers, surgeons |

- **`share_of_workforce`** — fraction of all workers in this tier (sums to 1.00)
- **`base_wage_usd`** — annual wage in 2026 dollars (BLS OEWS May 2024 source)
- **`ai_risk`** — fraction of jobs in this tier exposed to AI displacement (informational; not yet wired into the model loop)
- **`wage_pressure`** — how much wages move at full AI adoption: `wage × (1 + pressure × adoption)`. Negative = wages drop, positive = wages rise.

### `SECTORS` dict — what each tuple means

Format: `sector_name: (share_of_jobs, automation_rate, growth_rate, _reserved)`

| Sector | Share | Automation rate | Growth rate | Reserved |
|---|---|---|---|---|
| `Tech` | 10% | 4% | 6% | 0.0 |
| `Manufacturing` | 22% | 8% | 1% | 0.0 |
| `Healthcare` | 13% | 2% | 4% | 0.0 |
| `Services` | 55% | 6% | 2% | 0.0 |

- **`share_of_jobs`** — fallback share of total jobs (real share comes from WB when available)
- **`automation_rate`** — how exposed this sector is to AI automation (Manufacturing highest, Healthcare lowest)
- **`growth_rate`** — annual organic growth from AI productivity gains (Tech highest, Manufacturing lowest)
- **`_reserved`** — unused placeholder slot, kept for future extensions

---

## 5. Economic & Math Terms

### Adoption rate
The fraction of work where AI is in active use. Modeled as a **logistic S-curve** — slow start, fast middle, slow saturation.

### AI risk
A property of each skill tier — what fraction of jobs in that tier could plausibly be automated by AI. Low-skill jobs (L1) have 75% risk; high-skill jobs (L5) have 5% risk.

### Automation rate (`auto_rate`)
The annual fraction of jobs that get displaced **at full adoption**. Scaled by current adoption level: actual jobs lost in a year = `total_jobs × auto_rate × adoption`.

### Backtest
Running the model on **past data** to see how well it predicts known historical outcomes. The `validate` function backtests against 2000-2020 unemployment from the World Bank.

### Consumer spending
Total amount consumers spend per year. Modeled as a fraction of GDP that **shrinks when unemployment rises**: `gdp × max(0.30, 0.68 − unem × 1.2)`.

### Current dollars vs. constant dollars
- **Current** dollars = actual prices in that year (not adjusted for inflation)
- **Constant** dollars = prices adjusted to a base year (inflation removed)

The model uses **current dollars** (WB code `.CD`).

### GDP (Gross Domestic Product)
Total value of goods and services produced in a year. The model expresses GDP in **trillions of USD**.

### Gini coefficient
A number from 0 to ~1 measuring income inequality.
- `0` = everyone earns the same
- `1` = one person earns everything (max inequality)
- Real world: USA ≈ 0.41, Sweden ≈ 0.29, South Africa ≈ 0.63

Computed by sorting incomes and applying: `(2 × Σ(i × y_i)) / (n × Σy) − (n + 1) / n`.

### Job creation ratio
How many new jobs are created per job destroyed. Set to `0.60` — the model says AI destroys more jobs than it creates (matching most economist forecasts, but not all).

### Labor force
**Employed + actively looking for work**. Excludes retirees, students, stay-at-home parents, discouraged workers. Source: WB `SL.TLF.TOTL.IN`.

### Logistic S-curve
A growth curve that looks like the letter **S** — slow start, exponential middle, slow saturation. Equation: `1 / (1 + e^(-k(x − x_0)))`.

Used in `ai_adoption` to model AI rollout. Midpoint is at year 10, controlled by parameter `k = 0.35 × speed`.

### Mean Absolute Error (MAE)
Average of the absolute differences between predicted and actual values. The smaller, the more accurate. Computed in `validate` to score the model's backtest.

### Monte Carlo simulation
Run the simulation **many times with random parameter variations**, then look at the distribution of outcomes. Reports the mean and 95% confidence band (2.5th to 97.5th percentile). See `monte_carlo()`.

### Percentile
The value below which X% of observations fall. The 97.5th percentile of unemployment = "97.5% of simulation runs had unemployment at or below this number."

### Productivity
Output per unit of labor. The model boosts productivity with AI: `1 + adoption^0.7 × 0.85`. At full adoption, productivity is 85% above baseline.

### Sector
A broad industry category. Model uses 4: **Tech, Manufacturing, Healthcare, Services**.

### Sensitivity analysis
Vary one parameter at a time by ±20% and measure how much the final result changes. Tells you which parameters matter most. See `sensitivity()`.

### Spillover
A change in one sector that **leaks into** another. The model has Tech-sector spillover that boosts Services and Healthcare but hurts Manufacturing.

### Tech spillover
Specifically: `jobs["Tech"] × 0.02 × adoption`. At full adoption, 2% of Tech jobs' value spills into other sectors via the formula on lines 226-229.

### Unemployment rate
Fraction (or %) of labor force that's unemployed: `(labor_force − employment) / labor_force`. The model recomputes this every year as the labor force grows and jobs shift.

### Wage pressure
Per-tier sensitivity of wages to AI adoption. Negative = wages drop (low-skill); positive = wages rise (high-skill). Formula: `wage = base_wage × (1 + pressure × adoption)`.

### Workforce
Same as labor force. Stored on `state["workforce"]`.

---

## 6. Units Cheat Sheet

| Variable | Unit | Convert to display |
|---|---|---|
| `total_jobs`, `workforce`, `employment`, `labor_force` | **count of people** (raw integer) | Often shown divided by 1e6 (millions) or 1e9 (billions) |
| `ai_adoption`, `adoption` | **fraction** 0.0–1.0 | Multiply by 100 for percent |
| `auto_rate`, `automation_rate` | **fraction** 0.0–1.0 | Multiply by 100 for percent |
| `unem` | **fraction** 0.0–1.0 | Multiply by 100 for percent |
| `unem_pct` | **percent** 0–100 | Already a percent |
| `gini` | **coefficient** 0.0–1.0 | Usually shown as-is or ×100 |
| `gdp`, `gdp_trillion`, `gdp_base` | **trillion USD** | Multiply by 1000 for billion USD |
| `gdp_usd` | **raw USD** | Divide by 1e12 for trillions |
| `spending` | **trillion USD** | Same as GDP |
| `productivity` | **multiplier** (1.0 = baseline) | Subtract 1, ×100 for "% above baseline" |
| `wage`, `wages` | **annual USD** | As-is |
| `year_index` | **years since BASE_YEAR** | Add `BASE_YEAR` to get calendar year |

**Common conversion mistakes to watch for:**
1. `unem` (fraction) vs. `unem_pct` (percent) — easy to mix up. The model uses the fraction everywhere internally.
2. `gdp_usd` (raw dollars from API) vs. `gdp_trillion` (after divide by 1e12). The model uses trillions everywhere internally.
3. Sector shares from WB come in as **percents** (`55.0`) — line 133 divides by 100 to get fractions.

---

## 7. Function Parameter Decoder

Quick lookup for every parameter on every function.

### `_wb_latest(indicator, country)`
- `indicator` — World Bank indicator code string, e.g. `"SL.EMP.TOTL"`
- `country` — 3-letter WB country code, e.g. `"WLD"` (world), `"USA"`, `"DEU"`

### `fetch_world_bank_baseline(country)`
- `country` — Same as above

### `fetch_world_bank_sectors(country)`
- `country` — Same as above

### `get_country_baseline(country)`
- `country` — Same as above (results cached)

### `ai_adoption(year_index, speed)`
- `year_index` — Years since `BASE_YEAR`, 0-based (so 2026 → 0, 2030 → 4, 2046 → 20)
- `speed` — Multiplier on the S-curve steepness. `1.0` is default, `1.5` makes adoption faster.

### `initial_state(country)`
- `country` — WB country code; defaults to `"WLD"`

### `step_year(state, year_index, auto_rate, speed)`
- `state` — Mutable dict holding `total_jobs`, `workforce`, `ai_adoption`
- `year_index` — Year offset from start (0..horizon-1)
- `auto_rate` — Base annual displacement rate (e.g., 0.05 for moderate)
- `speed` — S-curve speed multiplier

### `skill_breakdown(state)`
- `state` — Same state dict

### `wages_by_skill(adoption)`
- `adoption` — Current AI adoption fraction (0.0–1.0)

### `sector_breakdown(state, auto_rate)`
- `state` — State dict
- `auto_rate` — Same as in `step_year`

### `gini_index(wages, skills)`
- `wages` — Dict of `{tier: wage}` (output of `wages_by_skill`)
- `skills` — Dict of `{tier: count}` (output of `skill_breakdown`)

### `run_scenario(scenario, horizon, adoption_speed, override_rate, country)`
- `scenario` — `"slow"`, `"moderate"`, or `"rapid"`
- `horizon` — How many years forward to simulate (default 20)
- `adoption_speed` — S-curve speed multiplier (default 1.0)
- `override_rate` — Optional manual override for `auto_rate` (used by sensitivity tests)
- `country` — WB country code

### `compare_scenarios(horizon, adoption_speed, country)`
- Same as above, but runs all 3 scenarios at once

### `monte_carlo(n_simulations, horizon)`
- `n_simulations` — How many random runs to do (default 1000)
- `horizon` — Years per run (default 20)

### `sensitivity(scenario, country)`
- `scenario` — Which baseline scenario to perturb
- `country` — WB country code

### `fetch_world_bank_unemployment(start, end)`
- `start` — First year (e.g., 2000)
- `end` — Last year (e.g., 2020)

### `validate(start, end)`
- Same as above; runs the model from `start` and compares to real data

### `summarize(results)`
- `results` — Output dict from `run_scenario`

### `report(results)`
- Same input

### `export_csv(results, filepath)`
- `results` — Output dict from `run_scenario`
- `filepath` — Where to write the CSV (default `"simulation_output.csv"`)

---

## 8. Acronyms (BLS, OEWS, WLD, GDP, etc.)

| Acronym | Stands for | What it is |
|---|---|---|
| **AI** | **A**rtificial **I**ntelligence | The technology whose labor-market impact this model simulates |
| **API** | **A**pplication **P**rogramming **I**nterface | The World Bank's web service that returns JSON data |
| **BLS** | **B**ureau of **L**abor **S**tatistics | US government agency that publishes wage data (source for `SKILLS` wages) |
| **CD** | **C**urrent **D**ollar | WB unit suffix — see indicator codes |
| **CI** | **C**onfidence **I**nterval | Statistical range (Monte Carlo reports 95% CI) |
| **CSV** | **C**omma-**S**eparated **V**alues | Plaintext spreadsheet format used by `export_csv` |
| **DEU** | (ISO code for Germany) | Example country code |
| **GDP** | **G**ross **D**omestic **P**roduct | Total economic output |
| **GNI** | **G**ross **N**ational **I**ncome | Alternative income measure (not used here) |
| **HTTP** | **H**yper**T**ext **T**ransfer **P**rotocol | The protocol the WB API uses |
| **HTTPS** | HTTP **S**ecure | Encrypted HTTP |
| **ISIC** | **I**nternational **S**tandard **I**ndustrial **C**lassification | UN's hierarchy of industry codes |
| **ISO** | **I**nternational **O**rganization for **S**tandardization | Source of the 3-letter country codes |
| **JSON** | **J**ava**S**cript **O**bject **N**otation | The data format returned by the WB API |
| **L1...L5** | **L**evel 1 to 5 | The 5 skill tiers in `SKILLS` |
| **MAE** | **M**ean **A**bsolute **E**rror | Backtest accuracy metric |
| **NY** | **N**ational accounts: **Y** (income) | WB topic prefix |
| **OECD** | **O**rganisation for **E**conomic **C**o-operation and **D**evelopment | Group of ~38 rich countries |
| **OEWS** | **O**ccupational **E**mployment and **W**age **S**tatistics | BLS dataset (source for wage tiers) |
| **SDK** | **S**oftware **D**evelopment **K**it | Not used here, but you'll see it in docs |
| **SL** | **S**ocial: **L**abor | WB topic prefix |
| **UN** | **U**nited **N**ations | Source of population/demographic projections |
| **URL** | **U**niform **R**esource **L**ocator | Web address |
| **USA** | (ISO code for United States) | Example country code |
| **USD** | **U**nited **S**tates **D**ollar | Currency unit |
| **WB** | **W**orld **B**ank | Source of all live baseline data |
| **WLD** | (WB code for "World") | The aggregate of all countries combined |
| **ZS** | **Z**ero-**S**hare → percent | WB unit suffix |

---

## 9. Python Naming Conventions Used in This File

The codebase follows these conventions consistently:

| Pattern | Meaning | Examples in `simulation.py` |
|---|---|---|
| `lowercase_with_underscores` | Variables, functions | `total_jobs`, `step_year` |
| `UPPERCASE_WITH_UNDERSCORES` | Module-level constants (don't change at runtime) | `BASE_YEAR`, `INITIAL_JOBS`, `SCENARIO_RATES` |
| `_leading_underscore` | "Private" — internal use only, not part of the public API | `_wb_latest`, `_BASELINE_CACHE`, `_gdp_base`, `_country` |
| `_solo` | "Throwaway" — value I'm not using | `for i, _ in enumerate(years)` |
| `_r` | "Reserved" — placeholder slot | `for sec, (_, sector_auto, growth, _r) in ...` |
| `name_pct` suffix | Value is a **percent** (0–100) | `unem_pct` |
| `name_usd` suffix | Value is in **dollars** | `base_wage_usd`, `gdp_usd` |
| `name_trillion` suffix | Value is in **trillions** of USD | `gdp_trillion` |
| Single-letter loop vars (`i`, `n`, `k`) | Mathematical convention | `for i in range(horizon)` |
| Short economic abbrevs (`agri`, `ind`, `srv`, `unem`) | Match World Bank / standard econ shorthand | `fetch_world_bank_sectors` |

---

## End

Cross-references:
- For **line-by-line walkthroughs** of each function → `SIMULATION_EXPLAINED.md`
- For the **source code itself** → [backend/simulation.py](backend/simulation.py)
- For **World Bank indicator lookup** → https://data.worldbank.org/indicator
- For **BLS wage data** → https://www.bls.gov/oes/

If a name or term appears in `simulation.py` and isn't in this file, it's worth adding — open the file and append it to the relevant section.
