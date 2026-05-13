"""Lully 1661 — bilingual ZH/EN Excel SOW.

Generates raw-requirements/data/proposals/sow-website-zh-en.xlsx mirroring
the French HTML SOW. Multi-sheet workbook:

    1. Summary           - cover + headline price
    2. Scope             - included / excluded, two-column ZH+EN
    3. Phases            - 6 phases × deliverables × effort × tokens
    4. Pricing           - 4 line items + VAT calc
    5. Timeline          - 4 milestones
    6. Acceptance        - 8 criteria
    7. Terms             - 6 contractual clauses

The output is intended for client review (negotiation, procurement) and
internal cross-check against the HTML version. Keep both in sync if the
scope or pricing changes.
"""

from __future__ import annotations

from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "raw-requirements" / "data" / "proposals" / "sow-website-zh-en.xlsx"
OUT.parent.mkdir(parents=True, exist_ok=True)


# =========================================================================
# Brand colors (Lully design system)
# =========================================================================
PAPER = "F4EEDF"
PAPER_2 = "EFE6D4"
INK = "1A1613"
INK_2 = "3C342E"
STONE = "7A746B"
GOLD = "A68A3E"
EMBER = "B8563D"


# =========================================================================
# Styling helpers
# =========================================================================
THIN = Side(style="thin", color="C9C0AA")
THICK = Side(style="medium", color=INK)


def style_header(cell):
    cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    cell.fill = PatternFill("solid", fgColor=INK)
    cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    cell.border = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)


def style_title(cell):
    cell.font = Font(name="Calibri", size=18, bold=True, color=INK)
    cell.alignment = Alignment(horizontal="left", vertical="center")


def style_subtitle(cell):
    cell.font = Font(name="Calibri", size=12, italic=True, color=EMBER)
    cell.alignment = Alignment(horizontal="left", vertical="center")


def style_eyebrow(cell):
    cell.font = Font(name="Calibri", size=9, bold=True, color=GOLD)
    cell.alignment = Alignment(horizontal="left", vertical="center")


def style_label(cell):
    cell.font = Font(name="Calibri", size=9, bold=True, color=STONE)
    cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)


def style_value(cell, bold=False):
    cell.font = Font(name="Calibri", size=10, bold=bold, color=INK)
    cell.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    cell.border = Border(bottom=THIN)


def style_money(cell, bold=False, color=INK):
    cell.font = Font(name="Calibri", size=10, bold=bold, color=color)
    cell.alignment = Alignment(horizontal="right", vertical="center")
    cell.number_format = '#,##0" €"'
    cell.border = Border(bottom=THIN)


def style_total(cell):
    cell.font = Font(name="Calibri", size=12, bold=True, color=EMBER)
    cell.alignment = Alignment(horizontal="right", vertical="center")
    cell.number_format = '#,##0" €"'
    cell.border = Border(top=THICK, bottom=THIN)


def set_col_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def add_section_break(ws, row):
    """Insert a thin spacer row."""
    ws.row_dimensions[row].height = 8


# =========================================================================
# Content — bilingual
# =========================================================================
# Sheet 1 — Summary
SUMMARY = [
    # (id, zh, en, value)
    ("", "Lully 1661", "Lully 1661", ""),
    ("", "网站项目报价单", "Website Statement of Work", ""),
    ("", "v1.0 · 2026-05-13", "v1.0 · 2026-05-13", ""),
    ("", "", "", ""),
    ("0.1", "客户", "Client", "Lully 1661 — Boulangerie Renaissance · Lisbonne, Portugal"),
    ("0.2", "供应方", "Vendor", "[ 公司名/工作室名待填 / Company or studio name TBD ]"),
    ("0.3", "执行周期", "Execution period", "J+0 → J+18 工作日 (~3 周历日 / ~3 calendar weeks)"),
    ("0.4", "报价有效期", "Quote validity", "30 天 / 30 days (至 2026-06-12 / until June 12, 2026)"),
    ("0.5", "付款条件", "Payment terms",
        "50% 签约时支付 + 50% 验收时支付 · SEPA 转账 15 日内 / "
        "50% on signature + 50% on acceptance · SEPA transfer within 15 days"),
    ("0.6", "知识产权", "IP transfer",
        "代码/内容/配置归客户所有 / Code, content & config become client property at acceptance"),
    ("", "", "", ""),
    ("", "🎯 总价 / Total Price", "", ""),
    ("0.7", "不含税 (HT)", "Excl. VAT (HT)", 1800),
    ("0.8", "葡萄牙 IVA 23% (如适用)", "Portuguese VAT 23% (if applicable)", 414),
    ("0.9", "含税总价 (TTC)", "Incl. VAT (TTC)", 2214),
]

# Sheet 2 — Scope (Included / Excluded)
SCOPE_INCLUDED = [
    ("项目", "Item"),
    ("生产栈 (Next.js 15 + Tailwind v4 + Keystatic CMS + Biome)",
     "Production stack (Next.js 15 + Tailwind v4 + Keystatic CMS + Biome)"),
    ("Vercel 部署 + DNS lully1661.com 配置 + SSL 证书",
     "Vercel deployment + lully1661.com DNS configuration + SSL certificate"),
    ("11 个双语路由 PT/EN: 首页 / Menu (3 大类) / Brunch / 3 家门店 / 关于 / 节庆订单 / Lully Inside / 应聘 / 法律页 / 预约表单",
     "11 PT/EN routes: Home / Menu (3 pillars) / Brunch / 3 stores / About / Festive orders / Lully Inside / Careers / Legal / Reservations form"),
    ("品牌设计系统应用 (CSS tokens, Fraunces + Instrument Serif + Instrument Sans 字体, 动效)",
     "Brand design system applied (CSS tokens, Fraunces + Instrument Serif + Instrument Sans typography, motion)"),
    ("移动端优先响应式 (clamp typography, 汉堡菜单, 无横向溢出)",
     "Mobile-first responsive (clamp typography, hamburger menu, no horizontal overflow)"),
    ("SEO 技术: JSON-LD (Bakery + LocalBusiness + Menu + Article + BreadcrumbList), sitemap, OG tags",
     "SEO: JSON-LD (Bakery + LocalBusiness + Menu + Article + BreadcrumbList), sitemap, OG tags"),
    ("安全: CI 依赖审计 (pnpm audit), 2026-05 CVE 批量补丁 (12 漏洞), WCAG 2.1 AA 基础可访问性",
     "Security: CI dependency audit (pnpm audit), May 2026 CVE batch patch (12 vulns), WCAG 2.1 AA baseline accessibility"),
    ("Keystatic CMS 配置: 客户可在浏览器中独立编辑文字/价格/图片",
     "Keystatic CMS configured: client can edit text, prices and photos independently via browser"),
    ("交付文档: CMS 使用手册, Vercel 访问, DNS 管理指南",
     "Handover docs: CMS manual, Vercel access, DNS management guide"),
    ("3 轮迭代修改 (含在报价内)",
     "3 review iteration cycles (included in price)"),
    ("交付后 2 次 30 分钟在线培训",
     "2 × 30-min post-delivery training sessions"),
]

SCOPE_EXCLUDED = [
    ("项目", "Item", "另行报价 / Separate quote"),
    ("电商 / 购物车 / 在线支付", "E-commerce / cart / online payment", "~3 500 € HT"),
    ("预约系统 (时段日历, 失约处理, 提醒)", "Reservation system (slot calendar, no-show, reminders)", "~1 200 € HT"),
    ("专业产品摄影", "Professional product photography", "由本地摄影师承接 / Local photographer"),
    ("法语 (FR) 第三语言", "French (FR) third locale", "+300 € HT"),
    ("Glovo / UberEats 菜单同步", "Glovo / UberEats menu sync", "另议 / TBD"),
    ("自动化邮件营销 (Resend / SendGrid 序列)", "Automated email marketing (Resend / SendGrid sequences)", "+400 € HT"),
    ("高级分析 (Plausible / Posthog 定制看板)", "Advanced analytics (Plausible / Posthog custom dashboards)", "另议 / TBD"),
    ("交付后维护 (安全更新 + 1 小时支持/月)", "Post-delivery maintenance (security updates + 1 h support/month)", "80 € HT / mois"),
]

# Sheet 3 — Phases
PHASES = [
    # (n, zh_name, zh_subtitle, en_name, en_subtitle, zh_deliv, en_deliv, days, tokens)
    (1, "调研对齐", "对齐与盘点",
     "Discovery", "Alignment & inventory",
     "品牌资产盘点 (logo, 字体, 配色) · 现有内容盘点 · 范围与编辑优先级工作坊 · Vercel + GitHub + Keystatic Cloud 账号开通",
     "Brand audit (logos, fonts, palette) · existing content mapping · scope & editorial priority workshops · Vercel + GitHub + Keystatic Cloud access",
     0.5, 2),
    (2, "架构搭建", "技术初始化",
     "Architecture", "Technical setup",
     "栈初始化 (Next.js 15 + Tailwind v4 + Keystatic + Biome) · PT/EN i18n 路由 · Vercel preview-by-PR · CI (typecheck/lint/audit/build) · Keystatic schema",
     "Stack init (Next.js 15 + Tailwind v4 + Keystatic + Biome) · PT/EN i18n routing · Vercel preview-by-PR · CI (typecheck/lint/audit/build) · Keystatic schemas",
     0.5, 5),
    (3, "页面与内容", "实施",
     "Pages & content", "Implementation",
     "11 双语路由实施 · Anjos brunch 含画廊 · 3 家门店结构化 · 种子内容 (品牌调研 + 撰文) · Keystatic CMS 预填内容",
     "11 bilingual routes implemented · Anjos brunch with gallery · 3 structured store pages · seed editorial content (brand research + copywriting) · Keystatic CMS pre-populated",
     2.0, 22),
    (4, "设计系统与动效", "品牌打磨",
     "Design system & motion", "Brand polish",
     "CSS tokens 应用 (paper / ink / gold / ember) · Fraunces + Instrument Serif + Instrument Sans 字体 · 移动端响应式 (clamp typography, 汉堡菜单) · page-rise 动效, prefers-reduced-motion · hover/focus 可访问性",
     "CSS tokens applied (paper / ink / gold / ember) · Fraunces + Instrument Serif + Instrument Sans typography · mobile-first responsive (clamp typography, hamburger menu) · page-rise transitions, prefers-reduced-motion · accessible hover/focus states",
     1.0, 8),
    (5, "SEO 与安全", "加固",
     "SEO & security", "Hardening",
     "完整 JSON-LD (Bakery, LocalBusiness, Menu, Article, BreadcrumbList) · 按语言 sitemap · robots.txt · OG tags + favicon · 依赖安全审计 + 2026-05 CVE 批量补丁 (12 漏洞)",
     "Full JSON-LD (Bakery, LocalBusiness, Menu, Article, BreadcrumbList) · per-locale sitemap · robots.txt · OG tags + favicon · dependency security audit + May 2026 CVE batch (12 vulnerabilities)",
     0.5, 3),
    (6, "迭代与交付", "验收与移交",
     "Iteration & handoff", "Review & delivery",
     "3 轮客户反馈迭代 · 使用手册 · GitHub 仓库所有权移交 · 2 × 30 分钟陪同 (Keystatic CMS + 生产部署)",
     "3 cycles of client-feedback iteration · handover documentation · GitHub repo ownership transfer · 2 × 30-min training sessions (Keystatic CMS + production deployment)",
     1.0, 4),
]

# Sheet 4 — Pricing
PRICING_LINES = [
    ("人力投入", "Human effort", "5.5 人天 × 280 €/天 (混合资深/AI增强日费率)",
     "5.5 person-days × 280 €/day (mixed senior / AI-augmented rate)", 1540),
    ("AI 计算资源", "AI compute", "约 44 M tokens · Anthropic Claude (Sonnet 4.6 + Opus 4.7, 80% 缓存命中)",
     "~44 M tokens · Anthropic Claude (Sonnet 4.6 + Opus 4.7, 80% cache hit rate)", 150),
    ("托管与域名 (1 年)", "Hosting & domain (1 year)", "Vercel Free + lully1661.com 域名年续 (~12 €)",
     "Vercel Free tier + lully1661.com domain annual renewal (~12 €)", 60),
    ("迭代准备金", "Iteration buffer", "含 3 轮修改 + 2 次客户陪同会议",
     "Includes 3 review cycles + 2 client training sessions", 50),
]

# Sheet 5 — Timeline
TIMELINE = [
    ("J+0", "项目启动", "Kickoff",
     "签约 + 收到预付款", "Signature + deposit received",
     "权限共享, 30 分钟视频启动会", "Shared access, 30-min video kickoff"),
    ("J+7", "Phase 3 演示", "Phase 3 demo",
     "第 1 周末", "End of week 1",
     "Vercel preview: 11 路由骨架可见, 初步设计系统",
     "Vercel preview: 11 routes skeleton visible, preliminary design system"),
    ("J+12", "Phase 4 演示", "Phase 4 demo",
     "第 2 周中", "Mid week 2",
     "设计应用完成, 移动端响应式, 可进入内容审校",
     "Design system fully applied, mobile responsive, ready for content review"),
    ("J+18", "验收与交付", "Acceptance & handoff",
     "第 3 周末", "End of week 3",
     "lully1661.com 上线, CMS 移交, 文档交付, 收尾款",
     "lully1661.com live, CMS access transferred, docs delivered, final invoice"),
]

# Sheet 6 — Acceptance
ACCEPTANCE = [
    ("11 路由 PT + EN 全部可访问, 无 404/500",
     "11 routes accessible in both PT and EN, no 404/500 errors"),
    ("Lighthouse ≥ 90 (4 个维度) · 首页 + 3 门店页 · 移动 + 桌面",
     "Lighthouse ≥ 90 (4 axes) on home + 3 store pages, mobile + desktop"),
    ("移动 viewport 375 × 667 px 下, 11 路由无横向溢出无文字截断",
     "On mobile 375 × 667 px viewport, all 11 routes have no horizontal overflow and no truncated text"),
    ("pnpm audit --prod --audit-level=moderate 无漏洞",
     "pnpm audit --prod --audit-level=moderate reports no vulnerabilities"),
    ("客户可在 Keystatic 中独立创建/发布产品页 ≤ 5 分钟",
     "Client can independently create and publish a product page in Keystatic in ≤ 5 minutes"),
    ("lully1661.com HTTPS 上线, www → apex 重定向已配",
     "lully1661.com live on HTTPS, www → apex redirect configured"),
    ("GitHub 仓库所有权已移交至客户账号或组织",
     "GitHub repository ownership transferred to client account or organization"),
    ("JSON-LD (Bakery / LocalBusiness / Menu) 通过 Google Rich Results 验证",
     "JSON-LD (Bakery / LocalBusiness / Menu) validated by Google Rich Results test"),
]

# Sheet 7 — Terms
TERMS = [
    ("知识产权", "Intellectual property",
     "代码、原创内容、配置文件在验收时全部归客户所有。供应方保留作品集展示权 (项目名 + 截图).",
     "Code, original content, and configuration files become client property upon acceptance. Vendor retains portfolio rights (project name + screenshots)."),
    ("保修期", "Warranty",
     "验收后 30 天内, 免费修复显著缺陷 (技术 bug、客户未审定的拼写错误). 范围/内容变更不在保修内.",
     "30 calendar days after acceptance for free correction of manifest defects (technical bugs, typos not validated by client). Scope or content changes excluded from warranty."),
    ("保密义务", "Confidentiality",
     "供应方承诺不外泄项目期间获悉的客户非公开商业信息 (营收、利润率、供应商等).",
     "Vendor agrees not to disclose non-public business information of the client obtained during the engagement (revenue, margins, suppliers)."),
    ("AI 工具分包声明", "AI tooling disclosure",
     "客户接受供应方使用 Anthropic Claude 等 AI 工具协助开发. 供应方对最终交付质量负全责.",
     "Client accepts that vendor uses Anthropic Claude (and equivalent AI assistants) in producing code and content. Vendor remains solely responsible for final delivery quality."),
    ("不可抗力", "Force majeure",
     "关键基础设施供应商 (Vercel, GitHub, Anthropic) 连续中断 > 24 小时, 交付期相应顺延.",
     "Delivery deadlines suspended in case of critical infrastructure provider (Vercel, GitHub, Anthropic) downtime exceeding 24 consecutive hours."),
    ("报价有效期", "Quote validity",
     "本报价单有效至 2026-06-12. 逾期需重新评估 (范围、AI 模型或平台费用如发生变化).",
     "This quote is valid until June 12, 2026. After this date, a new estimate may be required (if scope, AI models, or platform costs change)."),
]


# =========================================================================
# Sheet builders
# =========================================================================
def build_summary(wb: Workbook) -> None:
    ws = wb.create_sheet("摘要 Summary", 0)
    set_col_widths(ws, [6, 32, 32, 60])
    ws.sheet_view.showGridLines = False
    ws.sheet_view.zoomScale = 110

    # Title row
    ws["B1"] = "Lully 1661 · 网站报价单"
    ws["B1"].font = Font(name="Calibri", size=20, bold=True, color=INK)
    ws["C1"] = "Website Statement of Work"
    ws["C1"].font = Font(name="Calibri", size=14, italic=True, color=EMBER)
    ws.row_dimensions[1].height = 32

    ws["B2"] = "v1.0 · 2026-05-13 · 1 800 € HT"
    ws["B2"].font = Font(name="Calibri", size=10, color=STONE)

    row = 4
    for sid, zh, en, val in SUMMARY:
        if not sid and not zh:
            row += 1
            continue
        if zh.startswith("🎯") or zh.startswith("Lully") or "v1" in zh:
            # Already handled in title block
            if zh.startswith("🎯"):
                ws.cell(row, 2, "总价 / Total Price").font = Font(name="Calibri", size=12, bold=True, color=GOLD)
                row += 1
            continue
        ws.cell(row, 1, sid).font = Font(name="Calibri", size=9, color=STONE)
        ws.cell(row, 2, zh)
        style_value(ws.cell(row, 2))
        ws.cell(row, 3, en)
        style_value(ws.cell(row, 3))
        ws.cell(row, 4, val if not isinstance(val, (int, float)) else val)
        if isinstance(val, (int, float)):
            ws.cell(row, 4).number_format = '#,##0" €"'
            ws.cell(row, 4).alignment = Alignment(horizontal="right", vertical="center")
            if sid == "0.9":
                ws.cell(row, 4).font = Font(name="Calibri", size=14, bold=True, color=EMBER)
            else:
                ws.cell(row, 4).font = Font(name="Calibri", size=11, bold=True, color=INK)
        else:
            style_value(ws.cell(row, 4))
        row += 1


def build_scope(wb: Workbook) -> None:
    ws = wb.create_sheet("范围 Scope")
    set_col_widths(ws, [55, 55, 22])
    ws.sheet_view.showGridLines = False

    ws["A1"] = "✅ 包含范围 / Included scope"
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color=GOLD)
    ws.merge_cells("A1:C1")

    headers = SCOPE_INCLUDED[0]
    ws["A2"] = headers[0]
    ws["B2"] = headers[1]
    style_header(ws["A2"]); style_header(ws["B2"])
    ws.merge_cells("B2:C2")

    row = 3
    for zh, en in SCOPE_INCLUDED[1:]:
        ws.cell(row, 1, zh)
        ws.cell(row, 2, en)
        ws.merge_cells(start_row=row, start_column=2, end_row=row, end_column=3)
        style_value(ws.cell(row, 1))
        style_value(ws.cell(row, 2))
        ws.row_dimensions[row].height = 32
        row += 1

    # Section break
    row += 2

    ws.cell(row, 1, "❌ 不包含 (另行报价) / Excluded scope (separate quote)").font = \
        Font(name="Calibri", size=14, bold=True, color=EMBER)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=3)
    row += 1

    hdr_zh, hdr_en, hdr_price = SCOPE_EXCLUDED[0]
    style_header(ws.cell(row, 1, hdr_zh))
    style_header(ws.cell(row, 2, hdr_en))
    style_header(ws.cell(row, 3, hdr_price))
    row += 1

    for zh, en, price in SCOPE_EXCLUDED[1:]:
        ws.cell(row, 1, zh)
        ws.cell(row, 2, en)
        ws.cell(row, 3, price)
        style_value(ws.cell(row, 1))
        style_value(ws.cell(row, 2))
        ws.cell(row, 3).font = Font(name="Calibri", size=10, color=EMBER, bold=True)
        ws.cell(row, 3).alignment = Alignment(horizontal="right", vertical="center")
        ws.cell(row, 3).border = Border(bottom=THIN)
        ws.row_dimensions[row].height = 28
        row += 1


def build_phases(wb: Workbook) -> None:
    ws = wb.create_sheet("阶段 Phases")
    set_col_widths(ws, [4, 18, 18, 40, 40, 8, 9])
    ws.sheet_view.showGridLines = False

    ws["A1"] = "项目阶段 / Project Phases"
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color=INK)
    ws.merge_cells("A1:G1")

    headers = ["#", "阶段 (ZH)", "Phase (EN)", "产出 (ZH)", "Deliverables (EN)",
               "人天 / Days", "Tokens (M)"]
    for col, h in enumerate(headers, 1):
        style_header(ws.cell(2, col, h))
    ws.row_dimensions[2].height = 28

    total_days = 0.0
    total_tokens = 0
    for n, zh_n, zh_sub, en_n, en_sub, zh_d, en_d, days, tokens in PHASES:
        row = 2 + n
        ws.cell(row, 1, n).font = Font(name="Calibri", size=11, bold=True, color=GOLD)
        ws.cell(row, 1).alignment = Alignment(horizontal="center", vertical="top")

        # Phase name + subtitle on two lines
        ws.cell(row, 2, f"{zh_n}\n{zh_sub}")
        ws.cell(row, 3, f"{en_n}\n{en_sub}")
        for c in (2, 3):
            ws.cell(row, c).font = Font(name="Calibri", size=10, bold=True, color=INK)
            ws.cell(row, c).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            ws.cell(row, c).border = Border(bottom=THIN)

        ws.cell(row, 4, zh_d)
        ws.cell(row, 5, en_d)
        for c in (4, 5):
            style_value(ws.cell(row, c))
            ws.cell(row, c).font = Font(name="Calibri", size=9, color=INK_2)

        ws.cell(row, 6, days)
        ws.cell(row, 6).number_format = '0.0" j"'
        ws.cell(row, 6).alignment = Alignment(horizontal="right", vertical="center")
        ws.cell(row, 6).border = Border(bottom=THIN)

        ws.cell(row, 7, tokens)
        ws.cell(row, 7).number_format = '~0" M"'
        ws.cell(row, 7).alignment = Alignment(horizontal="right", vertical="center")
        ws.cell(row, 7).border = Border(bottom=THIN)

        ws.row_dimensions[row].height = 70

        total_days += days
        total_tokens += tokens

    # Total row
    total_row = 2 + len(PHASES) + 1
    ws.cell(total_row, 2, "合计 / Total").font = Font(name="Calibri", size=11, bold=True, color=EMBER)
    ws.cell(total_row, 2).alignment = Alignment(horizontal="left", vertical="center")
    ws.merge_cells(start_row=total_row, start_column=2, end_row=total_row, end_column=5)
    ws.cell(total_row, 6, total_days).font = Font(name="Calibri", size=11, bold=True, color=EMBER)
    ws.cell(total_row, 6).number_format = '0.0" j"'
    ws.cell(total_row, 6).alignment = Alignment(horizontal="right", vertical="center")
    ws.cell(total_row, 6).border = Border(top=THICK)
    ws.cell(total_row, 7, total_tokens).font = Font(name="Calibri", size=11, bold=True, color=EMBER)
    ws.cell(total_row, 7).number_format = '"~"0" M"'
    ws.cell(total_row, 7).alignment = Alignment(horizontal="right", vertical="center")
    ws.cell(total_row, 7).border = Border(top=THICK)


def build_pricing(wb: Workbook) -> None:
    ws = wb.create_sheet("价格 Pricing")
    set_col_widths(ws, [22, 22, 52, 16])
    ws.sheet_view.showGridLines = False

    ws["A1"] = "价格明细 / Price Breakdown"
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color=INK)
    ws.merge_cells("A1:D1")

    headers = ["项目 (ZH)", "Line (EN)", "详情 / Detail", "金额 / Amount HT"]
    for col, h in enumerate(headers, 1):
        style_header(ws.cell(2, col, h))
    ws.row_dimensions[2].height = 28

    total_ht = 0
    for n, (zh, en, zh_d, en_d, amt) in enumerate(PRICING_LINES, 3):
        ws.cell(n, 1, zh)
        ws.cell(n, 2, en)
        ws.cell(n, 3, f"{zh_d}\n{en_d}")
        ws.cell(n, 4, amt)
        for c in (1, 2):
            style_value(ws.cell(n, c))
            ws.cell(n, c).font = Font(name="Calibri", size=10, bold=True, color=INK)
        style_value(ws.cell(n, 3))
        ws.cell(n, 3).font = Font(name="Calibri", size=9, color=INK_2)
        style_money(ws.cell(n, 4))
        ws.row_dimensions[n].height = 36
        total_ht += amt

    # Total HT
    tr = 3 + len(PRICING_LINES) + 1
    ws.cell(tr, 1, "Total HT").font = Font(name="Calibri", size=12, bold=True, italic=True, color=EMBER)
    ws.merge_cells(start_row=tr, start_column=1, end_row=tr, end_column=3)
    style_total(ws.cell(tr, 4))
    ws.cell(tr, 4, total_ht)

    # VAT
    tr += 1
    ws.cell(tr, 1, "葡萄牙增值税 23% (如适用) / Portuguese VAT 23% (if applicable)").font = \
        Font(name="Calibri", size=10, color=STONE)
    ws.merge_cells(start_row=tr, start_column=1, end_row=tr, end_column=3)
    ws.cell(tr, 4, round(total_ht * 0.23)).font = Font(name="Calibri", size=10, color=STONE)
    ws.cell(tr, 4).number_format = '"+ "#,##0" €"'
    ws.cell(tr, 4).alignment = Alignment(horizontal="right", vertical="center")

    # Total TTC
    tr += 1
    ws.cell(tr, 1, "Total TTC (含税总价 / VAT incl.)").font = Font(name="Calibri", size=11, bold=True, color=INK)
    ws.merge_cells(start_row=tr, start_column=1, end_row=tr, end_column=3)
    ws.cell(tr, 4, round(total_ht * 1.23)).font = Font(name="Calibri", size=11, bold=True, color=INK)
    ws.cell(tr, 4).number_format = '#,##0" €"'
    ws.cell(tr, 4).alignment = Alignment(horizontal="right", vertical="center")
    ws.cell(tr, 4).border = Border(top=THIN)

    # Payment terms note
    tr += 2
    ws.cell(tr, 1,
        "付款方式: 50% (900 € HT) 签约时, 50% (900 € HT) 验收时, SEPA 转账 15 日内.\n"
        "Payment terms: 50% (€900 HT) on signature, 50% (€900 HT) on acceptance, SEPA transfer within 15 days."
    ).font = Font(name="Calibri", size=9, italic=True, color=STONE)
    ws.cell(tr, 1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=tr, start_column=1, end_row=tr, end_column=4)
    ws.row_dimensions[tr].height = 32


def build_timeline(wb: Workbook) -> None:
    ws = wb.create_sheet("时间表 Timeline")
    set_col_widths(ws, [10, 22, 22, 28, 28])
    ws.sheet_view.showGridLines = False

    ws["A1"] = "项目时间表 / Project Timeline"
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color=INK)
    ws.merge_cells("A1:E1")

    headers = ["节点 / Milestone", "中文", "English", "可见产出 (ZH)", "Visible deliverable (EN)"]
    for col, h in enumerate(headers, 1):
        style_header(ws.cell(2, col, h))
    ws.row_dimensions[2].height = 28

    for n, (mi, zh, en, zh_when, en_when, zh_d, en_d) in enumerate(TIMELINE, 3):
        ws.cell(n, 1, mi).font = Font(name="Calibri", size=11, bold=True, color=GOLD)
        ws.cell(n, 1).alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(n, 2, f"{zh}\n{zh_when}")
        ws.cell(n, 3, f"{en}\n{en_when}")
        for c in (2, 3):
            ws.cell(n, c).font = Font(name="Calibri", size=10, bold=True, color=INK)
            ws.cell(n, c).alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
            ws.cell(n, c).border = Border(bottom=THIN)
        ws.cell(n, 4, zh_d)
        ws.cell(n, 5, en_d)
        for c in (4, 5):
            style_value(ws.cell(n, c))
            ws.cell(n, c).font = Font(name="Calibri", size=9, color=INK_2)
        ws.row_dimensions[n].height = 44


def build_acceptance(wb: Workbook) -> None:
    ws = wb.create_sheet("验收标准 Acceptance")
    set_col_widths(ws, [4, 60, 60])
    ws.sheet_view.showGridLines = False

    ws["A1"] = "验收标准 / Acceptance Criteria"
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color=INK)
    ws.merge_cells("A1:C1")

    note = ws["A2"]
    note.value = ("项目交付后, 客户有 5 个工作日提出明确不合规之处, 否则视为默认验收通过. \n"
                  "After delivery, client has 5 business days to raise concrete deviations; otherwise the project is deemed accepted.")
    note.font = Font(name="Calibri", size=9, italic=True, color=STONE)
    note.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:C2")
    ws.row_dimensions[2].height = 36

    headers = ["☐", "中文", "English"]
    for col, h in enumerate(headers, 1):
        style_header(ws.cell(4, col, h))
    ws.row_dimensions[4].height = 28

    for n, (zh, en) in enumerate(ACCEPTANCE, 5):
        ws.cell(n, 1, "☐").font = Font(name="Calibri", size=12, color=GOLD)
        ws.cell(n, 1).alignment = Alignment(horizontal="center", vertical="center")
        ws.cell(n, 2, zh)
        ws.cell(n, 3, en)
        for c in (2, 3):
            style_value(ws.cell(n, c))
        ws.row_dimensions[n].height = 32


def build_terms(wb: Workbook) -> None:
    ws = wb.create_sheet("条款 Terms")
    set_col_widths(ws, [22, 22, 45, 45])
    ws.sheet_view.showGridLines = False

    ws["A1"] = "条款与条件 / Terms & Conditions"
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color=INK)
    ws.merge_cells("A1:D1")

    headers = ["项目 (ZH)", "Topic (EN)", "中文", "English"]
    for col, h in enumerate(headers, 1):
        style_header(ws.cell(2, col, h))
    ws.row_dimensions[2].height = 28

    for n, (zh_t, en_t, zh_b, en_b) in enumerate(TERMS, 3):
        ws.cell(n, 1, zh_t).font = Font(name="Calibri", size=11, bold=True, color=INK)
        ws.cell(n, 1).alignment = Alignment(vertical="top")
        ws.cell(n, 1).border = Border(bottom=THIN)
        ws.cell(n, 2, en_t).font = Font(name="Calibri", size=11, bold=True, italic=True, color=EMBER)
        ws.cell(n, 2).alignment = Alignment(vertical="top")
        ws.cell(n, 2).border = Border(bottom=THIN)
        ws.cell(n, 3, zh_b)
        ws.cell(n, 4, en_b)
        for c in (3, 4):
            style_value(ws.cell(n, c))
            ws.cell(n, c).font = Font(name="Calibri", size=10, color=INK_2)
        ws.row_dimensions[n].height = 56

    # Signature block at bottom
    sig_row = 3 + len(TERMS) + 2
    ws.cell(sig_row, 1, "签字栏 / Signatures").font = Font(name="Calibri", size=12, bold=True, color=GOLD)
    ws.merge_cells(start_row=sig_row, start_column=1, end_row=sig_row, end_column=4)
    sig_row += 1
    ws.cell(sig_row, 1, "客户方 / For Lully 1661").font = Font(name="Calibri", size=10, bold=True)
    ws.cell(sig_row, 3, "供应方 / For the studio").font = Font(name="Calibri", size=10, bold=True)
    sig_row += 1
    for label_zh, label_en in [("姓名 / Name", "姓名 / Name"),
                                 ("职务 / Role", "NIF / SIRET"),
                                 ("签名 / Signature", "签名 / Signature"),
                                 ("日期 / Date", "日期 / Date")]:
        ws.cell(sig_row, 1, label_zh).font = Font(name="Calibri", size=9, color=STONE)
        ws.cell(sig_row, 2, "_____________________")
        ws.cell(sig_row, 3, label_en).font = Font(name="Calibri", size=9, color=STONE)
        ws.cell(sig_row, 4, "_____________________")
        sig_row += 1


# =========================================================================
# Assemble workbook
# =========================================================================
wb = Workbook()
# Remove the default sheet — we add our own
default = wb.active
wb.remove(default)

build_summary(wb)
build_scope(wb)
build_phases(wb)
build_pricing(wb)
build_timeline(wb)
build_acceptance(wb)
build_terms(wb)

# Set workbook-level properties
wb.properties.title = "Lully 1661 — Website SOW (ZH/EN)"
wb.properties.subject = "Statement of Work · v1.0 · 1 800 € HT"
wb.properties.creator = "lully-1661 project"

wb.save(OUT)
print(f"→ {OUT.relative_to(REPO)}: {len(wb.sheetnames)} sheets")
for name in wb.sheetnames:
    print(f"    · {name}")
