"""Lully 1661 — pure ZH / pure EN SOW HTML generator.

Produces two standalone, single-language HTML SOWs (no mixed bilingual
layout) — one Chinese, one English. Mirrors the structure of the existing
French sow-website-fr.html but with separated content per locale.

Reads: nothing (content is inline in this script — keep in sync with the
       xlsx generator if scope or pricing changes).
Writes:
    raw-requirements/data/proposals/sow-website-zh.html
    raw-requirements/data/proposals/sow-website-en.html

Run: python3 scripts/build-sow-html.py
"""

from __future__ import annotations

from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "raw-requirements" / "data" / "proposals"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# =========================================================================
# Content data (mirror of sow-website-fr.html and build-sow-xlsx.py)
# =========================================================================
PRICING_HT = 1800
VAT_RATE = 0.23


PHASES = [
    {
        "n": 1, "days": 0.5, "tokens": 2,
        "zh_name": "调研对齐", "zh_sub": "对齐与盘点",
        "en_name": "Discovery", "en_sub": "Alignment & inventory",
        "zh_deliv": "品牌资产盘点(logo、字体、配色)· 现有内容盘点 · 范围与编辑优先级工作坊 · Vercel + GitHub + Keystatic Cloud 账号开通",
        "en_deliv": "Brand audit (logos, fonts, palette) · existing content mapping · scope and editorial-priority workshops · Vercel + GitHub + Keystatic Cloud access provisioning",
    },
    {
        "n": 2, "days": 0.5, "tokens": 5,
        "zh_name": "架构搭建", "zh_sub": "技术初始化",
        "en_name": "Architecture", "en_sub": "Technical setup",
        "zh_deliv": "技术栈初始化(Next.js 15 + Tailwind v4 + Keystatic + Biome)· PT/EN 路由配置 · Vercel preview-by-PR · CI(类型检查、lint、依赖审计、构建)· Keystatic schema",
        "en_deliv": "Stack initialisation (Next.js 15 + Tailwind v4 + Keystatic + Biome) · PT/EN i18n routing · Vercel preview-by-PR · CI (typecheck, lint, audit, build) · Keystatic schemas",
    },
    {
        "n": 3, "days": 2.0, "tokens": 22,
        "zh_name": "页面与内容", "zh_sub": "实施",
        "en_name": "Pages &amp; content", "en_sub": "Implementation",
        "zh_deliv": "11 个双语路由实施 · Anjos brunch 含画廊 · 3 家门店结构化 · 编辑种子内容(品牌调研 + 撰文)· Keystatic CMS 预填内容",
        "en_deliv": "11 bilingual routes implemented · Anjos brunch with gallery · 3 structured store pages · seed editorial content (brand research + copywriting) · Keystatic CMS pre-populated",
    },
    {
        "n": 4, "days": 1.0, "tokens": 8,
        "zh_name": "设计系统与动效", "zh_sub": "品牌打磨",
        "en_name": "Design system &amp; motion", "en_sub": "Brand polish",
        "zh_deliv": "CSS tokens 应用(paper / ink / gold / ember)· Fraunces + Instrument Serif + Instrument Sans 字体 · 移动端响应式(clamp typography、汉堡菜单)· page-rise 动效、prefers-reduced-motion · hover/focus 可访问性",
        "en_deliv": "CSS tokens applied (paper / ink / gold / ember) · Fraunces + Instrument Serif + Instrument Sans typography · mobile-first responsive (clamp typography, hamburger menu) · page-rise transitions, prefers-reduced-motion · accessible hover/focus states",
    },
    {
        "n": 5, "days": 0.5, "tokens": 3,
        "zh_name": "SEO 与安全", "zh_sub": "加固",
        "en_name": "SEO &amp; security", "en_sub": "Hardening",
        "zh_deliv": "完整 JSON-LD(Bakery、LocalBusiness、Menu、Article、BreadcrumbList)· 按语言 sitemap · robots.txt · OG tags + favicons · 依赖安全审计 + 2026-05 CVE 批量补丁(12 漏洞)",
        "en_deliv": "Full JSON-LD (Bakery, LocalBusiness, Menu, Article, BreadcrumbList) · per-locale sitemap · robots.txt · OG tags + favicons · dependency security audit + May 2026 CVE batch patch (12 vulnerabilities)",
    },
    {
        "n": 6, "days": 1.0, "tokens": 4,
        "zh_name": "迭代与交付", "zh_sub": "验收与移交",
        "en_name": "Iteration &amp; handoff", "en_sub": "Review &amp; delivery",
        "zh_deliv": "3 轮客户反馈迭代 · 使用手册 · GitHub 仓库所有权移交 · 2 × 30 分钟陪同(Keystatic CMS + 生产部署)",
        "en_deliv": "3 cycles of client-feedback iteration · handover documentation · GitHub repo ownership transfer · 2 × 30-min training sessions (Keystatic CMS + production deployment)",
    },
]


PRICING_LINES = [
    {
        "amount": 1540,
        "zh_name": "人力投入", "en_name": "Human effort",
        "zh_detail": "5.5 人天 × 280 €/天(资深 / AI 增强混合日费率)",
        "en_detail": "5.5 person-days × 280 € / day (mixed senior / AI-augmented day rate)",
    },
    {
        "amount": 150,
        "zh_name": "AI 计算资源", "en_name": "AI compute",
        "zh_detail": "约 44 M tokens · Anthropic Claude(Sonnet 4.6 + Opus 4.7,缓存命中 80%)",
        "en_detail": "~44 M tokens · Anthropic Claude (Sonnet 4.6 + Opus 4.7, 80% cache hit rate)",
    },
    {
        "amount": 60,
        "zh_name": "托管与域名(1 年)", "en_name": "Hosting &amp; domain (1 year)",
        "zh_detail": "Vercel Free tier + lully1661.com 域名年续(约 12 €)",
        "en_detail": "Vercel Free tier + lully1661.com domain annual renewal (~12 €)",
    },
    {
        "amount": 50,
        "zh_name": "迭代准备金", "en_name": "Iteration buffer",
        "zh_detail": "含 3 轮修改 + 2 次客户陪同会议",
        "en_detail": "Includes 3 review cycles + 2 client training sessions",
    },
]


INCLUDED = [
    ("生产栈:Next.js 15 App Router + Tailwind CSS v4 + Keystatic CMS + Biome",
     "Production stack: Next.js 15 App Router + Tailwind CSS v4 + Keystatic CMS + Biome"),
    ("Vercel 部署 + DNS lully1661.com 配置 + SSL 证书自动续期",
     "Vercel deployment + lully1661.com DNS configuration + auto-renewing SSL certificate"),
    ("11 个双语路由 PT/EN:首页 / Menu(三大类:面包、糕点、饮品)/ Brunch(Anjos 详细菜单 + 画廊)/ 3 家门店 / 关于 / 节庆订单 / Lully Inside / 招聘 / 法律页 / 预约表单",
     "11 PT/EN routes: Home / Menu (3 pillars: breads, pastry, drinks) / Brunch (Anjos detailed menu + gallery) / 3 store pages / About / Festive orders / Lully Inside / Careers / Legal / Reservations form"),
    ("品牌设计系统应用(CSS tokens、Fraunces + Instrument Serif + Instrument Sans 字体、subtle 动效)",
     "Brand design system applied (CSS tokens, Fraunces + Instrument Serif + Instrument Sans typography, subtle motion)"),
    ("移动端优先响应式(clamp typography、汉堡菜单、无横向溢出)",
     "Mobile-first responsive (clamp typography, hamburger menu, no horizontal overflow)"),
    ("完整 SEO 技术:JSON-LD(Bakery + LocalBusiness + Menu + Article + BreadcrumbList)、sitemap、OG tags、canonical 标签",
     "Complete technical SEO: JSON-LD (Bakery + LocalBusiness + Menu + Article + BreadcrumbList), sitemap, OG tags, canonical URLs"),
    ("安全加固:CI 依赖审计(pnpm audit)、2026-05 CVE 批量补丁(12 漏洞)、WCAG 2.1 AA 基础可访问性",
     "Security hardening: CI dependency audit (pnpm audit), May 2026 CVE batch patch (12 vulnerabilities), WCAG 2.1 AA baseline accessibility"),
    ("Keystatic CMS 完整配置:客户可在浏览器中独立编辑文字、价格、图片,无需技术介入",
     "Keystatic CMS fully configured: client can edit text, prices, and photos independently in browser — no technical intervention required"),
    ("交付文档:CMS 使用手册、Vercel 访问指南、DNS 管理说明",
     "Handover docs: CMS user manual, Vercel access guide, DNS management instructions"),
    ("含 3 轮迭代修改",
     "3 review-iteration cycles included"),
    ("交付后含 2 次 30 分钟在线培训",
     "Includes 2 × 30-min post-delivery training sessions"),
]


EXCLUDED = [
    ("电商 / 购物车 / 在线支付", "E-commerce / cart / online payment", "~3 500 € HT"),
    ("预约系统(时段日历、失约处理、提醒)", "Reservation system (slot calendar, no-show handling, reminders)", "~1 200 € HT"),
    ("专业产品摄影", "Professional product photography", "由本地摄影师承接 / Coordinated with local photographer"),
    ("法语(FR)作为第三语言", "French (FR) as third locale", "+300 € HT"),
    ("Glovo / UberEats 菜单同步与状态对接", "Glovo / UberEats menu sync and order-status integration", "另议 / TBD"),
    ("自动化邮件营销(Resend / SendGrid 序列)", "Automated email marketing (Resend / SendGrid sequences)", "+400 € HT"),
    ("高级分析(Plausible / Posthog 定制看板)", "Advanced analytics (Plausible / Posthog custom dashboards)", "另议 / TBD"),
    ("交付后维护(安全更新 + 每月 1 小时技术支持)", "Post-delivery maintenance (security updates + 1 h/month technical support)", "80 € HT / 月"),
]


TIMELINE = [
    ("J+0", "项目启动", "Project kickoff",
     "签约 + 收到预付款", "Signature received + deposit paid",
     "权限共享、30 分钟视频启动会", "Shared access provisioned, 30-min video kickoff"),
    ("J+7", "Phase 3 演示", "Phase 3 demo",
     "第 1 周末", "End of week 1",
     "Vercel preview:11 路由骨架可见、初步设计系统",
     "Vercel preview: 11-route skeleton navigable, preliminary design system"),
    ("J+12", "Phase 4 演示", "Phase 4 demo",
     "第 2 周中", "Mid-week 2",
     "设计系统完整应用、移动端响应式、可进入内容审校",
     "Design system fully applied, mobile responsive, ready for content review"),
    ("J+18", "验收与交付", "Acceptance &amp; handoff",
     "第 3 周末", "End of week 3",
     "lully1661.com 上线、CMS 移交、文档交付、收尾款",
     "lully1661.com live, CMS access transferred, docs delivered, final invoice settled"),
]


ACCEPTANCE_ZH = [
    "11 个路由的 PT + EN 版本全部可访问,无 404/500 错误",
    "首页和 3 家门店页的 Lighthouse 评分在 4 个维度上均 ≥ 90(移动 + 桌面)",
    "移动端 viewport(375 × 667 px)下,11 个路由无横向溢出、无文字截断",
    "运行 pnpm audit --prod --audit-level=moderate 不报告任何漏洞",
    "客户可在 Keystatic 中独立创建产品页并发布至上线 ≤ 5 分钟",
    "lully1661.com 通过 HTTPS 上线,www → apex 重定向已配置",
    "GitHub 仓库所有权已移交至客户账号或组织",
    "JSON-LD(Bakery / LocalBusiness / Menu)通过 Google Rich Results 验证器",
]

ACCEPTANCE_EN = [
    "All 11 routes accessible in both PT and EN, with no 404 / 500 errors",
    "Lighthouse score ≥ 90 across all 4 axes for the homepage and the 3 store pages (mobile + desktop)",
    "On mobile viewport (375 × 667 px), all 11 routes show no horizontal overflow and no truncated text",
    "pnpm audit --prod --audit-level=moderate reports no vulnerabilities",
    "Client can independently create a product page in Keystatic and publish it live in ≤ 5 minutes",
    "lully1661.com is live over HTTPS, with www → apex redirection configured",
    "GitHub repository ownership has been transferred to the client account or organisation",
    "JSON-LD (Bakery / LocalBusiness / Menu) passes the Google Rich Results validator",
]


TERMS = [
    {
        "zh_title": "知识产权", "en_title": "Intellectual property",
        "zh_body": "代码源、撰写内容与配置在验收时全部归客户所有。供应方保留作品集展示权(项目名 + 截图)。",
        "en_body": "Source code, written content, and configuration become full property of the client upon acceptance. The vendor retains portfolio rights (project name + screenshots).",
    },
    {
        "zh_title": "保修期", "en_title": "Warranty",
        "zh_body": "验收后 30 日内免费修复显著缺陷(技术 bug、客户未审定的拼写错误)。交付后的范围或内容变更不在保修内。",
        "en_body": "30 calendar days post-acceptance for free correction of manifest defects (technical bugs, typos not validated by client). Scope or content changes after delivery are excluded from warranty.",
    },
    {
        "zh_title": "保密义务", "en_title": "Confidentiality",
        "zh_body": "供应方承诺不向第三方披露在项目期间获悉的客户非公开商业信息(营收、利润率、供应商等)。",
        "en_body": "The vendor commits not to disclose to third parties any non-public business information of the client obtained during the engagement (revenue, margins, suppliers).",
    },
    {
        "zh_title": "AI 工具使用声明", "en_title": "AI tooling disclosure",
        "zh_body": "客户接受供应方在生产代码和内容时使用 Anthropic Claude 等 AI 工具。最终交付质量由供应方单独负责。",
        "en_body": "The client acknowledges that the vendor uses Anthropic Claude (and equivalent AI assistants) to produce code and content. The vendor remains solely responsible for final delivery quality.",
    },
    {
        "zh_title": "不可抗力", "en_title": "Force majeure",
        "zh_body": "关键基础设施供应商(Vercel、GitHub、Anthropic)连续中断超过 24 小时,交付期相应顺延。",
        "en_body": "Delivery deadlines are suspended in the event of any critical infrastructure provider outage (Vercel, GitHub, Anthropic) exceeding 24 consecutive hours.",
    },
    {
        "zh_title": "报价有效期", "en_title": "Quote validity",
        "zh_body": "本报价单有效至 2026 年 6 月 12 日。逾期需重新评估(若范围、AI 模型或平台费用发生变化)。",
        "en_body": "This quote is valid until June 12, 2026. After this date, a fresh estimate may be required (if scope, AI models, or platform costs have changed).",
    },
]


STRINGS = {
    "zh": {
        "lang": "zh-Hans",
        "doc_title": "Lully 1661 网站项目报价单",
        "doc_subtitle": "v1.0 · 2026-05-13",
        "brand_em": "1661",
        "topbar_id": "网站项目报价单 · v1.0 · 2026-05-13",

        # Section 0 (Cover)
        "eyebrow_cover": "网站项目报价单",
        "title_pre": "Lully 1661 双语官网,",
        "title_em": "三周交付。",
        "lead": "Lully 1661 烘焙坊(里斯本三家门店)官网整体翻新:Next.js 架构、品牌设计系统、Keystatic CMS 交予客户运营、Vercel 上线。固定包干价,AI 增强工作流交付。",
        "label_client": "客户",
        "value_client": "Lully 1661 — Boulangerie Renaissance<br>葡萄牙里斯本",
        "label_vendor": "供应方",
        "value_vendor": "[ 公司名 / 工作室名 ]<br><em>联系方式待填</em>",
        "label_period": "执行周期",
        "value_period": "J+0 → J+18 工作日<br>约 3 周历日",
        "label_validity": "报价有效期",
        "value_validity": "30 天(自 2026-05-13 起)<br>至 2026-06-12 截止",
        "price_label": "包干价格",
        "price_amount_em": "HT",
        "price_sub_1": "葡萄牙 IVA 23% 视情况另加(= 2 214 € TTC)。",
        "price_sub_2": "50% 签约时支付 · 50% 验收时支付。",

        # Section 1
        "eyebrow_context": "1 · 项目背景",
        "context_title_pre": "一家在重新书写自己的",
        "context_title_em": "法语烘焙坊。",
        "context_body_1": "Lully 1661 — 里斯本起家,三家门店(Anjos、Campo de Ourique、Beato)— 以 <em>Boulangerie Renaissance</em>(文艺复兴烘焙坊)为品牌定位,法语糕点词汇、土色 / 墨色 / 金色 / 余烬色调色板、Fraunces + Instrument Serif + Instrument Sans 字体。官网需要承载这套品牌身份,同时面向里斯本本地双语公众(葡萄牙语 + 英语)和法语圈游客。",
        "context_body_2": "官网承担三个角色:",
        "context_role_1": "<strong>数字名片</strong> — 在 \"里斯本 / 烘焙 / brunch\" 等 SEO 关键词上获得能见度,吸引法语游客。",
        "context_role_2": "<strong>信息枢纽</strong> — 三家门店信息(地址、营业时间、氛围)、菜单、Anjos brunch。",
        "context_role_3": "<strong>季节性沟通支撑</strong> — 节庆订单(圣诞、复活节、圣若昂节)、<em>Lully Inside</em>(幕后、团队)、招聘表单。",
        "context_body_3": "电商和精确预约系统在本报价中<strong>明确不含</strong>(详见第 3 节)— v1 官网保持品牌展示型。",

        # Section 2
        "eyebrow_scope": "2 · 服务范围",
        "scope_title_pre": "11 个路由、两种语言、",
        "scope_title_em": "一个设计系统。",
        "scope_included_title": "包含在包干内",
        "scope_excluded_title": "不包含(另行报价)",
        "scope_amount_header": "另行金额",

        # Section 3
        "eyebrow_method": "3 · 方法论",
        "method_title_pre": "AI 增强工作流,",
        "method_title_em": "成本透明。",
        "method_lead": "本项目按 Anthropic Claude Code 团队公开的工程工作流再造方法论交付:瓶颈已从 \"敲代码\" 转移到 \"验证、设计与客户对齐\"。价格结构反映这一现实。",
        "method_body": "<strong>具体表现为:</strong>",
        "method_p1": "<strong>即时规划(Just-in-time planning)</strong> — 不在第一次提交前写 50 页详尽 spec。架构与设计选择通过可点击的 PR 和原型即时验证。",
        "method_p2": "<strong>代码胜辩论</strong> — 与其用文字争论方案,直接生成多个版本让客户在浏览器中对比。讨论基于真实渲染,不是描述。",
        "method_p3": "<strong>验证左移(shift-left)</strong> — 类型检查、lint、依赖审计、构建在每次提交触发 CI 自动跑,在人工评审前抓出回退。",
        "method_p4": "<strong>计算成本与时间成本分离</strong> — 项目期间消耗的 AI tokens(~44 M)作为独立预算行项透明列出,占总价不到 10%。",
        "method_source": "来源:Fiona Fung(Anthropic Claude Code),《Bottlenecks have shifted》,Anthropic 2026 大会 — ",

        "method_econ": "经济影响:此规模的官网(11 双语路由 + 设计系统 + CMS + 完整 SEO + 生产部署)在传统外包模式下需要 15-25 人天(里斯本平均时薪计 6 000-12 000 € HT)。AI 增强模式下,同等范围 5.5 人天 + ~150 € 计算资源,即 <strong>1 800 € HT 包干</strong>。",

        # Section 4
        "eyebrow_phases": "4 · 阶段与产出",
        "phases_title_pre": "五个阶段,",
        "phases_title_em": "五人天半。",
        "phases_lead": "每个阶段产出客户可审阅的具体交付物。Token 数为高估值(Anthropic Claude Sonnet 4.6 + Opus 4.7,2026 年公开价格)。",
        "phases_header_phase": "阶段",
        "phases_header_deliv": "交付物",
        "phases_header_effort": "人天",
        "phases_header_tokens": "Tokens(~M)",
        "phases_total": "合计",
        "phases_total_caption": "5 阶段 + 交付,端到端完成",

        # Section 5
        "eyebrow_price": "5 · 价格",
        "price_title_pre": "1 800 € HT 包干,",
        "price_title_em": "一价到底。",
        "price_lead": "下表将 <strong>1 800 € HT</strong> 拆解为 AI 增强项目的两条成本轴:人力时间(人天)与计算资源(tokens),外加年度托管。",
        "price_header_line": "项目",
        "price_header_detail": "详情",
        "price_header_amount": "金额(HT)",
        "price_total_ht": "Total HT",
        "price_vat_label": "葡萄牙 IVA 23%(如适用)",
        "price_vat_detail": "另加,视客户增值税身份决定",
        "price_total_ttc": "Total TTC(含税)",
        "price_terms": "付款方式:签约时 50%(900 € HT)、验收时 50%(900 € HT)。SEPA 转账 15 日内。银行手续费由客户承担。",

        # Section 6
        "eyebrow_timeline": "6 · 时间表",
        "timeline_title_pre": "三周,",
        "timeline_title_em": "四个节点。",
        "timeline_header_milestone": "节点",
        "timeline_header_when": "时间",
        "timeline_header_visible": "可见交付物",
        "timeline_note": "工期依赖客户在 48 小时工作日内对验证问题给出答复。任何节点验证延迟超过 5 工作日可顺延后续节点。",

        # Section 7
        "eyebrow_acceptance": "7 · 验收标准",
        "acceptance_title_pre": "客观验收,",
        "acceptance_title_em": "30 分钟可核对。",
        "acceptance_note": "项目交付后,客户有 5 个工作日就具体偏离提出书面意见。逾期未提则视为默认验收通过、可结算尾款。",

        # Section 8
        "eyebrow_terms": "8 · 条款与条件",
        "terms_title": "知识产权、保修、",
        "terms_title_em": "有效期。",

        # Section 9
        "eyebrow_sign": "9 · 接受",
        "sign_title": "双方签署。",
        "sign_body": "下方签字栏,或一封明确引用本文档(v1.0,2026-05-13 发布,金额 1 800 € HT)的接受邮件,即视为正式下单,触发预付款发票开具。",
        "sign_client": "客户方 / Lully 1661",
        "sign_vendor": "供应方 / 工作室",
        "sign_field_name": "姓名:",
        "sign_field_role": "职务:",
        "sign_field_nif": "SIRET / NIF 编号:",
        "sign_field_date": "日期:",
        "sign_field_signature": "签名:",

        "footer_credit": "Lully 1661 · 网站项目报价单",
        "footer_meta": "v1.0 · 2026-05-13 · 1 800 € HT · 有效期 30 天",
    },

    "en": {
        "lang": "en",
        "doc_title": "Lully 1661 — Website Statement of Work",
        "doc_subtitle": "v1.0 · May 13, 2026",
        "brand_em": "1661",
        "topbar_id": "Statement of Work · v1.0 · May 13, 2026",

        "eyebrow_cover": "Statement of work — Website",
        "title_pre": "Lully 1661 bilingual website,",
        "title_em": "ready in three weeks.",
        "lead": "Complete website rebuild for the Lully 1661 bakery (three houses in Lisbon): Next.js architecture, in-house design system, Keystatic CMS handed off to the client, deployed on Vercel. Fixed-price engagement, delivered in an AI-augmented workflow.",
        "label_client": "Prepared for",
        "value_client": "Lully 1661 — Boulangerie Renaissance<br>Lisbon, Portugal",
        "label_vendor": "Prepared by",
        "value_vendor": "[ Studio / company name ]<br><em>contact to be filled in</em>",
        "label_period": "Execution window",
        "value_period": "J+0 to J+18 business days<br>~3 calendar weeks",
        "label_validity": "Quote validity",
        "value_validity": "30 days from May 13, 2026<br>until June 12, 2026",
        "price_label": "Fixed-price quote",
        "price_amount_em": "HT",
        "price_sub_1": "Portuguese VAT 23% added if applicable (= € 2 214 TTC).",
        "price_sub_2": "50% on signature · 50% on acceptance.",

        "eyebrow_context": "1 · Context &amp; objectives",
        "context_title_pre": "A bakery rewriting itself",
        "context_title_em": "in French.",
        "context_body_1": "Lully 1661 — founded in Lisbon, three houses (Anjos, Campo de Ourique, Beato) — carries a <em>Boulangerie Renaissance</em> brand identity: French pastry vocabulary, paper / ink / gold / ember palette, Fraunces + Instrument Serif + Instrument Sans typography. The website must embody this identity while remaining functional for a bilingual Lisbon audience (Portuguese + English) and for francophone tourism.",
        "context_body_2": "Three expected roles:",
        "context_role_1": "<strong>Digital business card</strong> — SEO visibility on Lisbon / bakery / brunch queries, appeal to French-speaking tourism.",
        "context_role_2": "<strong>Information hub</strong> — three store pages (addresses, opening hours, atmosphere), menu, Anjos brunch.",
        "context_role_3": "<strong>Seasonal communication support</strong> — festive orders (Christmas, Easter, São João), <em>Lully Inside</em> (behind-the-scenes, team), recruitment form.",
        "context_body_3": "E-commerce and a slot-based reservation system are <strong>explicitly out of scope</strong> in this proposal (see section 3) — the v1 site remains a brochure / showcase.",

        "eyebrow_scope": "2 · Scope of work",
        "scope_title_pre": "Eleven routes, two languages,",
        "scope_title_em": "one design system.",
        "scope_included_title": "Included in the fixed price",
        "scope_excluded_title": "Out of scope (separate quote)",
        "scope_amount_header": "Separate amount",

        "eyebrow_method": "3 · Methodology",
        "method_title_pre": "AI-augmented workflow,",
        "method_title_em": "transparent costs.",
        "method_lead": "This project is delivered per the engineering-workflow re-engineering framework published by Anthropic's Claude Code team: the bottleneck has shifted from code-writing to validation, design, and client alignment. The pricing structure reflects this reality.",
        "method_body": "<strong>In practice, that means:</strong>",
        "method_p1": "<strong>Just-in-time planning</strong> — no exhaustive 50-page spec before the first commit. Architecture and design choices are validated as we go, via clickable PRs and navigable prototypes.",
        "method_p2": "<strong>Code wins debates</strong> — instead of arguing about options in writing, multiple variants are generated and compared in-browser. The discussion is based on real rendering, not descriptions.",
        "method_p3": "<strong>Shift-left verification</strong> — typecheck, lint, dependency audit, and build run on every commit in CI. Regressions are caught before human review.",
        "method_p4": "<strong>Compute cost separated from time cost</strong> — AI tokens consumed during the project (~44 M) appear as a transparent budget line, distinct from human time. They represent less than 10% of the fixed price.",
        "method_source": "Source: Fiona Fung (Anthropic, Claude Code), <em>“Bottlenecks have shifted”</em>, Anthropic 2026 conference — ",

        "method_econ": "Economic consequence: a website of this calibre (11 bilingual routes, design system, CMS, full SEO, production deployment) historically required 15–25 person-days in agency mode (€ 6 000–12 000 HT at average Lisbon rates). The AI-augmented fixed price delivers the same scope in 5.5 person-days + ~€ 150 of compute, i.e. <strong>€ 1 800 HT all-inclusive</strong>.",

        "eyebrow_phases": "4 · Phases &amp; deliverables",
        "phases_title_pre": "Five phases,",
        "phases_title_em": "five and a half person-days.",
        "phases_lead": "Each phase produces a concrete deliverable the client can review. Token figures are high-side estimates (Anthropic Claude Sonnet 4.6 + Opus 4.7, 2026 public pricing).",
        "phases_header_phase": "Phase",
        "phases_header_deliv": "Deliverables",
        "phases_header_effort": "Effort",
        "phases_header_tokens": "Tokens (~M)",
        "phases_total": "Total",
        "phases_total_caption": "5 phases + handoff, end-to-end delivery",

        "eyebrow_price": "5 · Pricing",
        "price_title_pre": "Fixed price € 1 800 HT,",
        "price_title_em": "all-inclusive.",
        "price_lead": "The table below decomposes the <strong>€ 1 800 HT</strong> along the two cost axes of an AI-augmented project: human time (person-days) and compute (AI tokens), plus annual hosting.",
        "price_header_line": "Line",
        "price_header_detail": "Detail",
        "price_header_amount": "Amount (HT)",
        "price_total_ht": "Total HT",
        "price_vat_label": "Portuguese VAT 23% (if applicable)",
        "price_vat_detail": "in addition, depending on client's VAT status",
        "price_total_ttc": "Total TTC (VAT incl.)",
        "price_terms": "Payment terms: 50% (€ 900 HT) on signature, 50% (€ 900 HT) on final acceptance. SEPA transfer within 15 days. Any bank fees are payable by the client.",

        "eyebrow_timeline": "6 · Timeline",
        "timeline_title_pre": "Three weeks,",
        "timeline_title_em": "four milestones.",
        "timeline_header_milestone": "Milestone",
        "timeline_header_when": "When",
        "timeline_header_visible": "Visible deliverable",
        "timeline_note": "Timeline is conditioned on a client response time of 48 business hours on validation questions. Any validation delay over 5 business days on a milestone may shift the following milestone accordingly.",

        "eyebrow_acceptance": "7 · Acceptance criteria",
        "acceptance_title_pre": "Objective acceptance,",
        "acceptance_title_em": "verifiable in 30 minutes.",
        "acceptance_note": "After delivery, the client has 5 business days to raise any concrete deviations in writing. Past that, the project is tacitly accepted and the balance is due.",

        "eyebrow_terms": "8 · Terms &amp; conditions",
        "terms_title": "IP, warranty,",
        "terms_title_em": "validity.",

        "eyebrow_sign": "9 · Acceptance",
        "sign_title": "Signature of the parties.",
        "sign_body": "A signature in the boxes below, or an email acceptance explicitly referencing this document (v1.0 of May 13, 2026, amount € 1 800 HT), constitutes a firm order and triggers issuance of the deposit invoice.",
        "sign_client": "For Lully 1661",
        "sign_vendor": "For the studio",
        "sign_field_name": "Name:",
        "sign_field_role": "Role:",
        "sign_field_nif": "SIRET / NIF:",
        "sign_field_date": "Date:",
        "sign_field_signature": "Signature:",

        "footer_credit": "Lully 1661 · website statement of work",
        "footer_meta": "v1.0 · May 13, 2026 · € 1 800 HT · valid for 30 days",
    },
}


# =========================================================================
# Shared CSS (loaded per-locale; Chinese version swaps Latin display fonts
# for Noto Serif SC + Noto Sans SC so CJK glyphs render cleanly)
# =========================================================================
def css_for(locale: str) -> str:
    is_zh = locale == "zh"
    display = "'Noto Serif SC', 'Fraunces', Georgia, serif" if is_zh else "'Fraunces', Georgia, 'Times New Roman', serif"
    accent = "'Noto Serif SC', 'Instrument Serif', Georgia, serif" if is_zh else "'Instrument Serif', Georgia, serif"
    body = "'Noto Sans SC', 'Instrument Sans', system-ui, sans-serif" if is_zh else "'Instrument Sans', system-ui, -apple-system, sans-serif"
    return f"""
:root {{
  --paper: #f4eedf;
  --paper-2: #efe6d4;
  --paper-3: #e9dfc7;
  --ink: #1a1613;
  --ink-2: #3c342e;
  --ink-3: #5a5048;
  --stone: #7a746b;
  --gold: #a68a3e;
  --gold-2: #c2a04a;
  --ember: #b8563d;
  --rule: rgba(26, 22, 19, 0.14);
  --rule-strong: rgba(26, 22, 19, 0.28);
  --font-display: {display};
  --font-accent: {accent};
  --font-body: {body};
}}
* {{ box-sizing: border-box; }}
html, body {{ background: var(--paper); margin: 0; }}
body {{
  color: var(--ink);
  font-family: var(--font-body);
  font-size: 15px;
  line-height: 1.7;
  -webkit-font-smoothing: antialiased;
}}
.shell {{ max-width: 880px; margin: 0 auto; padding: 0 32px; }}
@media (max-width: 720px) {{ .shell {{ padding: 0 20px; }} }}

header.topbar {{
  padding: 22px 32px;
  border-bottom: 1px solid var(--rule);
  display: flex; justify-content: space-between; align-items: baseline;
}}
header.topbar .brand {{
  font-family: var(--font-display);
  font-size: 22px;
  letter-spacing: 0.04em;
  font-weight: 400;
}}
header.topbar .brand em {{ font-style: italic; color: var(--ember); font-family: var(--font-accent); }}
header.topbar .doc-id {{
  font-size: 11px;
  letter-spacing: 0.18em;
  color: var(--stone);
}}

section {{ padding: 72px 0; border-bottom: 1px solid var(--rule); }}
section.compact {{ padding: 48px 0; }}

.eyebrow {{
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
  font-weight: 500;
  margin-bottom: 16px;
  display: inline-block;
}}
h1.display, h2.display, h3.display {{
  font-family: var(--font-display);
  font-weight: 400;
  color: var(--ink);
  letter-spacing: -0.01em;
  margin: 0 0 16px;
  line-height: 1.1;
}}
h1.display {{ font-size: clamp(32px, 4.8vw, 46px); margin-bottom: 22px; }}
h2.display {{ font-size: clamp(24px, 3.4vw, 32px); margin-bottom: 18px; }}
h3.display {{ font-size: 20px; margin-bottom: 10px; }}
h1.display em, h2.display em, h3.display em {{
  font-family: var(--font-accent);
  font-style: italic;
  color: var(--ember);
}}

p.lead {{ font-size: 17px; color: var(--ink-2); max-width: 64ch; margin: 0 0 16px; }}
p {{ color: var(--ink-2); margin: 0 0 12px; max-width: 72ch; }}
ul, ol {{ color: var(--ink-2); padding-left: 22px; }}
ul li, ol li {{ margin-bottom: 6px; }}

.cover-meta {{
  margin-top: 40px;
  padding-top: 28px;
  border-top: 1px solid var(--rule);
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 22px 56px;
  max-width: 720px;
}}
@media (max-width: 600px) {{ .cover-meta {{ grid-template-columns: 1fr; gap: 14px; }} }}
.cover-meta .label {{
  display: block;
  font-size: 10px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--stone);
  margin-bottom: 5px;
}}
.cover-meta .value {{ color: var(--ink); font-size: 15px; }}
.cover-meta .value em {{ font-family: var(--font-accent); font-style: italic; color: var(--ember); }}

.price-headline {{
  margin-top: 40px;
  padding: 28px 32px;
  background: var(--paper-2);
  border-left: 4px solid var(--gold);
  display: flex;
  flex-direction: column;
  gap: 6px;
}}
.price-headline .price-label {{
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--gold);
}}
.price-headline .price-amount {{
  font-family: var(--font-display);
  font-size: clamp(36px, 5vw, 44px);
  line-height: 1;
  color: var(--ink);
  font-variant-numeric: tabular-nums;
}}
.price-headline .price-amount em {{
  font-family: var(--font-accent);
  font-style: italic;
  color: var(--ember);
  font-size: 0.6em;
}}
.price-headline .price-sub {{
  font-family: var(--font-accent);
  font-style: italic;
  color: var(--stone);
  font-size: 15px;
}}

table.data, table.phases, table.pricing {{
  width: 100%;
  border-collapse: collapse;
  margin: 22px 0;
  font-variant-numeric: tabular-nums;
  font-size: 14px;
}}
table th, table td {{
  padding: 12px 14px;
  text-align: left;
  border-bottom: 1px solid var(--rule);
  vertical-align: top;
}}
table th {{
  font-size: 10px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--stone);
  font-weight: 500;
  border-bottom: 1px solid var(--rule-strong);
}}
table.pricing td:last-child, table.pricing th:last-child,
table.phases td.num, table.phases th.num {{ text-align: right; }}
table.pricing tr.total td {{
  font-weight: 600;
  font-size: 16px;
  color: var(--ink);
  border-top: 1px solid var(--rule-strong);
  border-bottom: 0;
  padding-top: 16px;
}}
table.pricing tr.total td:first-child {{
  font-family: var(--font-accent);
  font-style: italic;
  color: var(--ember);
}}
table.pricing tr.ttc td {{
  font-size: 13px;
  color: var(--stone);
  border-bottom: 0;
  padding-top: 4px;
}}

.scope-grid {{
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 36px;
  margin-top: 18px;
}}
@media (max-width: 720px) {{ .scope-grid {{ grid-template-columns: 1fr; gap: 24px; }} }}
.scope-box {{
  padding: 22px 24px;
  border: 1px solid var(--rule);
  background: var(--paper);
}}
.scope-box.included {{ border-left: 3px solid var(--gold); }}
.scope-box.excluded {{ border-left: 3px solid var(--ember); }}
.scope-box h4 {{
  margin: 0 0 12px;
  font-family: var(--font-body);
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--ink);
}}
.scope-box ul {{ margin: 0; padding-left: 18px; font-size: 13.5px; color: var(--ink-2); }}
.scope-box li {{ margin-bottom: 6px; }}
.scope-box .scope-amount {{ display: inline-block; color: var(--ember); font-weight: 600; }}

.methodology {{
  background: var(--paper-2);
  border-left: 3px solid var(--gold);
  padding: 24px 28px;
  margin: 24px 0;
}}
.methodology .source {{
  display: block;
  margin-top: 12px;
  font-family: var(--font-accent);
  font-style: italic;
  color: var(--stone);
  font-size: 13px;
}}
.methodology .source a {{ color: var(--gold); text-decoration: none; }}

ul.acceptance {{ list-style: none; padding: 0; margin: 16px 0 0; }}
ul.acceptance li {{
  padding: 10px 0 10px 28px;
  border-bottom: 1px solid var(--rule);
  position: relative;
  color: var(--ink-2);
  font-size: 14px;
}}
ul.acceptance li::before {{
  content: "☐";
  position: absolute;
  left: 0;
  top: 8px;
  color: var(--gold);
  font-size: 16px;
}}

.signature-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  margin-top: 30px;
}}
@media (max-width: 600px) {{ .signature-grid {{ grid-template-columns: 1fr; gap: 40px; }} }}
.sig-block {{ border-top: 1px solid var(--ink); padding-top: 10px; }}
.sig-block .role {{
  font-size: 11px;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--stone);
  margin-bottom: 4px;
}}
.sig-block .name {{ color: var(--ink); font-size: 15px; }}
.sig-block .field {{
  margin-top: 8px;
  font-size: 12px;
  color: var(--stone);
  font-family: var(--font-accent);
  font-style: italic;
}}

footer.site {{
  background: var(--ink);
  color: var(--paper);
  padding: 40px 32px;
}}
footer.site .shell {{ display: flex; justify-content: space-between; align-items: baseline; gap: 16px; flex-wrap: wrap; }}
footer.site .brand {{
  font-family: var(--font-display);
  font-size: 18px;
}}
footer.site .brand em {{ color: var(--gold-2); font-family: var(--font-accent); font-style: italic; }}
footer.site .meta {{
  font-size: 11px;
  letter-spacing: 0.18em;
  color: rgba(244, 238, 223, 0.5);
}}

@media print {{
  body {{ background: white; font-size: 11pt; }}
  header.topbar, footer.site {{ background: white; color: black; }}
  section {{ padding: 24px 0; break-inside: avoid-page; }}
  h1.display, h2.display, h3.display {{ break-after: avoid; }}
  table, .methodology, .scope-box, .price-headline {{ break-inside: avoid; }}
  .price-headline {{ background: #f7f3e8; }}
}}
"""


# =========================================================================
# Render
# =========================================================================
def render(locale: str) -> str:
    s = STRINGS[locale]
    is_zh = locale == "zh"
    # Google Fonts URL
    if is_zh:
        gfonts = (
            "https://fonts.googleapis.com/css2"
            "?family=Noto+Sans+SC:wght@400;500;700"
            "&family=Noto+Serif+SC:wght@400;500;700"
            "&family=Instrument+Serif:ital@0;1"
            "&family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900"
            "&display=swap"
        )
    else:
        gfonts = (
            "https://fonts.googleapis.com/css2"
            "?family=Fraunces:ital,opsz,wght@0,9..144,300..900;1,9..144,300..900"
            "&family=Instrument+Serif:ital@0;1"
            "&family=Instrument+Sans:ital,wght@0,400..700;1,400..700"
            "&display=swap"
        )

    # Phases rows
    phase_rows = []
    total_days = 0.0
    total_tokens = 0
    for p in PHASES:
        name = p[f"{locale[:2]}_name"]
        sub = p[f"{locale[:2]}_sub"]
        deliv = p[f"{locale[:2]}_deliv"]
        days_label = f"{p['days']:.1f} {'天' if is_zh else 'd'}"
        phase_rows.append(f"""
        <tr>
          <td><strong>{p['n']} · {name}</strong><br>
              <em style="font-family: var(--font-accent); color: var(--stone);">{sub}</em></td>
          <td>{deliv}</td>
          <td class="num">{days_label}</td>
          <td class="num">~{p['tokens']}</td>
        </tr>""")
        total_days += p['days']
        total_tokens += p['tokens']
    total_days_label = f"{total_days:.1f} {'天' if is_zh else 'd'}"
    phase_rows_html = "".join(phase_rows)

    # Pricing rows
    pricing_rows = []
    total_ht = 0
    for line in PRICING_LINES:
        pricing_rows.append(f"""
        <tr>
          <td>{line[f"{locale[:2]}_name"]}</td>
          <td>{line[f"{locale[:2]}_detail"]}</td>
          <td>{line['amount']:,} €</td>
        </tr>""")
        total_ht += line['amount']
    pricing_rows_html = "".join(pricing_rows)
    vat_amount = round(total_ht * VAT_RATE)
    total_ttc = total_ht + vat_amount

    # Included / excluded scope
    inc_items = []
    exc_items = []
    if is_zh:
        for it in INCLUDED:
            inc_items.append(f"<li>{it[0]}</li>")
        for zh, en, price in EXCLUDED:
            exc_items.append(f"<li>{zh} · <span class='scope-amount'>{price}</span></li>")
    else:
        for it in INCLUDED:
            inc_items.append(f"<li>{it[1]}</li>")
        for zh, en, price in EXCLUDED:
            exc_items.append(f"<li>{en} · <span class='scope-amount'>{price}</span></li>")

    # Timeline rows
    timeline_rows = []
    for mi, zh_n, en_n, zh_w, en_w, zh_d, en_d in TIMELINE:
        if is_zh:
            timeline_rows.append(f"""
        <tr>
          <td><strong>{mi}</strong></td>
          <td><strong>{zh_n}</strong><br><span style="color: var(--stone); font-size: 13px;">{zh_w}</span></td>
          <td>{zh_d}</td>
        </tr>""")
        else:
            timeline_rows.append(f"""
        <tr>
          <td><strong>{mi}</strong></td>
          <td><strong>{en_n}</strong><br><span style="color: var(--stone); font-size: 13px;">{en_w}</span></td>
          <td>{en_d}</td>
        </tr>""")
    timeline_rows_html = "".join(timeline_rows)

    # Acceptance items
    acceptance_list = ACCEPTANCE_ZH if is_zh else ACCEPTANCE_EN
    acceptance_html = "".join(f"<li>{item}</li>" for item in acceptance_list)

    # Terms list
    terms_html = []
    for t in TERMS:
        title = t[f"{locale[:2]}_title"]
        body = t[f"{locale[:2]}_body"]
        terms_html.append(f"<li><strong>{title}.</strong> {body}</li>")
    terms_html = "".join(terms_html)

    # Source link inline
    source_url = '<a href="https://www.youtube.com/watch?v=igO8iyca2_g">youtube.com/watch?v=igO8iyca2_g</a>'

    return f"""<!doctype html>
<html lang="{s['lang']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{s['doc_title']}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="{gfonts}">
  <style>{css_for(locale)}</style>
</head>
<body>
  <header class="topbar">
    <div class="brand">lully <em>{s['brand_em']}</em></div>
    <div class="doc-id">{s['topbar_id']}</div>
  </header>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['eyebrow_cover']}</div>
      <h1 class="display">{s['title_pre']} <em>{s['title_em']}</em></h1>
      <p class="lead">{s['lead']}</p>

      <div class="cover-meta">
        <div><span class="label">{s['label_client']}</span><span class="value">{s['value_client']}</span></div>
        <div><span class="label">{s['label_vendor']}</span><span class="value">{s['value_vendor']}</span></div>
        <div><span class="label">{s['label_period']}</span><span class="value">{s['value_period']}</span></div>
        <div><span class="label">{s['label_validity']}</span><span class="value">{s['value_validity']}</span></div>
      </div>

      <div class="price-headline">
        <span class="price-label">{s['price_label']}</span>
        <span class="price-amount">{total_ht:,} € <em>{s['price_amount_em']}</em></span>
        <span class="price-sub">{s['price_sub_1']}<br>{s['price_sub_2']}</span>
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['eyebrow_context']}</div>
      <h2 class="display">{s['context_title_pre']} <em>{s['context_title_em']}</em></h2>
      <p>{s['context_body_1']}</p>
      <p>{s['context_body_2']}</p>
      <ul>
        <li>{s['context_role_1']}</li>
        <li>{s['context_role_2']}</li>
        <li>{s['context_role_3']}</li>
      </ul>
      <p>{s['context_body_3']}</p>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['eyebrow_scope']}</div>
      <h2 class="display">{s['scope_title_pre']} <em>{s['scope_title_em']}</em></h2>
      <div class="scope-grid">
        <div class="scope-box included">
          <h4>{s['scope_included_title']}</h4>
          <ul>{"".join(inc_items)}</ul>
        </div>
        <div class="scope-box excluded">
          <h4>{s['scope_excluded_title']}</h4>
          <ul>{"".join(exc_items)}</ul>
        </div>
      </div>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['eyebrow_method']}</div>
      <h2 class="display">{s['method_title_pre']} <em>{s['method_title_em']}</em></h2>
      <p class="lead">{s['method_lead']}</p>

      <div class="methodology">
        <p style="margin:0">{s['method_body']}</p>
        <ul style="margin: 12px 0 0;">
          <li>{s['method_p1']}</li>
          <li>{s['method_p2']}</li>
          <li>{s['method_p3']}</li>
          <li>{s['method_p4']}</li>
        </ul>
        <span class="source">{s['method_source']}{source_url}</span>
      </div>

      <p>{s['method_econ']}</p>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['eyebrow_phases']}</div>
      <h2 class="display">{s['phases_title_pre']} <em>{s['phases_title_em']}</em></h2>
      <p class="lead">{s['phases_lead']}</p>
      <table class="phases">
        <thead>
          <tr>
            <th>{s['phases_header_phase']}</th>
            <th>{s['phases_header_deliv']}</th>
            <th class="num">{s['phases_header_effort']}</th>
            <th class="num">{s['phases_header_tokens']}</th>
          </tr>
        </thead>
        <tbody>
          {phase_rows_html}
          <tr style="background: var(--paper-2);">
            <td><strong>{s['phases_total']}</strong></td>
            <td><em style="font-family: var(--font-accent); color: var(--ember);">{s['phases_total_caption']}</em></td>
            <td class="num"><strong>{total_days_label}</strong></td>
            <td class="num"><strong>~{total_tokens} M</strong></td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['eyebrow_price']}</div>
      <h2 class="display">{s['price_title_pre']} <em>{s['price_title_em']}</em></h2>
      <p class="lead">{s['price_lead']}</p>
      <table class="pricing">
        <thead>
          <tr>
            <th>{s['price_header_line']}</th>
            <th>{s['price_header_detail']}</th>
            <th>{s['price_header_amount']}</th>
          </tr>
        </thead>
        <tbody>
          {pricing_rows_html}
          <tr class="total">
            <td>{s['price_total_ht']}</td>
            <td></td>
            <td>{total_ht:,} €</td>
          </tr>
          <tr class="ttc">
            <td>{s['price_vat_label']}</td>
            <td>{s['price_vat_detail']}</td>
            <td>+ {vat_amount:,} €</td>
          </tr>
          <tr class="ttc">
            <td>{s['price_total_ttc']}</td>
            <td></td>
            <td>{total_ttc:,} €</td>
          </tr>
        </tbody>
      </table>
      <p style="font-size: 13px; color: var(--stone); font-family: var(--font-accent); font-style: italic; margin-top: 16px;">{s['price_terms']}</p>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['eyebrow_timeline']}</div>
      <h2 class="display">{s['timeline_title_pre']} <em>{s['timeline_title_em']}</em></h2>
      <table class="data">
        <thead>
          <tr>
            <th>{s['timeline_header_milestone']}</th>
            <th>{s['timeline_header_when']}</th>
            <th>{s['timeline_header_visible']}</th>
          </tr>
        </thead>
        <tbody>
          {timeline_rows_html}
        </tbody>
      </table>
      <p style="font-size: 13px; color: var(--stone); font-family: var(--font-accent); font-style: italic;">{s['timeline_note']}</p>
    </div>
  </section>

  <section>
    <div class="shell">
      <div class="eyebrow">{s['eyebrow_acceptance']}</div>
      <h2 class="display">{s['acceptance_title_pre']} <em>{s['acceptance_title_em']}</em></h2>
      <p>{s['acceptance_note']}</p>
      <ul class="acceptance">{acceptance_html}</ul>
    </div>
  </section>

  <section class="compact">
    <div class="shell">
      <div class="eyebrow">{s['eyebrow_terms']}</div>
      <h3 class="display">{s['terms_title']} <em>{s['terms_title_em']}</em></h3>
      <ul style="font-size: 14px;">{terms_html}</ul>
    </div>
  </section>

  <section class="compact">
    <div class="shell">
      <div class="eyebrow">{s['eyebrow_sign']}</div>
      <h3 class="display">{s['sign_title']}</h3>
      <p>{s['sign_body']}</p>
      <div class="signature-grid">
        <div class="sig-block">
          <div class="role">{s['sign_client']}</div>
          <div class="name">{s['sign_field_name']} __________________________</div>
          <div class="field">{s['sign_field_role']} __________________________</div>
          <div class="field">{s['sign_field_date']} __________ · {s['sign_field_signature']} __________</div>
        </div>
        <div class="sig-block">
          <div class="role">{s['sign_vendor']}</div>
          <div class="name">{s['sign_field_name']} __________________________</div>
          <div class="field">{s['sign_field_nif']} __________________________</div>
          <div class="field">{s['sign_field_date']} __________ · {s['sign_field_signature']} __________</div>
        </div>
      </div>
    </div>
  </section>

  <footer class="site">
    <div class="shell">
      <div class="brand">lully <em>{s['brand_em']}</em> · {s['footer_credit']}</div>
      <div class="meta">{s['footer_meta']}</div>
    </div>
  </footer>
</body>
</html>
"""


# =========================================================================
# Write outputs
# =========================================================================
for locale in ("zh", "en"):
    path = OUT_DIR / f"sow-website-{locale}.html"
    path.write_text(render(locale), encoding="utf-8")
    print(f"→ {path.relative_to(REPO)}")
