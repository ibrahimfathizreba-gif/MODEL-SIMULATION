"""
AI Analyzer — Connects to Claude API to produce Arabic Economic Advisory Reports.
API key is read from environment variable ANTHROPIC_API_KEY (never hardcoded).
"""
import os
from typing import Dict, Any

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


def _format_simulation_summary(results: Dict) -> str:
    """Format simulation results into a concise English summary for the prompt."""
    summary = results.get("summary", {})
    report  = results.get("report",  {})

    lines = [
        f"Simulation Scenario: {results.get('scenario', 'moderate').upper()}",
        f"Horizon: {report.get('start_year', 2026)}–{report.get('end_year', 2045)}",
        f"Automation Rate: {report.get('automation_rate', 0.05)*100:.1f}% per year",
        "",
        "=== KEY METRICS (Final Year) ===",
        f"Unemployment Rate: {report.get('final_unemployment_pct', 0):.2f}%",
        f"GDP (Trillion USD): {report.get('final_gdp_trillion', 0):.2f}",
        f"AI Adoption Level: {report.get('final_ai_adoption_pct', 0):.2f}%",
        f"Gini Inequality Index: {report.get('final_gini', 0):.4f}",
        f"Peak Unemployment: {report.get('peak_unemployment', 0):.2f}%",
        "",
        "=== SUMMARY STATISTICS ===",
    ]
    for metric, stats in summary.items():
        if isinstance(stats, dict):
            lines.append(
                f"{metric}: mean={stats.get('mean',0):.3f}, "
                f"std={stats.get('std',0):.3f}, "
                f"min={stats.get('min',0):.3f}, "
                f"max={stats.get('max',0):.3f}"
            )
    return "\n".join(lines)


def analyze_with_claude(simulation_results: Dict) -> Dict[str, Any]:
    """
    Send simulation results to Claude API.
    Returns a Professional Economic Advisory Report in ARABIC LANGUAGE ONLY.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    if not api_key:
        return {
            "success": False,
            "report": "خطأ: مفتاح API غير موجود. يرجى تعيين متغير البيئة ANTHROPIC_API_KEY.",
            "error": "ANTHROPIC_API_KEY environment variable not set.",
        }

    if not ANTHROPIC_AVAILABLE:
        return {
            "success": False,
            "report": "خطأ: مكتبة anthropic غير مثبتة.",
            "error": "anthropic library not installed.",
        }

    summary_text = _format_simulation_summary(simulation_results)

    system_prompt = (
        "أنت كبير المستشارين الاقتصاديين في منظمة العمل الدولية. "
        "مهمتك هي تحليل نتائج المحاكاة الاقتصادية وتقديم تقرير استشاري احترافي شامل. "
        "يجب أن يكون ردك كاملاً باللغة العربية الفصحى فقط، دون أي كلمة بالإنجليزية. "
        "هيكل تقريرك كالتالي:\n"
        "1. الملخص التنفيذي\n"
        "2. تحليل سوق العمل وتأثير الذكاء الاصطناعي\n"
        "3. التحليل الاقتصادي الكلي (الناتج المحلي، الأجور، عدم المساواة)\n"
        "4. التوقعات المستقبلية وسيناريوهات المخاطر\n"
        "5. التوصيات السياسية الاستراتيجية\n"
        "6. الخلاصة والرؤية المستقبلية\n"
        "اجعل التقرير مفصلاً، علمياً، ومبنياً على البيانات الواردة."
    )

    user_message = (
        f"فيما يلي نتائج محاكاة تأثير الذكاء الاصطناعي على سوق العمل للفترة 2026-2046:\n\n"
        f"{summary_text}\n\n"
        "يرجى تقديم التقرير الاستشاري الاقتصادي الشامل باللغة العربية."
    )

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-5-20251001",
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        report_text = message.content[0].text if message.content else "لا يوجد تقرير."
        return {
            "success": True,
            "report": report_text,
            "model": "claude-sonnet-4-5-20251001",
            "input_tokens":  message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
        }
    except anthropic.AuthenticationError:
        return {
            "success": False,
            "report": "خطأ في المصادقة: مفتاح API غير صالح.",
            "error": "Invalid API key.",
        }
    except Exception as e:
        return {
            "success": False,
            "report": f"خطأ في الاتصال بـ Claude API: {str(e)}",
            "error": str(e),
        }
