"""
Arabic Economic Advisory Report — generated via Ollama (local or cloud-routed LLM).

Default model: kimi-k2.6:cloud   (1T params, best Arabic quality)
Fallback:      qwen3.5:9b        (fully local)
"""
from __future__ import annotations

import os
from typing import Any, Dict, Optional

import requests


OLLAMA_HOST    = os.environ.get("OLLAMA_HOST",  "http://localhost:11434")
DEFAULT_MODEL  = os.environ.get("OLLAMA_MODEL", "kimi-k2.6:cloud")
FALLBACK_MODEL = "qwen3.5:9b"
REQUEST_TIMEOUT = 180   # seconds — generation can take a while

SYSTEM_PROMPT = (
    "أنت كبير المستشارين الاقتصاديين في منظمة العمل الدولية، خبير في تحليل تأثير "
    "الذكاء الاصطناعي على أسواق العمل والاقتصاد الكلي.\n\n"
    "مهمتك: تحليل نتائج محاكاة اقتصادية وتقديم تقرير استشاري احترافي شامل ومفصل.\n\n"
    "قواعد صارمة:\n"
    "1. اكتب الرد كاملاً باللغة العربية الفصحى فقط، دون أي كلمة بالإنجليزية.\n"
    "2. التزم بالأرقام الواردة في البيانات بدقة — لا تخترع أرقاماً جديدة.\n"
    "3. اربط استنتاجاتك بالبيانات الفعلية المُقدَّمة.\n"
    "4. استخدم لغة احترافية تليق بتقارير منظمات دولية كبرى.\n"
    "5. كن نقدياً وموضوعياً — لا تقدم تقريراً متفائلاً أو متشائماً بشكل مصطنع.\n\n"
    "هيكل التقرير الإلزامي:\n"
    "## 1. الملخص التنفيذي\n"
    "(فقرة مكثفة 3-5 أسطر تلخص أبرز النتائج)\n\n"
    "## 2. تحليل سوق العمل وتأثير الذكاء الاصطناعي\n"
    "(ناقش معدل البطالة، ذروة البطالة، تبنّي الذكاء الاصطناعي، الوظائف المفقودة والمخلوقة)\n\n"
    "## 3. التحليل الاقتصادي الكلي\n"
    "(الناتج المحلي، الأجور حسب المهارة، عدم المساواة، الإنفاق الاستهلاكي)\n\n"
    "## 4. التوقعات المستقبلية وسيناريوهات المخاطر\n"
    "(حدد المخاطر الرئيسية بناءً على الأرقام)\n\n"
    "## 5. التوصيات السياسية الاستراتيجية\n"
    "(قدم 5-7 توصيات عملية وملموسة، كل توصية في نقطة منفصلة)\n\n"
    "## 6. الخلاصة والرؤية المستقبلية\n"
    "(فقرة ختامية قوية)\n\n"
    "اجعل التقرير مفصلاً ومرتبطاً بالأرقام، مع تجنّب العموميات الفارغة."
)


def _format_simulation_summary(results: Dict[str, Any]) -> str:
    """Dense English summary of the simulation that the LLM can reason over."""
    summary = results.get("summary", {})
    report  = results.get("report",  {})

    unem  = results.get("unemployment", [])
    gdp   = results.get("gdp", [])
    wages = results.get("wages", {})
    sectors = results.get("sectors", {})

    unem_start  = unem[0]  if unem else 0
    unem_end    = unem[-1] if unem else 0
    unem_peak   = max(unem) if unem else 0
    gdp_start   = gdp[0]   if gdp else 0
    gdp_end     = gdp[-1]  if gdp else 0
    gdp_growth  = ((gdp_end - gdp_start) / gdp_start * 100) if gdp_start else 0

    wl_start = wages.get("L1_basic",  [0])[0]  if wages.get("L1_basic")  else 0
    wl_end   = wages.get("L1_basic",  [0])[-1] if wages.get("L1_basic")  else 0
    wh_start = wages.get("L5_expert", [0])[0]  if wages.get("L5_expert") else 0
    wh_end   = wages.get("L5_expert", [0])[-1] if wages.get("L5_expert") else 0

    lines = [
        f"SCENARIO: {results.get('scenario','moderate').upper()}",
        f"HORIZON: {report.get('start_year',2026)} – {report.get('end_year',2045)} "
        f"({len(results.get('years', []))} years)",
        f"AUTOMATION RATE: {report.get('automation_rate', 0.05)*100:.1f}% per year",
        "",
        "── LABOR MARKET ──",
        f"Unemployment: {unem_start:.2f}% → {unem_end:.2f}% (Δ {unem_end-unem_start:+.2f} pp)",
        f"Peak unemployment: {unem_peak:.2f}%",
        f"Final AI adoption: {report.get('final_ai_adoption_pct', 0):.1f}%",
        "",
        "── MACROECONOMY ──",
        f"GDP: ${gdp_start:.2f}T → ${gdp_end:.2f}T  ({gdp_growth:+.1f}%)",
        f"Gini Index: {report.get('final_gini', 0):.4f} (final year)",
        "",
        "── WAGE GAP ──",
        f"Lowest-skill (L1):  ${wl_start:,.0f} → ${wl_end:,.0f}",
        f"Highest-skill (L5): ${wh_start:,.0f} → ${wh_end:,.0f}",
        f"Wage ratio (L5/L1): {(wh_end/wl_end if wl_end else 0):.2f}x",
        "",
        "── SECTORS (final year, jobs) ──",
    ]
    for sec, jobs in sectors.items():
        final = jobs[-1] if jobs else 0
        lines.append(f"  {sec}: {final/1e6:.1f}M")

    lines.append("")
    lines.append("── SUMMARY STATISTICS ──")
    for metric, stats in summary.items():
        if isinstance(stats, dict):
            lines.append(
                f"{metric}: mean={stats.get('mean',0):.3f}, "
                f"std={stats.get('std',0):.3f}, "
                f"range=[{stats.get('min',0):.3f}, {stats.get('max',0):.3f}]"
            )
    return "\n".join(lines)


def _call_ollama(model: str, user_message: str) -> Dict[str, Any]:
    resp = requests.post(
        f"{OLLAMA_HOST}/api/chat",
        json={
            "model":    model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": user_message},
            ],
            "stream":  False,
            "options": {"temperature": 0.4, "top_p": 0.9, "num_predict": 3500},
        },
        timeout=REQUEST_TIMEOUT,
    )
    resp.raise_for_status()
    return resp.json()


def analyze_with_local_llm(results: Dict[str, Any], model: Optional[str] = None) -> Dict[str, Any]:
    chosen = model or DEFAULT_MODEL
    summary_text = _format_simulation_summary(results)
    user_message = (
        "فيما يلي نتائج المحاكاة الفعلية لتأثير الذكاء الاصطناعي على سوق العمل "
        "للسيناريو المختار:\n\n"
        f"```\n{summary_text}\n```\n\n"
        "يرجى تقديم التقرير الاستشاري الاقتصادي الشامل وفقاً للهيكل المحدد، "
        "مع التركيز على الأرقام الواردة أعلاه."
    )

    try:
        data = _call_ollama(chosen, user_message)
    except requests.exceptions.RequestException as e:
        if chosen != FALLBACK_MODEL:
            try:
                data = _call_ollama(FALLBACK_MODEL, user_message)
                chosen = FALLBACK_MODEL + " (fallback)"
            except Exception as e2:
                return {
                    "success": False,
                    "report":  f"تعذّر الاتصال بـ Ollama على {OLLAMA_HOST}.",
                    "error":   f"{type(e).__name__}: {e} | fallback: {e2}",
                }
        else:
            return {
                "success": False,
                "report":  f"تعذّر الاتصال بـ Ollama على {OLLAMA_HOST}.",
                "error":   f"{type(e).__name__}: {e}",
            }
    except Exception as e:
        return {"success": False, "report": f"خطأ غير متوقّع: {e}", "error": str(e)}

    msg = data.get("message", {})
    return {
        "success":       True,
        "report":        msg.get("content", "").strip() or "لا يوجد محتوى في الاستجابة.",
        "model":         chosen,
        "input_tokens":  data.get("prompt_eval_count", 0),
        "output_tokens": data.get("eval_count", 0),
        "duration_sec":  round(data.get("total_duration", 0) / 1e9, 2),
    }


def list_available_models() -> Dict[str, Any]:
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=10)
        resp.raise_for_status()
        models = [
            {
                "name":     m["name"],
                "size_mb":  round(m.get("size", 0) / 1e6, 1),
                "is_cloud": "cloud" in m.get("name", "").lower(),
            }
            for m in resp.json().get("models", [])
        ]
        return {"available": True, "models": models, "default": DEFAULT_MODEL}
    except Exception as e:
        return {"available": False, "error": str(e)}
