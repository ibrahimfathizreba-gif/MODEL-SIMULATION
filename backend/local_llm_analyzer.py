"""
Local LLM Analyzer — Generates Arabic Economic Advisory Reports via Ollama.
Replaces the Claude API integration with a trained, locally-routed LLM that
adapts to any simulation output.

Default model: kimi-k2.6:cloud   (1T params, best Arabic quality, fast)
Fallback:      qwen3.5:9b        (6.6 GB local, fully offline)
"""
import os
import json
import requests
from typing import Dict, Any

OLLAMA_HOST    = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
DEFAULT_MODEL  = os.environ.get("OLLAMA_MODEL", "kimi-k2.6:cloud")
FALLBACK_MODEL = "qwen3.5:9b"
REQUEST_TIMEOUT = 180  # seconds — generation can take a while


def _format_simulation_summary(results: Dict) -> str:
    """Compress simulation results into a dense English summary the LLM can reason over."""
    summary = results.get("summary", {})
    report  = results.get("report",  {})

    # Compute deltas / trends so the model has direction, not just final values
    unem_series = results.get("unemployment", [])
    gdp_series  = results.get("gdp", [])
    unem_start  = unem_series[0]  if unem_series else 0
    unem_end    = unem_series[-1] if unem_series else 0
    unem_peak   = max(unem_series) if unem_series else 0
    gdp_start   = gdp_series[0]   if gdp_series  else 0
    gdp_end     = gdp_series[-1]  if gdp_series  else 0
    gdp_growth_pct = ((gdp_end - gdp_start) / gdp_start * 100) if gdp_start else 0

    sectors = results.get("sectors", {})
    sector_final = {k: (v[-1] if v else 0) for k, v in sectors.items()}

    wages = results.get("wages", {})
    wage_low_start  = wages.get("L1_basic", [0])[0]  if wages.get("L1_basic")  else 0
    wage_low_end    = wages.get("L1_basic", [0])[-1] if wages.get("L1_basic")  else 0
    wage_high_start = wages.get("L5_expert", [0])[0]  if wages.get("L5_expert") else 0
    wage_high_end   = wages.get("L5_expert", [0])[-1] if wages.get("L5_expert") else 0

    lines = [
        f"SCENARIO: {results.get('scenario', 'moderate').upper()}",
        f"HORIZON: {report.get('start_year', 2026)} – {report.get('end_year', 2045)} "
        f"({len(results.get('years', []))} years)",
        f"AUTOMATION RATE: {report.get('automation_rate', 0.05)*100:.1f}% per year",
        "",
        "── LABOR MARKET ──",
        f"Unemployment: {unem_start:.2f}% → {unem_end:.2f}% (Δ {unem_end-unem_start:+.2f} pp)",
        f"Peak unemployment: {unem_peak:.2f}%",
        f"Final AI adoption: {report.get('final_ai_adoption_pct', 0):.1f}%",
        "",
        "── MACROECONOMY ──",
        f"GDP: ${gdp_start:.2f}T → ${gdp_end:.2f}T  ({gdp_growth_pct:+.1f}%)",
        f"Gini Index: {report.get('final_gini', 0):.4f} (final year)",
        "",
        "── WAGE GAP ──",
        f"Lowest-skill (L1): ${wage_low_start:,.0f} → ${wage_low_end:,.0f}",
        f"Highest-skill (L5): ${wage_high_start:,.0f} → ${wage_high_end:,.0f}",
        f"Wage ratio (L5/L1): {(wage_high_end/wage_low_end if wage_low_end else 0):.2f}x",
        "",
        "── SECTORS (final year, jobs) ──",
    ]
    for sec, jobs in sector_final.items():
        lines.append(f"  {sec}: {jobs/1e6:.1f}M")

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


def _call_ollama(model: str, user_message: str) -> Dict[str, Any]:
    """Call Ollama /api/chat endpoint and return the response."""
    url = f"{OLLAMA_HOST}/api/chat"
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_message},
        ],
        "stream": False,
        "options": {
            "temperature": 0.4,   # low → consistent, factual
            "top_p":       0.9,
            "num_predict": 3500,  # max output tokens (≈ 2500 Arabic words)
        },
    }
    resp = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def analyze_with_local_llm(simulation_results: Dict,
                            model: str = None) -> Dict[str, Any]:
    """
    Send simulation results to a local/cloud-routed Ollama model.
    Returns the same response shape as the previous Claude integration.
    """
    chosen_model = model or DEFAULT_MODEL
    summary_text = _format_simulation_summary(simulation_results)

    user_message = (
        f"فيما يلي نتائج المحاكاة الفعلية لتأثير الذكاء الاصطناعي على سوق العمل "
        f"للسيناريو المختار:\n\n"
        f"```\n{summary_text}\n```\n\n"
        f"يرجى تقديم التقرير الاستشاري الاقتصادي الشامل وفقاً للهيكل المحدد، "
        f"مع التركيز على الأرقام الواردة أعلاه."
    )

    # Try chosen model, fall back to qwen3.5:9b if unreachable
    try:
        data = _call_ollama(chosen_model, user_message)
    except requests.exceptions.RequestException as e:
        if chosen_model != FALLBACK_MODEL:
            try:
                data = _call_ollama(FALLBACK_MODEL, user_message)
                chosen_model = FALLBACK_MODEL + " (fallback)"
            except Exception as e2:
                return {
                    "success": False,
                    "report": f"تعذّر الاتصال بـ Ollama. تأكد أن الخدمة تعمل على {OLLAMA_HOST}.",
                    "error":  f"{type(e).__name__}: {e} | fallback: {e2}",
                }
        else:
            return {
                "success": False,
                "report": f"تعذّر الاتصال بـ Ollama على {OLLAMA_HOST}.",
                "error":  f"{type(e).__name__}: {e}",
            }
    except Exception as e:
        return {
            "success": False,
            "report": f"خطأ غير متوقّع: {str(e)}",
            "error":  str(e),
        }

    # Parse Ollama response
    message      = data.get("message", {})
    report_text  = message.get("content", "").strip() or "لا يوجد محتوى في الاستجابة."
    eval_count   = data.get("eval_count", 0)
    prompt_count = data.get("prompt_eval_count", 0)
    duration_ns  = data.get("total_duration", 0)

    return {
        "success":       True,
        "report":        report_text,
        "model":         chosen_model,
        "input_tokens":  prompt_count,
        "output_tokens": eval_count,
        "duration_sec":  round(duration_ns / 1e9, 2),
    }


def list_available_models() -> Dict[str, Any]:
    """Return the list of models installed in the local Ollama instance."""
    try:
        resp = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=10)
        resp.raise_for_status()
        data = resp.json()
        models = [
            {
                "name":   m["name"],
                "size_mb": round(m.get("size", 0) / 1e6, 1),
                "is_cloud": "cloud" in m.get("name", "").lower(),
            }
            for m in data.get("models", [])
        ]
        return {"available": True, "models": models, "default": DEFAULT_MODEL}
    except Exception as e:
        return {"available": False, "error": str(e)}
