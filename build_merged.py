#!/usr/bin/env python3
"""Build merged CRM: combines crm.html (Jobs) + consulting.html (Consulting) into deploy/index.html"""

import re

# Read source files
with open('crm.html', 'r') as f:
    jobs_lines = f.readlines()

with open('consulting.html', 'r') as f:
    consult_lines = f.readlines()

# --- Extract sections ---

# Jobs CRM: CSS lines 7-320, HTML body 321-826, JS 827-1804
jobs_css = ''.join(jobs_lines[6:319])  # lines 7-320 (0-indexed: 6-319)
jobs_html_body = ''.join(jobs_lines[321:824])  # lines 322-825 (body content, skip passcode+app wrapper)
jobs_js = ''.join(jobs_lines[826:1800])  # lines 827-1801

# Consulting CRM: CSS lines 7-174, HTML body 175-622, JS 623-1174
consult_css = ''.join(consult_lines[6:173])  # lines 7-174
consult_html_body = ''.join(consult_lines[176:620])  # lines 177-621
consult_js = ''.join(consult_lines[622:1173])  # lines 623-1174

# --- Extract sub-sections from HTML ---

# Jobs HTML: extract inner content of #app (skip passcode screen, #app wrapper)
# Lines 338-825 in original = the #app div content
# We need: top-bar (339-355), crm-view (357-379), research-view (381-633), cv-view (635-678), guide-view (680-823)
jobs_topbar_start = next(i for i, l in enumerate(jobs_lines) if '<div class="top-bar">' in l and i > 330)
jobs_app_end = next(i for i, l in enumerate(jobs_lines) if l.strip() == '</div>' and i > 820 and i < 830)
jobs_inner_html = ''.join(jobs_lines[jobs_topbar_start:jobs_app_end])

# Consulting HTML: extract inner content of #app
consult_topbar_start = next(i for i, l in enumerate(consult_lines) if '<div class="top-bar">' in l and i > 190)
consult_app_end = next(i for i, l in enumerate(consult_lines) if l.strip() == '</div>' and i > 618 and i < 625)
consult_inner_html = ''.join(consult_lines[consult_topbar_start:consult_app_end])

# --- Transform Jobs HTML ---
# Prefix element IDs
jobs_id_map = {
    'crm-view': 'jobs-crm-view',
    'research-view': 'jobs-research-view',
    'cv-view': 'jobs-cv-view',
    'guide-view': 'jobs-guide-view',
    'stats-bar': 'jobs-stats-bar',
    'contacts-container': 'jobs-contacts-container',
    'save-indicator': 'jobs-save-indicator',
    'toggle-research-btn': 'jobs-toggle-research-btn',
    'toggle-cv-btn': 'jobs-toggle-cv-btn',
    'toggle-guide-btn': 'jobs-toggle-guide-btn',
    'cv-variant-select': 'jobs-cv-variant-select',
    'cv-dynamic': 'jobs-cv-dynamic',
    'cv-content': 'jobs-cv-content',
    'cl-contact-select': 'jobs-cl-contact-select',
    'cl-output': 'jobs-cl-output',
    'import-file': 'jobs-import-file',
    'import-excel-file': 'jobs-import-excel-file',
}

for old_id, new_id in jobs_id_map.items():
    jobs_inner_html = jobs_inner_html.replace(f'id="{old_id}"', f'id="{new_id}"')
    jobs_inner_html = jobs_inner_html.replace(f"id='{old_id}'", f"id='{new_id}'")
    jobs_inner_html = jobs_inner_html.replace(f'for="{old_id}"', f'for="{new_id}"')
    jobs_inner_html = jobs_inner_html.replace(f"for='{old_id}'", f"for='{new_id}'")

# Remove theme-toggle from Jobs (will be shared in mode bar)
jobs_inner_html = re.sub(r'<button id="theme-toggle"[^>]*>.*?</button>\s*', '', jobs_inner_html)

# Remove "Consulting CRM" button
jobs_inner_html = re.sub(r"<button onclick=\"window\.location\.href='consulting\.html'\"[^>]*>.*?</button>\s*", '', jobs_inner_html)

# Update Lock button
jobs_inner_html = jobs_inner_html.replace(
    "localStorage.removeItem('alessio_crm_auth');document.getElementById('passcode-screen').style.display='flex';document.getElementById('app').style.display='none';",
    "lockApp();"
)

# Update onclick handlers to use JobsCRM namespace
jobs_onclick_map = {
    'onclick="exportData()"': 'onclick="JobsCRM.exportData()"',
    'onclick="exportExcel()"': 'onclick="JobsCRM.exportExcel()"',
    'onchange="importData(event)"': 'onchange="JobsCRM.importData(event)"',
    'onchange="importExcel(event)"': 'onchange="JobsCRM.importExcel(event)"',
    'onclick="toggleResearch()"': 'onclick="JobsCRM.toggleResearch()"',
    'onclick="showCV()"': 'onclick="JobsCRM.showCV()"',
    'onclick="showGuide()"': 'onclick="JobsCRM.showGuide()"',
    'onclick="showCRM()"': 'onclick="JobsCRM.showCRM()"',
    'onclick="toggleFilter(this)"': 'onclick="JobsCRM.toggleFilter(this)"',
    'oninput="renderContacts()"': 'oninput="JobsCRM.renderContacts()"',
    'onclick="downloadPDF()"': 'onclick="JobsCRM.downloadPDF()"',
    'onclick="downloadWord()"': 'onclick="JobsCRM.downloadWord()"',
    'onchange="switchCVVariant(this.value)"': 'onchange="JobsCRM.switchCVVariant(this.value)"',
    'onchange="generateCoverLetter()"': 'onchange="JobsCRM.generateCoverLetter()"',
    'onclick="copyCoverLetter()"': 'onclick="JobsCRM.copyCoverLetter()"',
    'onclick="downloadCoverLetterWord()"': 'onclick="JobsCRM.downloadCoverLetterWord()"',
}
for old, new in jobs_onclick_map.items():
    jobs_inner_html = jobs_inner_html.replace(old, new)

# --- Transform Consulting HTML ---
consult_id_map = {
    'crm-view': 'consult-crm-view',
    'research-view': 'consult-research-view',
    'donors-view': 'consult-donors-view',
    'cv-view': 'consult-cv-view',
    'guide-view': 'consult-guide-view',
    'stats-bar': 'consult-stats-bar',
    'contacts-container': 'consult-contacts-container',
    'save-indicator': 'consult-save-indicator',
    'toggle-research-btn': 'consult-toggle-research-btn',
    'toggle-donors-btn': 'consult-toggle-donors-btn',
    'toggle-cv-btn': 'consult-toggle-cv-btn',
    'toggle-guide-btn': 'consult-toggle-guide-btn',
    'cv-variant-select': 'consult-cv-variant-select',
    'cv-dynamic': 'consult-cv-dynamic',
    'cv-content': 'consult-cv-content',
    'cl-contact-select': 'consult-cl-contact-select',
    'cl-output': 'consult-cl-output',
    'import-file': 'consult-import-file',
}

for old_id, new_id in consult_id_map.items():
    consult_inner_html = consult_inner_html.replace(f'id="{old_id}"', f'id="{new_id}"')
    consult_inner_html = consult_inner_html.replace(f"id='{old_id}'", f"id='{new_id}'")
    consult_inner_html = consult_inner_html.replace(f'for="{old_id}"', f'for="{new_id}"')
    consult_inner_html = consult_inner_html.replace(f"for='{old_id}'", f"for='{new_id}'")

# Remove theme-toggle from Consulting
consult_inner_html = re.sub(r'<button id="theme-toggle"[^>]*>.*?</button>\s*', '', consult_inner_html)

# Remove "Jobs CRM" button
consult_inner_html = re.sub(r"<button onclick=\"window\.location\.href='crm\.html'\"[^>]*>.*?</button>\s*", '', consult_inner_html)

# Update Lock button
consult_inner_html = consult_inner_html.replace(
    "localStorage.removeItem('alessio_consult_auth');document.getElementById('passcode-screen').style.display='flex';document.getElementById('app').style.display='none';",
    "lockApp();"
)

# Update onclick handlers to use ConsultCRM namespace
consult_onclick_map = {
    'onclick="exportData()"': 'onclick="ConsultCRM.exportData()"',
    'onclick="toggleResearch()"': 'onclick="ConsultCRM.toggleResearch()"',
    'onclick="toggleDonors()"': 'onclick="ConsultCRM.toggleDonors()"',
    'onclick="toggleCV()"': 'onclick="ConsultCRM.toggleCV()"',
    'onclick="toggleGuide()"': 'onclick="ConsultCRM.toggleGuide()"',
    'onclick="showCRM()"': 'onclick="ConsultCRM.showCRM()"',
    'onclick="toggleFilter(this)"': 'onclick="ConsultCRM.toggleFilter(this)"',
    'oninput="renderContacts()"': 'oninput="ConsultCRM.renderContacts()"',
    'onclick="downloadPDF()"': 'onclick="ConsultCRM.downloadPDF()"',
    'onclick="downloadWord()"': 'onclick="ConsultCRM.downloadWord()"',
    'onchange="switchCVVariant(this.value)"': 'onchange="ConsultCRM.switchCVVariant(this.value)"',
    'onchange="generateEOI()"': 'onchange="ConsultCRM.generateEOI()"',
    'onclick="copyEOI()"': 'onclick="ConsultCRM.copyEOI()"',
    'onclick="downloadEOIWord()"': 'onclick="ConsultCRM.downloadEOIWord()"',
    'onclick="toggleDonor(this)"': 'onclick="ConsultCRM.toggleDonor(this)"',
    'onchange="importData(event)"': 'onchange="ConsultCRM.importData(event)"',
}
for old, new in consult_onclick_map.items():
    consult_inner_html = consult_inner_html.replace(old, new)

# --- Extract Jobs JS sections ---
# We need to extract: cvVariants, cvSharedIT, cvShared, cvPrintCSS, contacts, and all functions
# Then wrap them in a JobsCRM namespace

# Find the JS content between <script> and </script>
jobs_js_content = ''.join(jobs_lines[827:1800])  # after <script> tag, before </script>

# Extract contacts array (lines 1393-1476 approx)
contacts_start = next(i for i, l in enumerate(jobs_lines) if 'const contacts = [' in l)
# Find matching ] by tracking brackets
bracket_count = 0
contacts_end = contacts_start
for i in range(contacts_start, len(jobs_lines)):
    bracket_count += jobs_lines[i].count('[') - jobs_lines[i].count(']')
    if bracket_count == 0 and i > contacts_start:
        contacts_end = i + 1
        break

jobs_contacts = ''.join(jobs_lines[contacts_start:contacts_end])

# Extract cvVariants (lines 905-1016)
cv_start = next(i for i, l in enumerate(jobs_lines) if 'const cvVariants = {' in l)
cv_end = cv_start
bracket_count = 0
for i in range(cv_start, len(jobs_lines)):
    bracket_count += jobs_lines[i].count('{') - jobs_lines[i].count('}')
    if bracket_count == 0 and i > cv_start:
        cv_end = i + 1
        break
jobs_cvVariants = ''.join(jobs_lines[cv_start:cv_end])

# Extract cvSharedIT (lines 1018-1111)
cvit_start = next(i for i, l in enumerate(jobs_lines) if 'const cvSharedIT = {' in l)
cvit_end = cvit_start
bracket_count = 0
for i in range(cvit_start, len(jobs_lines)):
    bracket_count += jobs_lines[i].count('{') - jobs_lines[i].count('}')
    if bracket_count == 0 and i > cvit_start:
        cvit_end = i + 1
        break
jobs_cvSharedIT = ''.join(jobs_lines[cvit_start:cvit_end])

# Extract cvShared (lines 1113-1206)
cvs_start = next(i for i, l in enumerate(jobs_lines) if 'const cvShared = {' in l and i > 1100)
cvs_end = cvs_start
bracket_count = 0
for i in range(cvs_start, len(jobs_lines)):
    bracket_count += jobs_lines[i].count('{') - jobs_lines[i].count('}')
    if bracket_count == 0 and i > cvs_start:
        cvs_end = i + 1
        break
jobs_cvShared = ''.join(jobs_lines[cvs_start:cvs_end])

# --- Extract Consulting JS sections ---
consult_js_content = ''.join(consult_lines[623:1173])

# Extract consulting contacts
c_contacts_start = next(i for i, l in enumerate(consult_lines) if 'const contacts = [' in l)
bracket_count = 0
c_contacts_end = c_contacts_start
for i in range(c_contacts_start, len(consult_lines)):
    bracket_count += consult_lines[i].count('[') - consult_lines[i].count(']')
    if bracket_count == 0 and i > c_contacts_start:
        c_contacts_end = i + 1
        break
consult_contacts = ''.join(consult_lines[c_contacts_start:c_contacts_end])

# Extract consulting cvVariants
c_cv_start = next(i for i, l in enumerate(consult_lines) if 'const cvVariants = {' in l)
c_cv_end = c_cv_start
bracket_count = 0
for i in range(c_cv_start, len(consult_lines)):
    bracket_count += consult_lines[i].count('{') - consult_lines[i].count('}')
    if bracket_count == 0 and i > c_cv_start:
        c_cv_end = i + 1
        break
consult_cvVariants = ''.join(consult_lines[c_cv_start:c_cv_end])

# Extract consulting cvShared
c_cvs_start = next(i for i, l in enumerate(consult_lines) if 'const cvShared = {' in l)
c_cvs_end = c_cvs_start
bracket_count = 0
for i in range(c_cvs_start, len(consult_lines)):
    bracket_count += consult_lines[i].count('{') - consult_lines[i].count('}')
    if bracket_count == 0 and i > c_cvs_start:
        c_cvs_end = i + 1
        break
consult_cvShared = ''.join(consult_lines[c_cvs_start:c_cvs_end])

# Extract consulting eoiFields
eoi_start = next(i for i, l in enumerate(consult_lines) if 'const eoiFields = {' in l)
eoi_end = eoi_start
bracket_count = 0
for i in range(eoi_start, len(consult_lines)):
    bracket_count += consult_lines[i].count('{') - consult_lines[i].count('}')
    if bracket_count == 0 and i > eoi_start:
        eoi_end = i + 1
        break
consult_eoiFields = ''.join(consult_lines[eoi_start:eoi_end])

# --- Build consulting-specific CSS (only the parts that differ from Jobs) ---
consult_specific_css = """
/* === CONSULTING CRM SPECIFIC === */
#consult-app .cat-badge{display:inline-block;padding:3px 10px;border-radius:12px;font-size:10px;font-weight:700;color:#fff;text-transform:uppercase;letter-spacing:.5px;}
#consult-app .cat-badge.un{background:#3b82f6;}
#consult-app .cat-badge.mdb{background:#8b5cf6;}
#consult-app .cat-badge.eu{background:#06b6d4;}
#consult-app .cat-badge.bilateral{background:#14b8a6;}
#consult-app .cat-badge.firm{background:#f59e0b;color:#000;}
#consult-app .cat-badge.platform{background:#10b981;}
#consult-app .reg-select{padding:4px 8px;font-size:11px;border-radius:6px;border:1px solid var(--border);background:var(--bg);color:var(--text);cursor:pointer;outline:none;width:140px;}
#consult-app .reg-select.not-registered{border-color:var(--border);}
#consult-app .reg-select.profile-created{border-color:var(--warning);color:var(--warning);}
#consult-app .reg-select.application-sent{border-color:var(--accent);color:var(--accent);}
#consult-app .reg-select.registered{border-color:var(--success);color:var(--success);}
#consult-app .reg-select.shortlisted{border-color:var(--purple);color:var(--purple);}
#consult-app .reg-select.active-engagement{border-color:#34d399;color:#34d399;}
#consult-app .col-header{grid-template-columns:40px 1fr 150px 90px 80px 140px 40px;}
#consult-app .contact-main{grid-template-columns:40px 1fr 150px 90px 80px 140px 40px;}
#consult-app .location-col{font-size:11px;color:var(--text-muted);}
#consult-app .cat-group-header{padding:12px 24px;font-size:14px;font-weight:700;text-transform:uppercase;letter-spacing:1px;border-bottom:2px solid var(--border);margin-top:8px;display:flex;align-items:center;gap:10px;}
#consult-app .cat-dot{width:12px;height:12px;border-radius:50%;display:inline-block;}
#consult-app .filter-btn.cat-un.active{background:#3b82f6;border-color:#3b82f6;}
#consult-app .filter-btn.cat-mdb.active{background:#8b5cf6;border-color:#8b5cf6;}
#consult-app .filter-btn.cat-eu.active{background:#06b6d4;border-color:#06b6d4;}
#consult-app .filter-btn.cat-firm.active{background:#f59e0b;border-color:#f59e0b;}
#consult-app .filter-btn.cat-platform.active{background:#10b981;border-color:#10b981;}

/* Donor table */
.donor-table{width:100%;border-collapse:collapse;font-size:13px;background:var(--card-bg);border-radius:12px;overflow:hidden;}
.donor-table th{padding:12px 16px;border-bottom:1px solid var(--border);color:var(--accent);text-align:left;background:var(--bg);}
.donor-table td{padding:10px 16px;border-bottom:1px solid var(--border);}
.donor-table a{color:var(--accent);text-decoration:none;}
.donor-table a:hover{text-decoration:underline;}
.donor-table tr.donor-row{cursor:pointer;transition:background .2s;}
.donor-table tr.donor-row:hover{background:var(--card-hover);}
.donor-table tr.donor-row td:first-child::before{content:'\\25B8 ';color:var(--text-muted);font-size:11px;}
.donor-table tr.donor-row.open td:first-child::before{content:'\\25BE ';}
.donor-table tr.donor-detail{display:none;}
.donor-table tr.donor-detail.open{display:table-row;}
.donor-table tr.donor-detail td{padding:14px 20px 14px 36px;background:var(--bg);border-bottom:1px solid var(--border);}
.donor-brief{font-size:12px;line-height:1.7;color:var(--text-muted);}
.donor-brief strong{color:var(--text);font-weight:600;}
.donor-brief .brief-tag{display:inline-block;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600;margin-right:6px;margin-bottom:4px;}
.donor-brief .tag-budget{background:rgba(52,211,153,0.15);color:var(--success);}
.donor-brief .tag-hire{background:rgba(168,85,247,0.15);color:var(--purple);}
.donor-brief .tag-focus{background:rgba(59,130,246,0.15);color:var(--accent);}
"""

# --- Build the mode bar CSS ---
mode_bar_css = """
/* === MODE BAR === */
#mode-bar {
  display:flex; align-items:center; justify-content:center; gap:0;
  background:var(--card-bg); border-bottom:2px solid var(--border);
  position:sticky; top:0; z-index:200; padding:0;
}
#mode-bar .mode-tab {
  flex:1; padding:14px 24px; font-size:14px; font-weight:600;
  text-align:center; cursor:pointer; border:none;
  background:transparent; color:var(--text-muted);
  transition:all 0.2s; border-bottom:3px solid transparent;
  font-family:inherit;
}
#mode-bar .mode-tab:hover { color:var(--text); background:var(--card-hover); }
#mode-bar .mode-tab.active-jobs { color:var(--accent); border-bottom-color:var(--accent); background:var(--bg); }
#mode-bar .mode-tab.active-consult { color:var(--purple); border-bottom-color:var(--purple); background:var(--bg); }
#mode-bar .mode-actions {
  display:flex; align-items:center; gap:8px; padding:0 16px;
}
#mode-bar .mode-actions button {
  padding:6px 12px; font-size:12px; border-radius:6px; border:1px solid var(--border);
  background:transparent; color:var(--text-muted); cursor:pointer; transition:all 0.2s;
  font-family:inherit;
}
#mode-bar .mode-actions button:hover { border-color:var(--accent); color:var(--text); }
"""

# Fix the top-bar z-index in both apps (below mode bar)
topbar_fix_css = """
#jobs-app .top-bar, #consult-app .top-bar { position:sticky; top:51px; z-index:100; }
"""

# --- Build the output ---
output = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Alessio CRM</title>
<style>
:root {{
  --d-color: #CC0000;
  --i-color: #E68A00;
  --s-color: #008000;
  --c-color: #0000CC;
  --bg: #0f1117;
  --card-bg: #1a1d27;
  --card-hover: #22263a;
  --border: #2a2e3f;
  --text: #e1e4ed;
  --text-muted: #8b90a0;
  --accent: #6c8aff;
  --accent-hover: #8ba3ff;
  --success: #34d399;
  --warning: #fbbf24;
  --danger: #f87171;
  --purple: #a855f7;
}}
body.light {{
  --bg: #f5f7fa;
  --card-bg: #ffffff;
  --card-hover: #f0f2f5;
  --border: #d1d5db;
  --text: #1a1a2e;
  --text-muted: #6b7280;
  --accent: #4f6df5;
  --accent-hover: #3b5de7;
  --success: #16a34a;
  --warning: #d97706;
  --danger: #dc2626;
  --purple: #9333ea;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: 'Segoe UI', system-ui, -apple-system, sans-serif; background: var(--bg); color: var(--text); min-height:100vh; transition: background 0.3s, color 0.3s; }}

/* === PASSCODE SCREEN === */
#passcode-screen {{
  display:flex; align-items:center; justify-content:center; min-height:100vh;
  background: linear-gradient(135deg, var(--bg) 0%, var(--card-bg) 50%, var(--bg) 100%);
}}
.passcode-box {{
  text-align:center; padding:48px; border-radius:16px;
  background: var(--card-bg); border:1px solid var(--border);
  box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}}
.passcode-box h1 {{ font-size:24px; margin-bottom:8px; color:var(--accent); }}
.passcode-box p {{ color:var(--text-muted); margin-bottom:24px; font-size:14px; }}
.passcode-box input {{
  padding:12px 20px; font-size:16px; border-radius:8px; border:1px solid var(--border);
  background:var(--bg); color:var(--text); width:260px; text-align:center;
  outline:none; transition:border-color 0.2s;
}}
.passcode-box input:focus {{ border-color:var(--accent); }}
.passcode-box button {{
  display:block; margin:16px auto 0; padding:12px 40px; font-size:14px; font-weight:600;
  border-radius:8px; border:none; background:var(--accent); color:#fff; cursor:pointer;
  transition: background 0.2s;
}}
.passcode-box button:hover {{ background:var(--accent-hover); }}
.passcode-error {{ color:var(--danger); margin-top:12px; font-size:13px; display:none; }}

{mode_bar_css}

/* === MAIN APP === */
#app {{ display:none; }}
.top-bar {{
  display:flex; align-items:center; justify-content:space-between;
  padding:16px 24px; border-bottom:1px solid var(--border);
  background: var(--card-bg); position:sticky; top:51px; z-index:100;
}}
.top-bar h1 {{ font-size:18px; }}
.top-bar h1 span {{ color:var(--accent); }}
#consult-app .top-bar h1 span {{ color:var(--purple); }}
.top-bar-actions {{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; }}
.top-bar-actions button, .top-bar-actions label, .top-bar-actions a {{
  padding:8px 14px; font-size:12px; border-radius:6px; border:1px solid var(--border);
  background:var(--bg); color:var(--text-muted); cursor:pointer; transition:all 0.2s;
  text-decoration:none; display:inline-block;
}}
.top-bar-actions button:hover, .top-bar-actions label:hover, .top-bar-actions a:hover {{
  border-color:var(--accent); color:var(--text);
}}
#jobs-import-file, #jobs-import-excel-file, #consult-import-file {{ display:none; }}

/* Stats bar */
.stats-bar {{ display:flex; gap:12px; padding:16px 24px; flex-wrap:wrap; }}
.stat-card {{
  padding:12px 20px; border-radius:10px; background:var(--card-bg);
  border:1px solid var(--border); min-width:120px; text-align:center;
}}
.stat-card .num {{ font-size:24px; font-weight:700; }}
.stat-card .label {{ font-size:11px; color:var(--text-muted); text-transform:uppercase; letter-spacing:0.5px; }}

/* Filters */
.filters {{ display:flex; gap:8px; padding:0 24px 16px; flex-wrap:wrap; align-items:center; }}
.filter-btn {{
  padding:6px 14px; font-size:12px; border-radius:20px; border:1px solid var(--border);
  background:transparent; color:var(--text-muted); cursor:pointer; transition:all 0.2s;
}}
.filter-btn:hover {{ border-color:var(--accent); color:var(--text); }}
.filter-btn.active {{ background:var(--accent); border-color:var(--accent); color:#fff; }}
#jobs-app .filter-btn.disc-d.active {{ background:var(--d-color); border-color:var(--d-color); }}
#jobs-app .filter-btn.disc-i.active {{ background:var(--i-color); border-color:var(--i-color); }}
#jobs-app .filter-btn.disc-s.active {{ background:var(--s-color); border-color:var(--s-color); }}
#jobs-app .filter-btn.disc-c.active {{ background:var(--c-color); border-color:var(--c-color); }}
.search-input {{
  padding:6px 14px; font-size:12px; border-radius:20px; border:1px solid var(--border);
  background:var(--bg); color:var(--text); outline:none; width:200px;
}}
.search-input:focus {{ border-color:var(--accent); }}

/* DISC Group headers */
.disc-group-header {{
  padding:12px 24px; font-size:14px; font-weight:700; text-transform:uppercase;
  letter-spacing:1px; border-bottom:2px solid var(--border); margin-top:8px;
  display:flex; align-items:center; gap:10px;
}}
.disc-group-header .disc-dot {{ width:12px; height:12px; border-radius:50%; display:inline-block; }}

/* Contact cards */
.contact-card {{ margin:0 24px; border-bottom:1px solid var(--border); transition: background 0.15s; }}
.contact-card:hover {{ background: var(--card-hover); }}
#jobs-app .contact-main {{
  display:grid; grid-template-columns: 40px 1fr 140px 180px 100px 90px 70px 140px 40px;
  align-items:center; padding:12px 0; gap:8px; cursor:pointer;
}}
#consult-app .contact-main {{
  display:grid; grid-template-columns: 40px 1fr 150px 90px 80px 140px 40px;
  align-items:center; padding:12px 0; gap:8px; cursor:pointer;
}}
.priority-badge {{
  width:28px; height:28px; border-radius:50%; display:flex; align-items:center;
  justify-content:center; font-size:11px; font-weight:700; background:var(--border); color:var(--text-muted);
}}
.priority-badge.top {{ background:var(--accent); color:#fff; }}
#consult-app .priority-badge.top {{ background:var(--purple); color:#fff; }}
.contact-info h3 {{ font-size:13px; font-weight:600; }}
.contact-info p {{ font-size:11px; color:var(--text-muted); }}
.company-col {{ font-size:12px; color:var(--text-muted); }}
.disc-badge {{
  display:inline-block; padding:3px 10px; border-radius:12px; font-size:11px;
  font-weight:700; color:#fff;
}}
.disc-badge.d {{ background:var(--d-color); }}
.disc-badge.i {{ background:var(--i-color); }}
.disc-badge.s {{ background:var(--s-color); }}
.disc-badge.c {{ background:var(--c-color); }}
.remote-badge {{
  font-size:11px; padding:3px 8px; border-radius:10px; background:var(--border); color:var(--text-muted);
}}
.remote-badge.yes {{ background:#064e3b; color:#34d399; }}
.remote-badge.hybrid {{ background:#713f12; color:#fbbf24; }}
.remote-badge.partial {{ background:#713f12; color:#fbbf24; }}
.remote-badge.no {{ background:#7f1d1d; color:#f87171; }}
.remote-badge-label {{ display:block; font-size:8px; text-transform:uppercase; letter-spacing:0.5px; opacity:0.7; line-height:1; }}
.remote-badge-value {{ display:block; font-weight:700; line-height:1.2; }}
.linkedin-link {{ font-size:11px; color:var(--accent); text-decoration:none; }}
.linkedin-link:hover {{ text-decoration:underline; }}
.status-select {{
  padding:4px 8px; font-size:11px; border-radius:6px; border:1px solid var(--border);
  background:var(--bg); color:var(--text); cursor:pointer; outline:none; width:130px;
}}
.status-select.not-contacted {{ border-color:var(--border); }}
.status-select.message-sent {{ border-color:var(--warning); color:var(--warning); }}
.status-select.responded {{ border-color:var(--accent); color:var(--accent); }}
.status-select.meeting {{ border-color:#c084fc; color:#c084fc; }}
.status-select.applied {{ border-color:var(--i-color); color:var(--i-color); }}
.status-select.rejected {{ border-color:var(--danger); color:var(--danger); }}
.status-select.offer {{ border-color:var(--success); color:var(--success); }}
/* Danger Zone */
.danger-zone-card {{ border-left:3px solid #ef4444 !important; }}
.danger-badge {{ display:inline-flex;align-items:center;gap:4px;background:#ef4444;color:#fff;font-size:9px;font-weight:700;padding:2px 7px;border-radius:4px;text-transform:uppercase;letter-spacing:0.5px; }}
.danger-info {{ background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:8px;padding:10px 12px;margin-top:8px;font-size:12px;color:#fca5a5; }}
.email-col {{ font-size:11px; color:var(--text-muted); word-break:break-all; }}
.expand-btn {{
  width:28px; height:28px; border-radius:6px; border:1px solid var(--border);
  background:transparent; color:var(--text-muted); cursor:pointer; font-size:14px;
  display:flex; align-items:center; justify-content:center; transition:all 0.2s;
}}
.expand-btn:hover {{ border-color:var(--accent); color:var(--accent); }}
.expand-btn.open {{ transform:rotate(180deg); }}

/* Expanded area */
.contact-expanded {{ display:none; padding:0 0 16px 48px; }}
.contact-expanded.open {{ display:block; }}
.expanded-grid {{ display:grid; grid-template-columns: 1fr 1fr; gap:16px; }}
.expanded-section {{
  background:var(--bg); border:1px solid var(--border); border-radius:10px; padding:14px;
}}
.expanded-section h4 {{
  font-size:11px; text-transform:uppercase; color:var(--text-muted);
  letter-spacing:0.5px; margin-bottom:8px;
}}
.expanded-section textarea {{
  width:100%; min-height:180px; padding:10px; font-size:12px; line-height:1.6;
  border-radius:6px; border:1px solid var(--border); background:var(--card-bg);
  color:var(--text); resize:vertical; outline:none; font-family:inherit;
}}
.expanded-section textarea:focus {{ border-color:var(--accent); }}
.expanded-section .comm-tip {{ font-size:12px; color:var(--text-muted); line-height:1.5; padding:8px 0; }}
.expanded-section .comm-tip strong {{ color:var(--text); }}
.notes-area {{ min-height:100px; }}
.date-row {{ display:flex; gap:12px; align-items:center; margin-top:8px; }}
.date-row label {{ font-size:11px; color:var(--text-muted); }}
.date-row input {{
  padding:4px 8px; font-size:11px; border-radius:6px; border:1px solid var(--border);
  background:var(--bg); color:var(--text); outline:none;
}}
.save-indicator {{
  position:fixed; bottom:20px; right:20px; padding:10px 20px; border-radius:8px;
  background:var(--success); color:#000; font-size:13px; font-weight:600;
  opacity:0; transition:opacity 0.3s; pointer-events:none; z-index:200;
}}
.save-indicator.show {{ opacity:1; }}

/* === TOOLTIPS === */
[data-tooltip] {{ position:relative; cursor:help; }}
[data-tooltip]::after {{
  content:attr(data-tooltip); position:absolute; bottom:calc(100% + 8px); left:50%;
  transform:translateX(-50%); background:#1a1d27; color:#e1e4ed;
  padding:8px 12px; border-radius:8px; font-size:11px; font-weight:400;
  line-height:1.4; white-space:normal; max-width:260px; width:max-content;
  text-align:left; pointer-events:none; opacity:0; transition:opacity 0.2s;
  z-index:500; box-shadow:0 4px 12px rgba(0,0,0,0.3);
  text-transform:none; letter-spacing:normal;
}}
[data-tooltip]::before {{
  content:''; position:absolute; bottom:calc(100% + 2px); left:50%;
  transform:translateX(-50%); border:6px solid transparent;
  border-top-color:#1a1d27; pointer-events:none; opacity:0;
  transition:opacity 0.2s; z-index:501;
}}
[data-tooltip]:hover::after, [data-tooltip]:hover::before {{ opacity:1; }}
body.light [data-tooltip]::after {{ background:#1e293b; color:#f1f5f9; }}
body.light [data-tooltip]::before {{ border-top-color:#1e293b; }}
[data-tooltip].tooltip-down::after {{ bottom:auto; top:calc(100% + 8px); }}
[data-tooltip].tooltip-down::before {{ bottom:auto; top:calc(100% + 2px); border-top-color:transparent; border-bottom-color:#1a1d27; }}
body.light [data-tooltip].tooltip-down::before {{ border-top-color:transparent; border-bottom-color:#1e293b; }}
.info-icon {{
  display:inline-flex; align-items:center; justify-content:center;
  width:14px; height:14px; border-radius:50%; background:var(--border);
  color:var(--text-muted); font-size:9px; font-weight:700; font-style:italic;
  cursor:help; margin-left:4px; vertical-align:middle; flex-shrink:0;
}}

/* === GUIDE PAGE === */
.guide-section {{
  background:var(--card-bg); border:1px solid var(--border);
  border-radius:12px; padding:20px; margin-bottom:16px;
}}
.guide-section h3 {{ color:var(--accent); font-size:16px; margin-bottom:10px; }}
#consult-app .guide-section h3 {{ color:var(--purple); }}
.guide-section p, .guide-section li {{ font-size:13px; line-height:1.7; color:var(--text); }}
.guide-section ul {{ margin:8px 0; padding-left:20px; }}
.guide-disc-card {{
  padding:14px; border-radius:10px; border:1px solid var(--border); background:var(--bg);
}}
.guide-disc-card h4 {{ margin-bottom:6px; font-size:14px; }}
.guide-disc-card p {{ font-size:12px; color:var(--text-muted); line-height:1.6; }}

/* Column header */
#jobs-app .col-header {{
  display:grid; grid-template-columns: 40px 1fr 140px 180px 100px 90px 70px 140px 40px;
  padding:8px 0; gap:8px; margin:0 24px; border-bottom:2px solid var(--border);
  font-size:10px; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-muted); font-weight:600;
}}
#consult-app .col-header {{
  display:grid; grid-template-columns: 40px 1fr 150px 90px 80px 140px 40px;
  padding:8px 0; gap:8px; margin:0 24px; border-bottom:2px solid var(--border);
  font-size:10px; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-muted); font-weight:600;
}}

{consult_specific_css}

/* === MOBILE === */
@media (max-width: 768px) {{
  .passcode-box {{ padding:32px 20px; margin:0 16px; }}
  .passcode-box input {{ width:100%; }}
  #mode-bar {{ flex-wrap:wrap; }}
  #mode-bar .mode-tab {{ font-size:13px; padding:10px 16px; }}
  .top-bar {{ flex-direction:column; gap:12px; padding:12px 16px; top:47px; }}
  .top-bar h1 {{ font-size:15px; }}
  .top-bar-actions {{ flex-wrap:wrap; justify-content:center; gap:6px; }}
  .top-bar-actions button, .top-bar-actions label {{ padding:6px 10px; font-size:11px; }}
  .stats-bar {{ padding:12px 16px; gap:8px; }}
  .stat-card {{ min-width:0; flex:1; padding:10px 8px; }}
  .stat-card .num {{ font-size:20px; }}
  .filters {{ padding:0 16px 12px; gap:6px; overflow-x:auto; flex-wrap:nowrap; -webkit-overflow-scrolling:touch; }}
  .filters::-webkit-scrollbar {{ display:none; }}
  .filter-btn {{ white-space:nowrap; flex-shrink:0; }}
  .search-input {{ width:140px; flex-shrink:0; }}
  .disc-group-header {{ padding:10px 16px; font-size:12px; }}
  .col-header {{ display:none !important; }}
  .contact-card {{ margin:0 16px; }}
  #jobs-app .contact-main, #consult-app .contact-main {{
    display:flex; flex-direction:column; gap:6px; padding:14px 0;
  }}
  .contact-main::after {{
    content: attr(data-mobile-info);
    font-size:10px; color:var(--text-muted); padding-top:4px;
  }}
  .priority-badge {{ position:absolute; right:0; top:14px; }}
  .contact-main {{ position:relative; }}
  .company-col, .email-col {{ display:none; }}
  .expanded-grid {{ grid-template-columns:1fr; }}
  .contact-expanded {{ padding:0 0 16px 16px; }}
}}
</style>
<script src="https://cdn.sheetjs.com/xlsx-0.20.1/package/dist/xlsx.full.min.js"></script>
</head>
<body>

<!-- PASSCODE SCREEN -->
<div id="passcode-screen">
  <div class="passcode-box">
    <h1>Alessio CRM</h1>
    <p style="color:var(--accent);font-style:italic;margin-bottom:8px;">The world needs what you have to offer. Go get it.</p>
    <p style="color:var(--text-muted);font-size:12px;margin-bottom:24px;">Built for you with love, by Lia</p>
    <input type="password" id="passcode-input" placeholder="Enter passcode" autofocus>
    <button onclick="checkPasscode()">Unlock</button>
    <div class="passcode-error" id="passcode-error">Incorrect passcode. Try again.</div>
  </div>
</div>

<!-- MAIN APP -->
<div id="app">

  <!-- MODE BAR -->
  <div id="mode-bar">
    <button class="mode-tab active-jobs" id="mode-jobs-btn" onclick="switchCRM('jobs')">Jobs CRM</button>
    <button class="mode-tab" id="mode-consult-btn" onclick="switchCRM('consult')">Consulting CRM</button>
    <div class="mode-actions">
      <button onclick="lockApp()" class="tooltip-down" data-tooltip="Lock and return to passcode screen">Lock</button>
      <button id="theme-toggle" onclick="toggleTheme()" style="font-size:16px;padding:4px 10px;" class="tooltip-down" data-tooltip="Switch between dark and light theme">&#9788;</button>
    </div>
  </div>

  <!-- JOBS APP -->
  <div id="jobs-app">
{jobs_inner_html}
  </div>

  <!-- CONSULTING APP -->
  <div id="consult-app" style="display:none">
{consult_inner_html}
  </div>

</div><!-- end #app -->

<script>
// =============================================
// SHARED UTILITIES
// =============================================
let RESOLVED_HASH = null;

async function sha256(str) {{
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(str));
  return Array.from(new Uint8Array(buf)).map(b => b.toString(16).padStart(2,"0")).join("");
}}

sha256("123").then(h => {{
  RESOLVED_HASH = h;
  if (localStorage.getItem("alessio_crm_auth") === h) unlock();
}});

function unlock() {{
  document.getElementById("passcode-screen").style.display = "none";
  document.getElementById("app").style.display = "block";
  // Restore last mode
  const lastMode = localStorage.getItem("alessio_crm_mode") || "jobs";
  switchCRM(lastMode);
}}

async function checkPasscode() {{
  const input = document.getElementById("passcode-input").value;
  const hash = await sha256(input);
  if (hash === RESOLVED_HASH) {{
    localStorage.setItem("alessio_crm_auth", RESOLVED_HASH);
    unlock();
  }} else {{
    document.getElementById("passcode-error").style.display = "block";
    document.getElementById("passcode-input").value = "";
    document.getElementById("passcode-input").focus();
  }}
}}

document.getElementById("passcode-input").addEventListener("keydown", e => {{
  if (e.key === "Enter") checkPasscode();
}});

function lockApp() {{
  localStorage.removeItem("alessio_crm_auth");
  document.getElementById("passcode-screen").style.display = "flex";
  document.getElementById("app").style.display = "none";
}}

// === THEME ===
function toggleTheme() {{
  document.body.classList.toggle('light');
  const isLight = document.body.classList.contains('light');
  localStorage.setItem('alessio_crm_theme', isLight ? 'light' : 'dark');
  document.getElementById('theme-toggle').innerHTML = isLight ? '&#9790;' : '&#9788;';
}}
(function initTheme() {{
  if (localStorage.getItem('alessio_crm_theme') === 'light') {{
    document.body.classList.add('light');
    document.addEventListener('DOMContentLoaded', () => {{
      const btn = document.getElementById('theme-toggle');
      if (btn) btn.innerHTML = '&#9790;';
    }});
  }}
}})();

// === CRM MODE SWITCHING ===
function switchCRM(mode) {{
  localStorage.setItem("alessio_crm_mode", mode);
  const jobsApp = document.getElementById("jobs-app");
  const consultApp = document.getElementById("consult-app");
  const jobsBtn = document.getElementById("mode-jobs-btn");
  const consultBtn = document.getElementById("mode-consult-btn");

  if (mode === "jobs") {{
    jobsApp.style.display = "block";
    consultApp.style.display = "none";
    jobsBtn.className = "mode-tab active-jobs";
    consultBtn.className = "mode-tab";
    JobsCRM.renderContacts();
    JobsCRM.updateStats();
  }} else {{
    jobsApp.style.display = "none";
    consultApp.style.display = "block";
    jobsBtn.className = "mode-tab";
    consultBtn.className = "mode-tab active-consult";
    ConsultCRM.renderContacts();
    ConsultCRM.updateStats();
  }}
}}

// =============================================
// JOBS CRM NAMESPACE
// =============================================
const JobsCRM = (function() {{
  // === CV VARIANTS ===
{jobs_cvVariants}

  // Italian shared sections
{jobs_cvSharedIT}

  // Shared CV sections
{jobs_cvShared}

  function buildCV(v) {{
    const d = cvVariants[v];
    const isIT = v === 'italiano';
    const shared = isIT ? cvSharedIT : cvShared;
    const loc = isIT ? 'Pisa, Italia' : 'Pisa, Italy';
    const mobil = isIT ? 'Cittadino UE \\u00b7 Disponibile al trasferimento in Europa' : 'EU Citizen \\u00b7 Internationally mobile \\u00b7 Open to relocation across Europe';
    const sumTitle = isIT ? 'Profilo Professionale' : 'Executive Summary';
    const compTitle = isIT ? 'Competenze Chiave' : 'Core Competencies';

    let html = `<div style="text-align:center;margin-bottom:8px;">
      <h1 style="font-size:26px;font-weight:700;color:#1a1a2e;margin:0 0 4px 0;letter-spacing:0.5px;">ALESSIO MENCARONI</h1>
      <p style="font-size:15px;color:#4a5568;margin:0 0 12px 0;font-weight:500;">${{d.headline}}</p>
      <div style="font-size:12px;color:#718096;display:flex;justify-content:center;gap:20px;flex-wrap:wrap;">
        <span>${{loc}}</span><span>+39 347 803 1137</span><span>alessio.mencaroni@icloud.com</span>
        <a href="https://linkedin.com/in/alessiomencaroni" target="_blank" style="color:#2563eb;text-decoration:none;">linkedin.com/in/alessiomencaroni</a>
      </div>
      <p style="font-size:11.5px;color:#4a9eff;margin:6px 0 0 0;font-weight:500;">${{mobil}}</p>
    </div>
    <hr style="border:none;border-top:2px solid #2563eb;margin:16px 0;">`;

    html += `<h2 style="font-size:14px;font-weight:700;color:#2563eb;text-transform:uppercase;letter-spacing:1.2px;margin:20px 0 10px 0;border-bottom:1px solid #e2e8f0;padding-bottom:4px;">${{sumTitle}}</h2>`;
    d.summary.forEach(p => html += `<p style="margin:0 0 6px 0;">${{p}}</p>`);
    html += shared.achievements;
    html += `<h2 style="font-size:14px;font-weight:700;color:#2563eb;text-transform:uppercase;letter-spacing:1.2px;margin:24px 0 10px 0;border-bottom:1px solid #e2e8f0;padding-bottom:4px;">${{compTitle}}</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 24px;font-size:13px;">`;
    d.competencies.forEach(c => html += `<div style="display:flex;align-items:center;gap:6px;"><span style="color:#2563eb;font-weight:700;">\\u25b6</span> ${{c}}</div>`);
    html += `</div>`;
    html += shared.experience;
    html += shared.bottom;
    html += `<div style="margin-top:24px;padding:16px 20px;background:linear-gradient(135deg,#ebf5ff 0%,#f0fdf4 100%);border-radius:10px;border:1px solid #bfdbfe;">
      <h3 style="font-size:13px;font-weight:700;color:#1e40af;margin:0 0 8px 0;">${{d.whyTitle}}</h3>
      <p style="margin:0;font-size:12.5px;line-height:1.65;color:#334155;">${{d.whyText}}</p>
    </div>`;
    return html;
  }}

  function switchCVVariant(v) {{ document.getElementById('jobs-cv-dynamic').innerHTML = buildCV(v); }}

  const cvPrintCSS = `@page{{margin:14mm 12mm;}}body{{font-family:"Segoe UI",system-ui,-apple-system,sans-serif;line-height:1.55;font-size:13.5px;color:#1a1a2e;margin:0;padding:0;}}a{{color:#2563eb;text-decoration:none;}}@media print{{body{{-webkit-print-color-adjust:exact;print-color-adjust:exact;}}}}`;

  function downloadPDF() {{
    const v = document.getElementById('jobs-cv-variant-select').value;
    const content = buildCV(v);
    const w = window.open('','_blank');
    w.document.write('<html><head><title>CV - Alessio Mencaroni - '+v.toUpperCase()+'</title><style>'+cvPrintCSS+'</style></head><body>'+content+'</body></html>');
    w.document.close();
    setTimeout(()=>{{w.print();}},400);
  }}

  function downloadWord() {{
    const v = document.getElementById('jobs-cv-variant-select').value;
    const content = buildCV(v);
    const html = `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">
<head><meta charset="utf-8"><title>CV - Alessio Mencaroni</title>
<style>@page{{size:A4;margin:16mm 14mm;}}body{{font-family:"Segoe UI",Calibri,sans-serif;line-height:1.55;font-size:13.5px;color:#1a1a2e;}}a{{color:#2563eb;text-decoration:none;}}</style>
</head><body>${{content}}</body></html>`;
    const blob = new Blob([html], {{type:'application/msword'}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url; a.download = 'CV_Alessio_Mencaroni_'+v+'.doc';
    document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
  }}

  // === COVER LETTER ===
  function populateCLContacts() {{
    const sel = document.getElementById('jobs-cl-contact-select');
    if (!sel || sel.options.length > 1) return;
    contacts.filter(c => c.role !== 'ta').forEach(c => {{
      const opt = document.createElement('option');
      opt.value = c.id; opt.textContent = c.name + ' - ' + c.company;
      sel.appendChild(opt);
    }});
    const grp = document.createElement('optgroup'); grp.label = 'Recruiters';
    contacts.filter(c => c.role === 'ta').forEach(c => {{
      const opt = document.createElement('option');
      opt.value = c.id; opt.textContent = c.name + ' - ' + c.company;
      grp.appendChild(opt);
    }});
    sel.appendChild(grp);
  }}

  function generateCoverLetter() {{
    const cid = document.getElementById('jobs-cl-contact-select').value;
    const out = document.getElementById('jobs-cl-output');
    if (!cid) {{ out.textContent = 'Select a contact above to generate a cover letter.'; return; }}
    const c = contacts.find(x => x.id === cid);
    const v = document.getElementById('jobs-cv-variant-select').value;
    const d = cvVariants[v];
    if (!c) return;
    const msg = (c.message || '').replace(/^Subject:.*\\n\\n?/i, '').trim();
    const firstName = c.name.split(',')[0].split('(')[0].trim().split(' ');
    const salutation = firstName.length > 1 ? firstName[0] : c.name.split(' ')[0];
    const today = new Date().toLocaleDateString('en-GB', {{day:'numeric',month:'long',year:'numeric'}});
    const letter = `${{today}}\\n\\n${{c.name}}\\n${{c.title}}\\n${{c.company}}\\n\\nDear ${{salutation}},\\n\\n${{msg}}\\n\\nI have attached my CV for your reference. I would welcome the opportunity to discuss how my background in technology transfer, process industrialization, and operational excellence in regulated manufacturing environments could contribute to ${{c.company}}'s objectives.\\n\\nI am available for a call at your convenience.\\n\\nBest regards,\\nAlessio Mencaroni\\n+39 347 803 1137\\nalessio.mencaroni@icloud.com\\nlinkedin.com/in/alessiomencaroni`;
    out.textContent = letter;
  }}

  function copyCoverLetter() {{
    const text = document.getElementById('jobs-cl-output').textContent;
    if (text.startsWith('Select a')) return;
    navigator.clipboard.writeText(text);
    const btn = event.target; btn.textContent = 'Copied!'; setTimeout(() => btn.textContent = 'Copy', 1500);
  }}

  function downloadCoverLetterWord() {{
    const text = document.getElementById('jobs-cl-output').textContent;
    if (text.startsWith('Select a')) return;
    const cid = document.getElementById('jobs-cl-contact-select').value;
    const c = contacts.find(x => x.id === cid);
    const html = `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word"><head><meta charset="utf-8"><style>@page{{size:A4;margin:20mm 18mm;}}body{{font-family:"Segoe UI",Calibri,sans-serif;line-height:1.7;font-size:13px;color:#1a1a2e;white-space:pre-wrap;}}</style></head><body>${{text}}</body></html>`;
    const blob = new Blob([html], {{type:'application/msword'}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url;
    a.download = 'CoverLetter_' + c.company.replace(/[^a-zA-Z0-9]/g,'_') + '.doc';
    document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
  }}

  // === CONTACTS DATA ===
{jobs_contacts}

  // === STATE ===
  const STORAGE_KEY = "alessio_crm_data";
  let state = {{}};

  function loadState() {{
    try {{ state = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{{}}'); }} catch(e) {{ state = {{}}; }}
    contacts.forEach(c => {{
      if (!state[c.id]) state[c.id] = {{ status: "Not Contacted", notes: "", lastContacted: "", message: c.message }};
    }});
  }}

  function saveState() {{
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    const ind = document.getElementById("jobs-save-indicator");
    ind.classList.add("show"); setTimeout(() => ind.classList.remove("show"), 1500);
  }}

  function exportData() {{
    const blob = new Blob([JSON.stringify(state, null, 2)], {{type:"application/json"}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a"); a.href = url;
    a.download = "alessio_crm_backup_" + new Date().toISOString().slice(0,10) + ".json";
    document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
  }}

  function importData(event) {{
    const file = event.target.files[0]; if (!file) return;
    const reader = new FileReader();
    reader.onload = function(e) {{
      try {{
        state = JSON.parse(e.target.result);
        contacts.forEach(c => {{
          if (!state[c.id]) state[c.id] = {{ status: "Not Contacted", notes: "", lastContacted: "", message: c.message }};
        }});
        saveState(); renderContacts(); updateStats();
        alert("Data imported successfully!");
      }} catch(err) {{ alert("Invalid JSON file."); }}
    }};
    reader.readAsText(file);
  }}

  // === EXCEL ===
  function exportExcel() {{
    const rows = contacts.map(c => {{
      const s = state[c.id] || {{}};
      return {{
        "Name": c.name, "Title": c.title, "Company": c.company, "Email": c.email,
        "DISC Type": c.disc, "DISC Label": c.discLabel,
        "Role": c.role === "msat" ? "MSAT / Tech Transfer" : (c.role === "ops" ? "Operations / Engineering" : "Talent Acquisition"),
        "Priority": c.priority > 0 ? c.priority : "", "Remote": c.remote, "Country": c.country,
        "LinkedIn": c.linkedin, "Status": s.status || "Not Contacted",
        "Last Contacted": s.lastContacted || "",
        "Communication Guide": c.howToComm,
        "Tailored Message": (s.message || c.message || "").replace(/\\\\n/g, "\\n"),
        "Notes": s.notes || ""
      }};
    }});
    const ws = XLSX.utils.json_to_sheet(rows);
    ws["!cols"] = [{{wch:22}},{{wch:35}},{{wch:30}},{{wch:35}},{{wch:8}},{{wch:20}},{{wch:25}},{{wch:8}},{{wch:8}},{{wch:15}},{{wch:45}},{{wch:16}},{{wch:14}},{{wch:50}},{{wch:80}},{{wch:40}}];
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Contacts");
    XLSX.writeFile(wb, `alessio_crm_${{new Date().toISOString().slice(0,10)}}.xlsx`);
  }}

  function importExcel(event) {{
    const file = event.target.files[0]; if (!file) return;
    const reader = new FileReader();
    reader.onload = e => {{
      try {{
        const wb = XLSX.read(e.target.result, {{type:"array"}});
        const ws = wb.Sheets[wb.SheetNames[0]];
        const rows = XLSX.utils.sheet_to_json(ws);
        let imported = 0;
        rows.forEach(row => {{
          const name = (row["Name"] || "").trim();
          const contact = contacts.find(c => c.name === name);
          if (!contact) return;
          const id = contact.id;
          if (!state[id]) state[id] = {{ status:"Not Contacted", notes:"", lastContacted:"", message:contact.message }};
          if (row["Status"] && statuses.includes(row["Status"])) state[id].status = row["Status"];
          if (row["Last Contacted"]) state[id].lastContacted = String(row["Last Contacted"]).slice(0,10);
          if (row["Notes"] !== undefined && row["Notes"] !== "") state[id].notes = String(row["Notes"]);
          if (row["Tailored Message"] !== undefined && row["Tailored Message"] !== "") state[id].message = String(row["Tailored Message"]);
          imported++;
        }});
        saveState(); renderContacts(); updateStats();
        alert(`Imported data for ${{imported}} contacts from Excel.`);
      }} catch(err) {{ alert("Error reading Excel file: " + err.message); }}
    }};
    reader.readAsArrayBuffer(file); event.target.value = "";
  }}

  // === FILTERS ===
  let activeFilters = new Set();

  function toggleFilter(btn) {{
    const f = btn.dataset.filter;
    if (activeFilters.has(f)) {{ activeFilters.delete(f); btn.classList.remove("active"); }}
    else {{ activeFilters.add(f); btn.classList.add("active"); }}
    renderContacts();
  }}

  function passesFilter(c) {{
    const searchEl = document.querySelector("#jobs-app .search-input");
    const search = searchEl ? searchEl.value.toLowerCase() : "";
    if (search && !c.name.toLowerCase().includes(search) && !c.company.toLowerCase().includes(search) && !c.title.toLowerCase().includes(search)) return false;
    let discFilters = [...activeFilters].filter(f => f.startsWith("disc-"));
    let roleFilters = [...activeFilters].filter(f => f.startsWith("role-"));
    let statusFilters = [...activeFilters].filter(f => f.startsWith("status-"));
    if (discFilters.length > 0) {{ const primaryDisc = c.disc[0]; if (!discFilters.some(f => f === "disc-" + primaryDisc)) return false; }}
    if (roleFilters.length > 0) {{ if (!roleFilters.some(f => f === "role-" + c.role)) return false; }}
    if (statusFilters.length > 0 && statusFilters.includes("status-active")) {{
      const s = (state[c.id] && state[c.id].status) || "Not Contacted";
      if (s === "Rejected" || s === "Offer") return false;
    }}
    return true;
  }}

  // === RENDERING ===
  const discOrder = ['D','I','S','C'];
  const discNames = {{D:"Captain \\u2014 Direct, Decisive, Results-First",I:"Motivator \\u2014 Enthusiastic, Creative, People-First",S:"Supporter \\u2014 Steady, Loyal, Harmony-First",C:"Analyst \\u2014 Logical, Precise, Data-First"}};
  const discTooltips = {{D:"Dominant \\u2014 direct, results-oriented, decisive. Be brief and lead with outcomes.",I:"Influential \\u2014 enthusiastic, collaborative, optimistic. Be warm and show personality.",S:"Steady \\u2014 patient, reliable, team-oriented. Be sincere and supportive.",C:"Conscientious \\u2014 analytical, precise, quality-focused. Be detailed and factual."}};
  const discColors = {{D:"var(--d-color)",I:"var(--i-color)",S:"var(--s-color)",C:"var(--c-color)"}};
  const careersUrls = {{
    "AstraZeneca":"https://careers.astrazeneca.com/","Sanofi":"https://jobs.sanofi.com/en","GSK":"https://www.gsk.com/en-gb/careers/",
    "Lonza":"https://www.lonza.com/careers","Chiesi Farmaceutici":"https://www.chiesi.com/en/work-with-us/",
    "Menarini Group":"https://www.menarini.com/en-us/careers","Merck / MSD":"https://jobs.merck.com/us/en",
    "Eli Lilly":"https://careers.lilly.com/us/en","Takeda":"https://www.takeda.com/careers/",
    "Novo Nordisk":"https://www.novonordisk.com/careers.html","Novartis":"https://www.novartis.com/careers",
    "BASF":"https://www.basf.com/global/en/careers","Merck Millipore (Merck KGaA)":"https://careers.emdgroup.com/us/en/home",
    "Korn Ferry":"https://www.kornferry.com/","Page Executive (PageGroup)":"https://www.pageexecutive.com/",
    "SRG (Impellam / HeadFirst Group)":"https://www.srgtalent.com/",
    "Kelly Science, Engineering, Technology & Telecom":"https://www.kellyservices.com/",
    "Pfizer":"https://www.pfizer.com/about/careers","Pfizer Belgium (Puurs)":"https://www.pfizer.com/about/careers",
    "Roche":"https://careers.roche.com/global/en","Boehringer Ingelheim":"https://www.boehringer-ingelheim.com/careers",
    "WuXi Biologics":"https://www.wuxibiologics.com/join-us/",
    "Fujifilm Diosynth Biotechnologies":"https://fujifilmbiotechnologies.fujifilm.com/careers",
    "AGC Biologics":"https://www.agcbio.com/careers","Hays (Netherlands)":"https://www.hays.nl/",
    "Hays France":"https://www.hays.fr/","Hays AG (Switzerland)":"https://www.hays.ch/",
    "Proclinical Staffing":"https://www.proclinical.com/","EPM Scientific (Phaidon International)":"https://www.epmscientific.com/",
    "Thermo Fisher / Patheon":"https://jobs.thermofisher.com/"
  }};
  const statuses = ["Not Contacted","Message Sent","Responded","Meeting Scheduled","Applied","Rejected","Offer"];
  const statusClasses = {{"Not Contacted":"not-contacted","Message Sent":"message-sent","Responded":"responded","Meeting Scheduled":"meeting","Applied":"applied","Rejected":"rejected","Offer":"offer"}};

  function renderContacts() {{
    const container = document.getElementById("jobs-contacts-container");
    container.innerHTML = "";
    const filtered = contacts.filter(passesFilter);
    discOrder.forEach(d => {{
      const group = filtered.filter(c => c.disc[0] === d);
      if (group.length === 0) return;
      group.sort((a,b) => {{
        if (a.priority > 0 && b.priority > 0) return a.priority - b.priority;
        if (a.priority > 0) return -1;
        if (b.priority > 0) return 1;
        return a.name.localeCompare(b.name);
      }});
      const header = document.createElement("div");
      header.className = "disc-group-header";
      header.innerHTML = `<span class="disc-dot" style="background:${{discColors[d]}}"></span> ${{d}} \\u2014 ${{discNames[d]}} <span style="font-size:11px;color:var(--text-muted);font-weight:400;">(${{group.length}} contacts)</span>`;
      container.appendChild(header);
      group.forEach(c => {{
        const s = state[c.id] || {{}};
        const card = document.createElement("div");
        card.className = "contact-card" + (c.dangerZone ? " danger-zone-card" : "");
        card.dataset.id = c.id;
        const statusClass = statusClasses[s.status || "Not Contacted"];
        const priorityClass = c.priority > 0 && c.priority <= 10 ? "top" : "";
        const remoteLower = c.remote.toLowerCase().replace(/\\s/g,"");
        const remoteClass = remoteLower === "yes" ? "yes" : remoteLower === "no" ? "no" : (remoteLower === "hybrid" || remoteLower === "partial" ? "hybrid" : "");
        const remoteDisplay = remoteLower === "no" ? "On-site" : c.remote;
        const dangerBadge = c.dangerZone ? ' <span class="danger-badge" data-tooltip="This contact has risk factors \\u2014 see expanded card for details">Danger Zone</span>' : '';
        let followUpBadge = '';
        const activeStatuses = ['Message Sent','Responded','Meeting Scheduled'];
        if (s.lastContacted && activeStatuses.includes(s.status)) {{
          const daysSince = Math.floor((Date.now() - new Date(s.lastContacted).getTime()) / 86400000);
          if (daysSince > 14) followUpBadge = ` <span style="display:inline-flex;align-items:center;gap:3px;background:var(--warning);color:#000;font-size:9px;font-weight:700;padding:2px 7px;border-radius:4px;" data-tooltip="Last contacted ${{daysSince}} days ago \\u2014 consider following up">Follow up (${{daysSince}}d)</span>`;
        }}
        card.innerHTML = `
          <div class="contact-main" data-mobile-info="${{c.company}} \\u00b7 ${{c.email}} \\u00b7 Remote: ${{remoteDisplay}}" onclick="JobsCRM.toggleExpand('${{c.id}}')">
            <div class="priority-badge ${{priorityClass}}" data-tooltip="${{c.priority > 0 ? 'Priority #' + c.priority + ' \\u2014 top target' : 'No priority ranking'}}">${{c.priority > 0 ? c.priority : "\\u2014"}}</div>
            <div class="contact-info"><h3>${{c.name}}${{dangerBadge}}${{followUpBadge}}</h3><p>${{c.title}}</p></div>
            <div class="company-col">${{careersUrls[c.company] ? `<a href="${{careersUrls[c.company]}}" target="_blank" style="color:var(--accent);text-decoration:none;font-size:12px;" onclick="event.stopPropagation()">${{c.company}}</a>` : c.company}}</div>
            <div class="email-col"><a href="mailto:${{c.email}}" style="color:var(--accent);text-decoration:none;font-size:11px;" onclick="event.stopPropagation()">${{c.email}}</a></div>
            <div><span class="disc-badge ${{c.disc[0].toLowerCase()}}" data-tooltip="${{discTooltips[c.disc[0]]}}">${{c.disc}}</span> <span style="font-size:10px;color:var(--text-muted);">${{c.discLabel}}</span></div>
            <div><span class="remote-badge ${{remoteClass}}" style="text-align:center;" data-tooltip="${{remoteLower === 'yes' ? 'Fully remote' : remoteLower === 'hybrid' || remoteLower === 'partial' ? 'Mix of office and remote' : remoteLower === 'no' ? 'On-site only' : ''}}"><span class="remote-badge-label">REMOTE</span><span class="remote-badge-value">${{remoteDisplay}}</span></span></div>
            <div><a class="linkedin-link" href="${{c.linkedin}}" target="_blank" onclick="event.stopPropagation()">LinkedIn \\u2192</a></div>
            <div><select class="status-select ${{statusClass}}" onchange="JobsCRM.updateStatus('${{c.id}}',this.value);event.stopPropagation();" onclick="event.stopPropagation();">
              ${{statuses.map(st => `<option value="${{st}}" ${{(s.status||"Not Contacted")===st?"selected":""}}>${{st}}</option>`).join("")}}
            </select></div>
            <div><button class="expand-btn" id="btn-${{c.id}}">&#9660;</button></div>
          </div>
          <div class="contact-expanded" id="exp-${{c.id}}">
            <div class="expanded-grid">
              <div class="expanded-section">
                <h4>Communication Guide (${{c.disc}} type)</h4>
                <div class="comm-tip"><strong>How to communicate:</strong> ${{c.howToComm}}</div>
                <h4 style="margin-top:12px;">Tailored Message (editable)</h4>
                <textarea onchange="JobsCRM.updateMessage('${{c.id}}',this.value)">${{(s.message||c.message).replace(/</g,"&lt;")}}</textarea>
              </div>
              <div class="expanded-section">
                <h4>Notes</h4>
                <textarea class="notes-area" placeholder="Add follow-up notes..." onchange="JobsCRM.updateNotes('${{c.id}}',this.value)">${{(s.notes||"").replace(/</g,"&lt;")}}</textarea>
                <div class="date-row"><label>Last contacted:</label><input type="date" value="${{s.lastContacted||""}}" onchange="JobsCRM.updateDate('${{c.id}}',this.value)"></div>
                <h4 style="margin-top:12px;">Contact Details</h4>
                <div class="comm-tip">
                  <strong>Company:</strong> ${{careersUrls[c.company] ? `<a href="${{careersUrls[c.company]}}" target="_blank" style="color:var(--accent);text-decoration:none;">${{c.company}} (Careers)</a>` : c.company}}<br>
                  <strong>Email:</strong> <a href="mailto:${{c.email}}" style="color:var(--accent);text-decoration:none;">${{c.email}}</a><br>
                  <strong>Country:</strong> ${{c.country}}<br>
                  <strong>Role type:</strong> ${{c.role === "msat" ? "MSAT / Tech Transfer" : (c.role === "ops" ? "Operations / Engineering" : "Talent Acquisition")}}
                </div>${{c.dangerZone ? `<div class="danger-info"><strong>\\u26a0 DANGER ZONE:</strong> ${{c.dangerZone}}</div>` : ''}}
              </div>
            </div>
          </div>`;
        container.appendChild(card);
      }});
    }});
    updateStats();
  }}

  function toggleExpand(id) {{
    document.getElementById("exp-" + id).classList.toggle("open");
    document.getElementById("btn-" + id).classList.toggle("open");
  }}

  function updateStatus(id, val) {{
    state[id].status = val;
    if (val !== "Not Contacted" && !state[id].lastContacted) state[id].lastContacted = new Date().toISOString().slice(0,10);
    saveState(); renderContacts();
  }}

  function updateNotes(id, val) {{ state[id].notes = val; saveState(); }}
  function updateMessage(id, val) {{ state[id].message = val; saveState(); }}
  function updateDate(id, val) {{ state[id].lastContacted = val; saveState(); }}

  function updateStats() {{
    const bar = document.getElementById("jobs-stats-bar");
    const total = contacts.length;
    const contacted = contacts.filter(c => state[c.id] && state[c.id].status !== "Not Contacted").length;
    const responded = contacts.filter(c => state[c.id] && ["Responded","Meeting Scheduled","Applied","Offer"].includes(state[c.id].status)).length;
    const meetings = contacts.filter(c => state[c.id] && state[c.id].status === "Meeting Scheduled").length;
    const offers = contacts.filter(c => state[c.id] && state[c.id].status === "Offer").length;
    bar.innerHTML = `
      <div class="stat-card" data-tooltip="Total contacts"><div class="num">${{total}}</div><div class="label">Total</div></div>
      <div class="stat-card" data-tooltip="Contacted"><div class="num" style="color:var(--warning)">${{contacted}}</div><div class="label">Contacted</div></div>
      <div class="stat-card" data-tooltip="Responded"><div class="num" style="color:var(--accent)">${{responded}}</div><div class="label">Responded</div></div>
      <div class="stat-card" data-tooltip="Meetings"><div class="num" style="color:#c084fc">${{meetings}}</div><div class="label">Meetings</div></div>
      <div class="stat-card" data-tooltip="Offers"><div class="num" style="color:var(--success)">${{offers}}</div><div class="label">Offers</div></div>`;
  }}

  // === VIEWS ===
  function showView(view) {{
    document.getElementById('jobs-crm-view').style.display = view === 'crm' ? 'block' : 'none';
    document.getElementById('jobs-research-view').style.display = view === 'research' ? 'block' : 'none';
    document.getElementById('jobs-cv-view').style.display = view === 'cv' ? 'block' : 'none';
    document.getElementById('jobs-guide-view').style.display = view === 'guide' ? 'block' : 'none';
    const rBtn = document.getElementById('jobs-toggle-research-btn');
    const cBtn = document.getElementById('jobs-toggle-cv-btn');
    const gBtn = document.getElementById('jobs-toggle-guide-btn');
    rBtn.style.background = view === 'research' ? 'var(--bg)' : '#6366f1';
    rBtn.style.color = view === 'research' ? 'var(--text-muted)' : '#fff';
    rBtn.style.borderColor = view === 'research' ? 'var(--border)' : '#6366f1';
    rBtn.textContent = view === 'research' ? 'Back to CRM' : 'Research';
    cBtn.style.background = view === 'cv' ? 'var(--bg)' : '#10b981';
    cBtn.style.color = view === 'cv' ? 'var(--text-muted)' : '#fff';
    cBtn.style.borderColor = view === 'cv' ? 'var(--border)' : '#10b981';
    cBtn.textContent = view === 'cv' ? 'Back to CRM' : 'CV';
    gBtn.style.background = view === 'guide' ? 'var(--bg)' : '#f59e0b';
    gBtn.style.color = view === 'guide' ? 'var(--text-muted)' : '#000';
    gBtn.style.borderColor = view === 'guide' ? 'var(--border)' : '#f59e0b';
    gBtn.textContent = view === 'guide' ? 'Back to CRM' : 'Help';
    window.scrollTo(0, 0);
  }}
  function toggleResearch() {{ showView(document.getElementById('jobs-research-view').style.display !== 'none' ? 'crm' : 'research'); }}
  function showCV() {{
    const isShowing = document.getElementById('jobs-cv-view').style.display !== 'none';
    showView(isShowing ? 'crm' : 'cv');
    if (!isShowing) {{ switchCVVariant(document.getElementById('jobs-cv-variant-select').value); populateCLContacts(); }}
  }}
  function showCRM() {{ showView('crm'); }}
  function showGuide() {{ showView(document.getElementById('jobs-guide-view').style.display !== 'none' ? 'crm' : 'guide'); }}

  // Init
  loadState();

  return {{
    renderContacts, updateStats, toggleFilter, toggleResearch, showCV, showCRM, showGuide,
    exportData, importData, exportExcel, importExcel,
    downloadPDF, downloadWord, switchCVVariant,
    generateCoverLetter, copyCoverLetter, downloadCoverLetterWord,
    toggleExpand, updateStatus, updateNotes, updateMessage, updateDate,
    populateCLContacts
  }};
}})();

// =============================================
// CONSULTING CRM NAMESPACE
// =============================================
const ConsultCRM = (function() {{
  // === CONTACTS DATA ===
{consult_contacts}

  // === CV VARIANTS ===
{consult_cvVariants}

{consult_cvShared}

  function buildCV(v) {{
    const d = cvVariants[v]; const loc = v==='italiano' ? 'Pisa, Italia' : 'Pisa, Italy';
    const mobil = v==='italiano' ? 'Cittadino UE \\u00b7 Disponibile per missioni internazionali' : 'EU Citizen \\u00b7 Available for international assignments \\u00b7 5 languages';
    let html = `<div style="text-align:center;margin-bottom:8px;">
      <h1 style="font-size:26px;font-weight:700;color:#1a1a2e;margin:0 0 4px 0;">ALESSIO MENCARONI</h1>
      <p style="font-size:15px;color:#4a5568;margin:0 0 12px 0;font-weight:500;">${{d.headline}}</p>
      <div style="font-size:12px;color:#718096;display:flex;justify-content:center;gap:20px;flex-wrap:wrap;">
        <span>${{loc}}</span><span>+39 347 803 1137</span><span>alessio.mencaroni@icloud.com</span>
        <a href="https://linkedin.com/in/alessiomencaroni" target="_blank" style="color:#7c3aed;text-decoration:none;">linkedin.com/in/alessiomencaroni</a>
      </div>
      <p style="font-size:11.5px;color:#7c3aed;margin:6px 0 0 0;font-weight:500;">${{mobil}}</p>
    </div><hr style="border:none;border-top:2px solid #7c3aed;margin:16px 0;">`;
    html += `<h2 style="font-size:14px;font-weight:700;color:#7c3aed;text-transform:uppercase;letter-spacing:1.2px;margin:20px 0 10px 0;border-bottom:1px solid #e2e8f0;padding-bottom:4px;">${{v==='italiano'?'Profilo Professionale':'Executive Summary'}}</h2>`;
    d.summary.forEach(p => html += `<p style="margin:0 0 6px 0;">${{p}}</p>`);
    html += cvShared.achievements;
    html += `<h2 style="font-size:14px;font-weight:700;color:#7c3aed;text-transform:uppercase;letter-spacing:1.2px;margin:24px 0 10px 0;border-bottom:1px solid #e2e8f0;padding-bottom:4px;">${{v==='italiano'?'Competenze Chiave':'Core Competencies'}}</h2><div style="display:grid;grid-template-columns:1fr 1fr;gap:4px 24px;font-size:13px;">`;
    d.competencies.forEach(c => html += `<div style="display:flex;align-items:center;gap:6px;"><span style="color:#7c3aed;font-weight:700;">\\u25b6</span> ${{c}}</div>`);
    html += `</div>`;
    html += cvShared.experience + cvShared.bottom;
    html += `<div style="margin-top:24px;padding:16px 20px;background:linear-gradient(135deg,#f3e8ff 0%,#f0fdf4 100%);border-radius:10px;border:1px solid #c4b5fd;">
      <h3 style="font-size:13px;font-weight:700;color:#5b21b6;margin:0 0 8px 0;">${{d.whyTitle}}</h3>
      <p style="margin:0;font-size:12.5px;line-height:1.65;color:#334155;">${{d.whyText}}</p>
    </div>`;
    return html;
  }}

  function switchCVVariant(v) {{ document.getElementById('consult-cv-dynamic').innerHTML = buildCV(v); }}

  const cvPrintCSS = `@page{{margin:14mm 12mm;}}body{{font-family:"Segoe UI",system-ui,sans-serif;line-height:1.55;font-size:13.5px;color:#1a1a2e;margin:0;padding:0;}}a{{color:#7c3aed;text-decoration:none;}}`;

  function downloadPDF() {{
    const v = document.getElementById('consult-cv-variant-select').value;
    const w = window.open('','_blank');
    w.document.write('<html><head><title>CV Consulting - Alessio Mencaroni</title><style>'+cvPrintCSS+'</style></head><body>'+buildCV(v)+'</body></html>');
    w.document.close(); setTimeout(()=>w.print(),400);
  }}

  function downloadWord() {{
    const v = document.getElementById('consult-cv-variant-select').value;
    const html = `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word"><head><meta charset="utf-8"><style>@page{{size:A4;margin:16mm 14mm;}}body{{font-family:"Segoe UI",Calibri,sans-serif;line-height:1.55;font-size:13.5px;color:#1a1a2e;}}</style></head><body>${{buildCV(v)}}</body></html>`;
    const blob = new Blob([html], {{type:'application/msword'}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url;
    a.download = 'CV_Consulting_Alessio_Mencaroni_'+v+'.doc';
    document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
  }}

  // === EOI GENERATOR ===
  function populateCLContacts() {{
    const sel = document.getElementById('consult-cl-contact-select');
    if (!sel || sel.options.length > 1) return;
    const cats = {{un:'UN Agencies',mdb:'Development Banks',eu:'EU / Bilateral',firm:'Consulting Firms'}};
    Object.entries(cats).forEach(([cat,label]) => {{
      const grp = document.createElement('optgroup'); grp.label = label;
      contacts.filter(c => c.category === cat).forEach(c => {{
        const opt = document.createElement('option'); opt.value = c.id;
        opt.textContent = c.name + ' \\u2014 ' + c.company; grp.appendChild(opt);
      }});
      sel.appendChild(grp);
    }});
  }}

{consult_eoiFields}

  function generateEOI() {{
    const cid = document.getElementById('consult-cl-contact-select').value;
    const out = document.getElementById('consult-cl-output');
    if (!cid) {{ out.textContent = 'Select an organization above to generate an Expression of Interest.'; return; }}
    const c = contacts.find(x => x.id === cid); if (!c) return;
    const v = document.getElementById('consult-cv-variant-select').value;
    const ef = eoiFields[v];
    const today = new Date().toLocaleDateString('en-GB', {{day:'numeric',month:'long',year:'numeric'}});
    const isIT = v === 'italiano';
    const eoi = isIT ? `ESPRESSIONE DI INTERESSE \\u2014 REGISTRAZIONE CONSULENTE\\n\\nData: ${{today}}\\nOrganizzazione: ${{c.company}}\\nRiferimento: ${{c.name}}\\n\\n1. DATI DEL CONSULENTE\\nNome: Alessio Mencaroni\\nNazionalit\\u00e0: Italiana (Cittadino UE)\\nResidenza: Pisa, Italia\\nContatto: +39 347 803 1137 | alessio.mencaroni@icloud.com\\nLinkedIn: linkedin.com/in/alessiomencaroni\\n\\n2. AREA TEMATICA\\n${{ef.thematic}}\\n\\n3. SETTORI DI COMPETENZA\\n${{ef.sectors}}\\n\\n4. SINTESI DELLE QUALIFICHE\\n- Laurea Magistrale in Ingegneria Chimica, Universit\\u00e0 di Pisa (110/110 e lode)\\n- 11 anni di esperienza in ambienti manifatturieri complessi (Europa e Asia)\\n- 5 anni di trasferimento tecnologico intercontinentale (Italia \\u2194 Cina)\\n- Lean Six Sigma Black Belt (SSGI)\\n- Riduzione emissioni PFAS del 95% \\u2014 coordinamento task force 50 persone\\n- Lingue: Italiano (madrelingua), Inglese (C2), Cinese (B1), Francese, Tedesco\\n\\n5. ESPERIENZA RILEVANTE\\n\\u2022 INEOS Inovyn (2024\\u2013presente): Senior Process Engineer\\n\\u2022 Solvay Specialty Polymers (2018\\u20132023): Trasferimento tecnologico Italia\\u2194Cina\\n\\u2022 Icap-Sira Chemicals (2016\\u20132018): Project Engineer\\n\\u2022 Turboden / Mitsubishi (2015\\u20132016): Process Engineer\\n\\n6. DISPONIBILIT\\u00c0\\nDisponibile per missioni a breve e medio termine. Cittadino UE, mobilit\\u00e0 internazionale.\\n\\nCV allegato.\\n\\nAlessio Mencaroni`
    : `EXPRESSION OF INTEREST \\u2014 CONSULTANT REGISTRATION\\n\\nDate: ${{today}}\\nOrganization: ${{c.company}}\\nReference: ${{c.name}}\\n\\n1. CONSULTANT DETAILS\\nName: Alessio Mencaroni\\nNationality: Italian (EU Citizen)\\nBase: Pisa, Italy\\nContact: +39 347 803 1137 | alessio.mencaroni@icloud.com\\nLinkedIn: linkedin.com/in/alessiomencaroni\\n\\n2. THEMATIC AREA\\n${{ef.thematic}}\\n\\n3. SECTORS OF EXPERTISE\\n${{ef.sectors}}\\n\\n4. SUMMARY OF QUALIFICATIONS\\n- MSc Chemical Engineering, University of Pisa (110/110 cum laude)\\n- 11 years of experience in complex manufacturing environments (Europe & Asia)\\n- 5 years of cross-continental technology transfer (Italy \\u2194 China, Solvay)\\n- Lean Six Sigma Black Belt (SSGI)\\n- 95% PFAS emission reduction \\u2014 coordinated 50-person cross-functional task force\\n- Languages: Italian (native), English (C2), Chinese Mandarin (B1), French, German\\n\\n5. RELEVANT EXPERIENCE\\n\\u2022 INEOS Inovyn (2024\\u2013present): Senior Process Engineer \\u2014 performance stabilization, +30% capacity, -75% alarm load, IMS ownership, HAZOP, CAPEX management. Seveso III regulated.\\n\\u2022 Solvay Specialty Polymers (2018\\u20132023): Process Technology Engineer \\u2014 cross-continental technology transfer of fluoropolymers (PTFE, PVDF, FKM, FFKM) between Italy and China. Scale-up from lab/pilot to full-scale. PFAS task force coordinator: 95% emission reduction, 4,000 samples/year.\\n\\u2022 Icap-Sira Chemicals (2016\\u20132018): Project Engineer \\u2014 process troubleshooting.\\n\\u2022 Turboden / Mitsubishi Heavy Industries (2015\\u20132016): Process Engineer \\u2014 ORC system design.\\n\\u2022 Guest Lecturer, Nottingham University Business School, China (2019\\u20132023)\\n\\n6. KEY ACHIEVEMENTS\\n- 95% PFAS micropollutant emission reduction (Stockholm Convention relevance)\\n- 30% production capacity increase through data-driven bottleneck analysis\\n- 90% maintenance reduction on critical systems via root-cause elimination\\n- 75% alarm load reduction improving operational effectiveness\\n- Published: Quantitative consequence assessment using dynamic process simulators (2018)\\n\\n7. AVAILABILITY\\nAvailable for short-term and medium-term assignments. EU citizen, internationally mobile.\\n\\nCV attached.\\n\\nAlessio Mencaroni`;
    out.textContent = eoi;
  }}

  function copyEOI() {{
    const t = document.getElementById('consult-cl-output').textContent;
    if (t.startsWith('Select')) return;
    navigator.clipboard.writeText(t);
    const b = event.target; b.textContent = 'Copied!'; setTimeout(() => b.textContent = 'Copy', 1500);
  }}

  function downloadEOIWord() {{
    const t = document.getElementById('consult-cl-output').textContent;
    if (t.startsWith('Select')) return;
    const cid = document.getElementById('consult-cl-contact-select').value;
    const c = contacts.find(x => x.id === cid);
    const html = `<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word"><head><meta charset="utf-8"><style>@page{{size:A4;margin:20mm 18mm;}}body{{font-family:"Segoe UI",Calibri,sans-serif;line-height:1.7;font-size:13px;color:#1a1a2e;white-space:pre-wrap;}}</style></head><body>${{t}}</body></html>`;
    const blob = new Blob([html], {{type:'application/msword'}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url;
    a.download = 'EOI_' + c.company.replace(/[^a-zA-Z0-9]/g, '_') + '.doc';
    document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
  }}

  function toggleDonor(row) {{
    row.classList.toggle('open');
    const detail = row.nextElementSibling;
    if (detail && detail.classList.contains('donor-detail')) detail.classList.toggle('open');
  }}

  // === STATE ===
  let state = {{}};

  function loadState() {{
    try {{ state = JSON.parse(localStorage.getItem('alessio_consult_state') || '{{}}'); }} catch(e) {{ state = {{}}; }}
    contacts.forEach(c => {{
      if (!state[c.id]) state[c.id] = {{ status: 'Not Registered', notes: '', message: c.message }};
    }});
  }}

  function saveState() {{
    localStorage.setItem('alessio_consult_state', JSON.stringify(state));
    const ind = document.getElementById('consult-save-indicator');
    ind.classList.add('show'); setTimeout(() => ind.classList.remove('show'), 1500);
  }}

  function exportData() {{
    const blob = new Blob([JSON.stringify(state, null, 2)], {{type: 'application/json'}});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a'); a.href = url;
    a.download = 'alessio_consulting_crm_backup.json';
    document.body.appendChild(a); a.click(); document.body.removeChild(a); URL.revokeObjectURL(url);
  }}

  function importData(e) {{
    const file = e.target.files[0]; if (!file) return;
    const r = new FileReader();
    r.onload = function(ev) {{
      try {{
        state = JSON.parse(ev.target.result);
        contacts.forEach(c => {{
          if (!state[c.id]) state[c.id] = {{ status: 'Not Registered', notes: '', message: c.message }};
        }});
        saveState(); renderContacts(); updateStats();
        alert('Imported successfully!');
      }} catch(err) {{ alert('Invalid file.'); }}
    }};
    r.readAsText(file);
  }}

  // === FILTERS ===
  let activeFilters = new Set();

  function toggleFilter(btn) {{
    const f = btn.dataset.filter;
    if (activeFilters.has(f)) {{ activeFilters.delete(f); btn.classList.remove('active'); }}
    else {{ activeFilters.add(f); btn.classList.add('active'); }}
    renderContacts();
  }}

  function passesFilter(c) {{
    const searchEl = document.querySelector('#consult-app .search-input');
    const search = searchEl ? searchEl.value.toLowerCase() : '';
    if (search && !c.name.toLowerCase().includes(search) && !c.company.toLowerCase().includes(search) && !c.title.toLowerCase().includes(search)) return false;
    const catF = [...activeFilters].filter(f => f.startsWith('cat-'));
    const statF = [...activeFilters].filter(f => f.startsWith('status-'));
    if (catF.length > 0 && !catF.some(f => f === 'cat-' + c.category)) return false;
    if (statF.includes('status-pending')) {{
      const s = (state[c.id] && state[c.id].status) || 'Not Registered';
      if (s !== 'Not Registered') return false;
    }}
    return true;
  }}

  // === RENDERING ===
  const catOrder = ['un','mdb','eu','firm','platform'];
  const catNames = {{un:'UN Agencies',mdb:'Multilateral Development Banks',eu:'EU & Bilateral Agencies',firm:'Consulting Firms',platform:'Platforms & Databases'}};
  const catColors = {{un:'#3b82f6',mdb:'#8b5cf6',eu:'#06b6d4',firm:'#f59e0b',platform:'#10b981'}};
  const regStatuses = ['Not Registered','Profile Created','Application Sent','Registered','Shortlisted','Active Engagement'];
  const regClasses = {{'Not Registered':'not-registered','Profile Created':'profile-created','Application Sent':'application-sent','Registered':'registered','Shortlisted':'shortlisted','Active Engagement':'active-engagement'}};

  function renderContacts() {{
    const container = document.getElementById('consult-contacts-container');
    container.innerHTML = '';
    const filtered = contacts.filter(passesFilter);
    catOrder.forEach(cat => {{
      const group = filtered.filter(c => c.category === cat);
      if (group.length === 0) return;
      group.sort((a, b) => a.priority - b.priority);
      const header = document.createElement('div'); header.className = 'cat-group-header';
      header.innerHTML = `<span class="cat-dot" style="background:${{catColors[cat]}}"></span> ${{catNames[cat]}} <span style="font-size:11px;color:var(--text-muted);font-weight:400;">(${{group.length}})</span>`;
      container.appendChild(header);
      group.forEach(c => {{
        const s = state[c.id] || {{}};
        const card = document.createElement('div'); card.className = 'contact-card';
        const statusClass = regClasses[s.status || 'Not Registered'];
        const priorityClass = c.priority <= 10 ? 'top' : '';
        card.innerHTML = `
          <div class="contact-main" data-mobile-info="${{c.company}} \\u00b7 ${{c.location}} \\u00b7 ${{s.status||'Not Registered'}}" onclick="ConsultCRM.toggleExpand('${{c.id}}')">
            <div class="priority-badge ${{priorityClass}}" data-tooltip="Priority #${{c.priority}}">${{c.priority}}</div>
            <div class="contact-info"><h3>${{c.name}}</h3><p>${{c.title}}</p></div>
            <div class="company-col">${{c.website?`<a href="${{c.website}}" target="_blank" style="color:var(--accent);text-decoration:none;font-size:12px;" onclick="event.stopPropagation()">${{c.company}}</a>`:c.company}}</div>
            <div><span class="cat-badge ${{c.category}}">${{c.category.toUpperCase()}}</span></div>
            <div class="location-col">${{c.location}}</div>
            <div><select class="reg-select ${{statusClass}}" onchange="ConsultCRM.updateStatus('${{c.id}}',this.value);event.stopPropagation();" onclick="event.stopPropagation();">
              ${{regStatuses.map(st=>`<option value="${{st}}" ${{(s.status||'Not Registered')===st?'selected':''}}>${{st}}</option>`).join('')}}
            </select></div>
            <div><button class="expand-btn" id="btn-${{c.id}}">&#9660;</button></div>
          </div>
          <div class="contact-expanded" id="exp-${{c.id}}">
            <div class="expanded-grid">
              <div class="expanded-section">
                <h4>How to Approach</h4>
                <div class="comm-tip">${{c.howToApproach}}</div>
                ${{c.registrationUrl?`<h4 style="margin-top:12px;">Registration Link</h4><div class="comm-tip"><a href="${{c.registrationUrl}}" target="_blank" style="color:var(--accent);">${{c.registrationUrl}}</a></div>`:''}}
                <h4 style="margin-top:12px;">Application Message (editable)</h4>
                <textarea onchange="ConsultCRM.updateMessage('${{c.id}}',this.value)">${{(s.message||c.message).replace(/</g,'&lt;')}}</textarea>
              </div>
              <div class="expanded-section">
                <h4>Notes</h4>
                <textarea class="notes-area" style="min-height:100px;" placeholder="Track registration progress..." onchange="ConsultCRM.updateNotes('${{c.id}}',this.value)">${{(s.notes||'').replace(/</g,'&lt;')}}</textarea>
                <div class="date-row"><label>Last action:</label><input type="date" value="${{s.lastAction||''}}" onchange="ConsultCRM.updateDate('${{c.id}}',this.value)"></div>
                <h4 style="margin-top:12px;">Details</h4>
                <div class="comm-tip">
                  <strong>Organization:</strong> ${{c.company}}<br>
                  ${{c.email?`<strong>Email:</strong> <a href="mailto:${{c.email}}" style="color:var(--accent);">${{c.email}}</a><br>`:''}}
                  <strong>Location:</strong> ${{c.location}}<br>
                  <strong>Category:</strong> ${{catNames[c.category]}}
                </div>
              </div>
            </div>
          </div>`;
        container.appendChild(card);
      }});
    }});
    updateStats();
  }}

  function toggleExpand(id) {{
    document.getElementById('exp-' + id).classList.toggle('open');
    document.getElementById('btn-' + id).classList.toggle('open');
  }}

  function updateStatus(id, val) {{
    state[id].status = val;
    if (!state[id].lastAction) state[id].lastAction = new Date().toISOString().slice(0,10);
    saveState(); renderContacts();
  }}

  function updateNotes(id, val) {{ state[id].notes = val; saveState(); }}
  function updateMessage(id, val) {{ state[id].message = val; saveState(); }}
  function updateDate(id, val) {{ state[id].lastAction = val; saveState(); }}

  function updateStats() {{
    const bar = document.getElementById('consult-stats-bar');
    const total = contacts.length;
    const registered = contacts.filter(c => state[c.id] && ['Registered','Shortlisted','Active Engagement'].includes(state[c.id].status)).length;
    const inProgress = contacts.filter(c => state[c.id] && ['Profile Created','Application Sent'].includes(state[c.id].status)).length;
    const active = contacts.filter(c => state[c.id] && state[c.id].status === 'Active Engagement').length;
    const pending = total - registered - inProgress - active;
    bar.innerHTML = `
      <div class="stat-card" data-tooltip="Total organizations"><div class="num">${{total}}</div><div class="label">Total</div></div>
      <div class="stat-card" data-tooltip="Not yet started"><div class="num" style="color:var(--text-muted)">${{pending}}</div><div class="label">Pending</div></div>
      <div class="stat-card" data-tooltip="In progress"><div class="num" style="color:var(--warning)">${{inProgress}}</div><div class="label">In Progress</div></div>
      <div class="stat-card" data-tooltip="Registered"><div class="num" style="color:var(--success)">${{registered}}</div><div class="label">Registered</div></div>
      <div class="stat-card" data-tooltip="Active engagements"><div class="num" style="color:var(--purple)">${{active}}</div><div class="label">Active</div></div>`;
  }}

  // === VIEWS ===
  function showView(v) {{
    ['consult-crm-view','consult-research-view','consult-donors-view','consult-cv-view','consult-guide-view'].forEach(id => {{
      const el = document.getElementById(id);
      if (el) el.style.display = id === 'consult-' + v + '-view' ? 'block' : 'none';
    }});
    const btns = {{
      research: {{id:'consult-toggle-research-btn',bg:'#6366f1',text:'Research'}},
      donors: {{id:'consult-toggle-donors-btn',bg:'#06b6d4',text:'Donors'}},
      cv: {{id:'consult-toggle-cv-btn',bg:'#10b981',text:'CV'}},
      guide: {{id:'consult-toggle-guide-btn',bg:'#f59e0b',text:'Help'}}
    }};
    Object.entries(btns).forEach(([key, cfg]) => {{
      const b = document.getElementById(cfg.id); if (!b) return;
      const active = v === key;
      b.style.background = active ? 'var(--bg)' : cfg.bg;
      b.style.color = active ? 'var(--text-muted)' : (key === 'guide' ? '#000' : '#fff');
      b.style.borderColor = active ? 'var(--border)' : cfg.bg;
      b.textContent = active ? 'Back to CRM' : cfg.text;
    }});
    window.scrollTo(0, 0);
  }}

  function toggleResearch() {{ showView(document.getElementById('consult-research-view').style.display !== 'none' ? 'crm' : 'research'); }}
  function toggleDonors() {{ showView(document.getElementById('consult-donors-view').style.display !== 'none' ? 'crm' : 'donors'); }}
  function toggleCV() {{
    const s = document.getElementById('consult-cv-view').style.display !== 'none';
    showView(s ? 'crm' : 'cv');
    if (!s) {{ switchCVVariant(document.getElementById('consult-cv-variant-select').value); populateCLContacts(); }}
  }}
  function toggleGuide() {{ showView(document.getElementById('consult-guide-view').style.display !== 'none' ? 'crm' : 'guide'); }}
  function showCRM() {{ showView('crm'); }}

  // Init
  loadState();

  return {{
    renderContacts, updateStats, toggleFilter, toggleResearch, toggleDonors, toggleCV, toggleGuide, showCRM,
    exportData, importData, downloadPDF, downloadWord, switchCVVariant,
    generateEOI, copyEOI, downloadEOIWord, toggleDonor,
    toggleExpand, updateStatus, updateNotes, updateMessage, updateDate,
    populateCLContacts
  }};
}})();
</script>
<div style="text-align:center;padding:24px 16px 16px;font-size:9px;color:var(--text-muted);opacity:0.6;letter-spacing:0.3px;">this project is made with love &mdash; Alessio, i believe in you</div>
</body>
</html>
"""

# Write the output
with open('deploy/index.html', 'w') as f:
    f.write(output)

print(f"Generated deploy/index.html ({len(output)} chars, {output.count(chr(10))} lines)")
