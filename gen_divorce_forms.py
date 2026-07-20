#!/usr/bin/env python3
"""
NYS Uncontested Divorce Forms — PDF Generator
Daniel N. Irving v. Julia Diaz Irving  |  Monroe County Supreme Court
NOT LEGAL ADVICE. Draft for Plaintiff's review before signing or filing.

Produces: divorce_forms_draft.pdf (combined UD-1a, UD-2, UD-6, UD-8(1))
UD-4 omitted — civil ceremony confirmed; UD-4 not required.
SSN lines are labeled by whose SSN belongs there — Dan fills in from tax records.
"""
import weasyprint, os

OUT = "/tmp/claude-0/-home-user-irving-calendar-sync/6fd42b43-244b-5d2b-a3d0-3f97d669668c/scratchpad/divorce_forms_draft.pdf"

CSS = """
@font-face { src: local('Times New Roman'); }
@page {
    size: letter;
    margin: 1in 1in 0.85in 1in;
    @bottom-center { content: counter(page); font-size: 9pt; font-family: serif; }
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: "Liberation Serif", "Times New Roman", Times, Georgia, serif;
       font-size: 12pt; line-height: 1.5; color: #000; background: #fff; }
.cover { page-break-after: always; padding: 0.5in 0.5in; }
.cover-title { font-size: 15pt; font-weight: bold; text-transform: uppercase;
               text-align: center; margin-bottom: 0.25in; }
.cover-sub { text-align: center; margin: 0.07in 0; font-size: 11pt; }
.wbox { border: 2px solid #000; padding: 0.18in; margin: 0.35in 0;
        font-size: 10.5pt; line-height: 1.4; }
.wbox p { margin: 0.07in 0; }
hr { border: none; border-top: 1px solid #000; margin: 0.1in 0; }
.form-start { page-break-before: always; }
.ct { text-align: center; font-weight: bold; text-transform: uppercase;
      font-size: 12pt; margin-bottom: 0.06in; }
.fn { text-align: center; font-size: 10pt; font-style: italic; margin-bottom: 0.1in; }
table.cap { width: 100%; border-collapse: collapse; margin: 0.06in 0 0.14in; }
table.cap td { border: 1px solid #000; padding: 0.06in 0.1in;
               vertical-align: top; font-size: 11pt; }
.cap-l { width: 62%; }
.cap-r { width: 38%; }
.pn { font-weight: bold; }
.pr { padding-left: 0.22in; font-style: italic; }
.vs { text-align: center; }
.ah { text-align: center; font-weight: bold; text-decoration: underline;
      text-transform: uppercase; margin: 0.04in 0 0.1in; }
p, .p { margin: 0.08in 0; }
.pb { font-weight: bold; display: inline; }
.i1 { margin-left: 0.4in; }
.i2 { margin-left: 0.8in; }
.bx { display: inline-block; width: 0.16in; height: 0.16in; border: 1px solid #000;
      vertical-align: middle; text-align: center; font-size: 9pt; font-weight: bold;
      line-height: 0.15in; margin: 0 0.04in; }
.bl { display: inline-block; border-bottom: 1px solid #000; vertical-align: bottom; min-width: 1.8in; }
.bls { min-width: 0.8in; }
.blm { min-width: 2.5in; }
.bll { min-width: 3.5in; }
.fi { font-weight: bold; }
.ni { display: inline-block; border-bottom: 2px dashed #555; min-width: 1.8in;
      font-style: italic; font-size: 10pt; color: #333; vertical-align: bottom; }
.nis { min-width: 0.9in; }
.ssn { display: inline-block; border-bottom: 1px solid #000; min-width: 1.55in;
       font-family: monospace; font-size: 10.5pt; vertical-align: bottom;
       letter-spacing: 0.04in; }
.sig { margin-top: 0.35in; border-top: 1px solid #000; padding-top: 0.08in; }
.sig-row { display: flex; gap: 0.4in; margin-top: 0.2in; }
.sig-col { flex: 1; }
.sig-line { border-bottom: 1px solid #000; min-height: 0.28in; }
.sig-lbl { font-size: 9.5pt; text-align: center; margin-top: 0.04in; }
.note { border-left: 3px solid #000; padding: 0.06in 0.12in; margin: 0.1in 0;
        font-size: 10pt; font-style: italic; }
.ni-box { border: 1px dashed #777; padding: 0.06in 0.1in; margin: 0.07in 0;
           font-size: 10pt; font-style: italic; color: #333; }
.warn { border: 2px solid #555; padding: 0.06in 0.12in; margin: 0.1in 0;
        font-size: 10pt; font-style: italic; background: #f9f9f9; }
.sec { font-weight: bold; text-decoration: underline; margin: 0.15in 0 0.07in; }
.or { text-align: center; font-weight: bold; margin: 0.04in 0; }
table.fin { width: 100%; border-collapse: collapse; margin: 0.1in 0; font-size: 11pt; }
table.fin th, table.fin td { border: 1px solid #000; padding: 0.04in 0.08in; }
table.fin th { background: #eee; text-align: center; font-weight: bold; font-size: 10.5pt; }
table.fin td.d { width: 56%; }
table.fin td.p { width: 22%; text-align: right; }
table.fin td.q { width: 22%; text-align: right; }
"""

# ─── helpers ────────────────────────────────────────────────────────────────
def cb(c=False): return f'<span class="bx">{"X" if c else "&nbsp;"}</span>'
def bl(s=''): return f'<span class="bl{(" b"+s) if s else ""}"> &nbsp;</span>'
def bls(): return '<span class="bl bls">&nbsp;</span>'
def fi(t): return f'<span class="fi">{t}</span>'
def ni(t=''): return f'<span class="ni">&lt;{t or "NEEDS INPUT"}&gt;</span>'
def ssn(who): return f'<span class="ssn">&nbsp;[{who} SSN — fill from tax records]&nbsp;</span>'

def cap(extra=''):
    return f"""<table class="cap"><tr>
  <td class="cap-l">
    <div class="pn">DANIEL N. IRVING,</div>
    <div class="pr">Plaintiff,</div>
    <div class="vs">&ndash;against&ndash;</div>
    <div class="pn">JULIA DIAZ IRVING,</div>
    <div class="pr">Defendant.</div>
  </td>
  <td class="cap-r">
    Index No.: {bl()}<br>
    {extra}
  </td>
</tr></table>"""

def notary(who="Plaintiff"):
    return f"""
<div class="sig">
<p>Subscribed and Sworn to before me on {bl()}</p>
<div class="sig-row" style="margin-top:0.2in;">
  <div class="sig-col"><div class="sig-line"></div>
    <div class="sig-lbl">{who}&rsquo;s Signature</div></div>
  <div class="sig-col"><div class="sig-line"></div>
    <div class="sig-lbl">NOTARY PUBLIC</div></div>
</div></div>"""

def ct():
    return '<div class="ct">Supreme Court of the State of New York<br>County of Monroe</div>'

# ─── Party / address constants ────────────────────────────────────────────────
DAN_ADDR  = fi('275 Alexander St, Apt 2, Rochester, NY 14607')
JULIA_ADDR = fi('28 Penbrooke Dr, Penfield, NY 14625')
PRIOR_ADDR = fi('20 Landing Rd S, Rochester, NY 14610')

# ─── COVER ──────────────────────────────────────────────────────────────────
COVER = f"""
<div class="cover">
<div class="cover-title">NYS Uncontested Divorce &mdash; Court Papers<br>
<span style="font-size:12pt;">Draft &mdash; For Plaintiff&rsquo;s Review Before Signing or Filing</span></div>
<div class="cover-sub"><strong>Plaintiff:</strong> Daniel N. Irving &nbsp;|&nbsp;
  <strong>Defendant:</strong> Julia Diaz Irving</div>
<div class="cover-sub">Supreme Court of the State of New York &bull; Monroe County</div>
<div class="cover-sub" style="font-style:italic;">Prepared July 2026 &mdash; Draft v4</div>
<div class="wbox">
<p><strong>NOT LEGAL ADVICE.</strong> These forms are filled with confirmed facts only.
True underline blanks (<span style="display:inline-block;border-bottom:1px solid #000;
min-width:0.7in;">&nbsp;</span>) require information Dan enters directly.
Dashed italic labels (<span style="display:inline-block;border-bottom:2px dashed #555;
font-style:italic;font-size:10pt;min-width:1in;">&lt;NEEDS INPUT&gt;</span>) require
a decision or confirmation before this line can be signed.
SSN lines are labeled — transcribe from your own tax records, do not type through this
document. Review with an attorney or NY&rsquo;s free DIY Divorce navigator
(nycourts.gov/divorce) before signing, serving, or filing.</p>
<hr>
<p><strong>Confirmed facts incorporated in this version (v3):</strong><br>
Plaintiff: Daniel N. Irving &bull; DOB 08/15/1973 &bull; 275 Alexander St Apt 2, Rochester NY 14607<br>
Defendant: Julia Diaz Irving &bull; 28 Penbrooke Dr, <strong>Penfield</strong>, NY 14625<br>
Marriage: October 5, 2002 &bull; <strong>Glendoveer&rsquo;s</strong>, Brighton, NY &bull;
<strong>Civil ceremony</strong> (UD-4 Barriers to Remarriage is NOT required and is omitted from this packet)<br>
Children: Magnolia Z. Irving (DOB 01/06/2010, lives with Defendant) &bull;
Hazel E. Irving (DOB 03/06/2013, joint schedule)<br>
Prior family home: 20 Landing Rd S, Rochester, NY 14610 (approx. until 2022&ndash;2023)<br>
Custody: Joint legal custody of both children; primary physical with Defendant for Magnolia;
joint physical for Hazel per existing schedule<br>
Magnolia parenting time: Option A &mdash; &ldquo;to be determined upon agreement of the parties or petition to the court&rdquo;<br>
UD-6 &sect;6b: <strong>Box B selected</strong> &mdash; court will determine all unsettled issues<br>
Property: equitable distribution requested (court decides); former marital home foreclosed;
Julia&rsquo;s pension + possible 401(k) are marital assets; QDRO required<br>
Maintenance: Plaintiff seeks guideline maintenance per DRL &sect;236(B)(6)<br>
No prior custody proceedings &bull; Defendant not in military service<br>
Records: No Orders of Protection, no FCA Art. 10, not on Sex Offender registry<br>
Plaintiff&rsquo;s income: <strong>SSDI $2,306.17/mo &times; 12 = $27,674.04/yr</strong> &bull;
Health: Plaintiff on Medicaid; children on CHP<br>
Defendant&rsquo;s income: <strong>UNKNOWN &mdash; BLOCKS UD-8(2) and UD-8(3)</strong></p>
<hr>
<p><strong>Still needed before any form can be signed:</strong><br>
&bull; Julia&rsquo;s health plan &mdash; unknown to Plaintiff (affects UD-2 &sect;FOURTH and UD-6 &sect;4 health boxes)<br>
&bull; Property: court will decide equitable distribution (Box B); former marital home foreclosed;
Julia&rsquo;s pension and possible 401(k) are marital assets &mdash; <strong>QDRO required; attorney strongly recommended</strong><br>
&bull; Maintenance: Plaintiff is seeking guideline maintenance; amount blocked pending Julia&rsquo;s income<br>
&bull; All 4 SSN fields &mdash; fill by hand from tax records (Dan, Magnolia, Hazel, Julia)<br>
&bull; <strong>Julia&rsquo;s income &mdash; blocks UD-8(2) and UD-8(3)</strong></p>
<hr>
<p><strong>Forms in this packet:</strong><br>
UD-1a &mdash; Summons &nbsp;&bull;&nbsp;
UD-2 &mdash; Verified Complaint &nbsp;&bull;&nbsp;
UD-6 &mdash; Affidavit of Plaintiff &nbsp;&bull;&nbsp;
UD-8(1) &mdash; Annual Income Worksheet (Plaintiff side only)</p>
<p><strong>Forms NOT in this packet:</strong><br>
UD-4 (not required &mdash; <strong>civil ceremony confirmed</strong>) &bull;
UD-3/4a (require service of process) &bull; UD-5 (requires Julia&rsquo;s appearance or default) &bull;
UD-7 (Julia&rsquo;s own form) &bull; UD-8(2)/8(3) (require Julia&rsquo;s income) &bull;
UD-9&ndash;14 (court stage &mdash; require index number and settled or ordered terms)</p>
</div></div>"""

# ─── UD-1a: SUMMONS ──────────────────────────────────────────────────────────
UD1A = f"""
<div class="form-start">
{ct()}
<div class="fn">(Form UD-1a Rev. 5/99)</div>
{cap()}
<div class="ah">Summons &mdash; Action for Divorce</div>

<p>Plaintiff designates {fi('MONROE')} County as the place of trial.</p>
<p>The basis of venue is: Residence of the parties &mdash; both Plaintiff and Defendant
currently reside in Monroe County, New York, and the marital residence was also in
Monroe County, New York.</p>
<p>Plaintiff resides at: {DAN_ADDR}</p>
<p>Defendant resides at: {JULIA_ADDR}</p>

<p style="text-align:center; font-weight:bold; margin:0.2in 0;">
&mdash; ACTION FOR A DIVORCE &mdash;</p>

<p>To the above named Defendant:</p>
<p><strong>YOU ARE HEREBY SUMMONED</strong> to answer the complaint in this action and to serve
a copy of your answer on the {cb(True)}&nbsp;Plaintiff &nbsp;&nbsp;{cb()}&nbsp;Plaintiff&rsquo;s
Attorney(s) within twenty (20) days after the service of this summons, exclusive of the day
of service, where service is made by delivery upon you personally within the state, or within
thirty (30) days after completion of service where service is made in any other manner. In case
of your failure to appear or answer, judgment will be taken against you by default for the relief
demanded in the complaint.</p>

<p><em><strong>NOTICE:</strong> The nature of this action is to dissolve the marriage between
the parties, on the ground of irretrievable breakdown of the marriage relationship pursuant to
Subdivision (7) of Section 170 of the Domestic Relations Law.</em></p>

<p><em>YOUR FAILURE TO APPEAR OR RESPOND TO THIS SUMMONS WILL RESULT IN A COURT ORDER OF
DIVORCE WITH DECISIONS MADE BY THE COURT ABOUT ALL OF THE FOLLOWING: EQUITABLE DISTRIBUTION
OF YOUR PROPERTY AND DEBTS; SPOUSAL SUPPORT (ALSO CALLED MAINTENANCE); CHILD SUPPORT; CHILD
CUSTODY AND CHILD VISITATION; AND ATTORNEY FEES AND COSTS, TO THE EXTENT THAT THESE ISSUES ARE
NOT RESOLVED BY A WRITTEN AGREEMENT BETWEEN THE PARTIES THAT IS SUBMITTED TO THE COURT.</em></p>

<div class="sig">
<p>Dated: {bl()}</p>
<div class="sig-row" style="margin-top:0.25in;">
  <div class="sig-col">
    <div class="sig-line"></div>
    <div class="sig-lbl">{cb(True)}&nbsp;Plaintiff &nbsp; {cb()}&nbsp;Attorney(s) for Plaintiff</div>
  </div>
</div>
<p style="margin-top:0.15in;">Phone No.: {fi('585-202-7321')}</p>
<p>Address: {DAN_ADDR}</p>
</div>

<div class="note" style="margin-top:0.2in;">
<strong>Note:</strong> File UD-1a together with UD-2 (Verified Complaint) with the Monroe County Clerk.
The Clerk assigns the Index Number; enter it in the caption blank on all forms. Date on the signature
line = date Dan actually signs. &ldquo;Date Summons filed&rdquo; on UD-9 = the date filed with the Clerk.
</div>
</div>"""

# ─── UD-2: VERIFIED COMPLAINT ────────────────────────────────────────────────
UD2 = f"""
<div class="form-start">
{ct()}
<div class="fn">(Form UD-2 Rev. 1/25/16)</div>
{cap()}
<div class="ah">Verified Complaint &mdash; Action for Divorce</div>

<p><span class="pb">FIRST:</span> Plaintiff herein, complaining of the Defendant,
alleges that the parties are over the age of 18 years and;</p>

<p><span class="pb">SECOND:</span></p>
<p class="i1">{cb(True)}&nbsp;A) The {cb(True)}&nbsp;Plaintiff {cb()}&nbsp;Defendant has
resided in New York State for a continuous period of at least two (2) years immediately
preceding the commencement of this divorce action.</p>
<div class="note">Box A checked. Dan confirmed no gaps in NY residency &mdash; continuous Monroe County
resident well beyond the 2-year requirement. No alternative box needed.</div>
<p class="i1 or">OR</p>
<p class="i1">{cb()}&nbsp;B) The {cb()}&nbsp;Plaintiff {cb()}&nbsp;Defendant resided in New York
State on the date of commencement and for a continuous period of one year immediately preceding,
AND: a.&nbsp;{cb()}&nbsp;parties were married in NY, or b.&nbsp;{cb()}&nbsp;parties resided as
married persons in NY.</p>
<p class="i1 or">OR</p>
<p class="i1">{cb()}&nbsp;C) The cause of action occurred in New York State and {cb()}&nbsp;Plaintiff
{cb()}&nbsp;Defendant resided in NY for at least one year immediately preceding commencement.</p>
<p class="i1 or">OR</p>
<p class="i1">{cb()}&nbsp;D) The cause of action occurred in New York State and both parties were
residents at the time of commencement.</p>

<p><span class="pb">THIRD:</span> The Plaintiff and the Defendant were married on
{fi('October 5, 2002')}, in {fi('Glendoveer&rsquo;s')},
{fi('Brighton, New York')}.</p>
<p class="i1">The marriage was <strong>not</strong> performed by a clergyman, minister or
leader of the Society for Ethical Culture.</p>
<div class="note"><strong>Civil ceremony confirmed.</strong> The sentence above correctly reads
&ldquo;was NOT performed by a clergyman...&rdquo; Form UD-4 (Barriers to Remarriage) is
<strong>NOT required</strong> and is omitted from this packet. Verify &ldquo;Glendoveer&rsquo;s&rdquo;
spelling against the marriage certificate before signing.</div>

<p><span class="pb">FOURTH:</span> {cb()}&nbsp;There are no children of the marriage &nbsp; OR<br>
{cb(True)}&nbsp;There is(are) {fi('2')} child(ren) of the marriage, namely:</p>
<table class="fin" style="margin-left:0.3in;width:95%;">
<tr><th>Name</th><th>Date of Birth</th><th>Social Security No.</th></tr>
<tr><td>{fi('Magnolia Z. Irving')}</td><td>{fi('January 6, 2010')}</td>
    <td>{ssn('Magnolia')}</td></tr>
<tr><td>{fi('Hazel E. Irving')}</td><td>{fi('March 6, 2013')}</td>
    <td>{ssn('Hazel')}</td></tr>
</table>
<p class="i1">The Plaintiff resides at: {DAN_ADDR}</p>
<p class="i1">The Defendant resides at: {JULIA_ADDR}</p>
<p class="i1">The parties are covered by the following group health plans:</p>
<p class="i2">Plaintiff: {fi('Medicaid')} <em>(government program &mdash; children covered by Child Health Plus/CHP under Plaintiff)</em></p>
<p class="i2">Defendant: {ni('Julia&rsquo;s health plan &mdash; unknown to Plaintiff')}</p>
<p class="i2">{cb()}&nbsp;Not Applicable &nbsp; {cb()}&nbsp;No health plans available through employment</p>
<div class="note">Medicaid and CHP are government programs, not employer-sponsored group health plans.
If neither party has an <em>employer</em> group plan, check &ldquo;No health plans available
through employment&rdquo; and note government coverage separately. Confirm correct box with DIY
navigator or attorney. Defendant&rsquo;s health coverage is unknown to Plaintiff.</div>

<p><span class="pb">FIFTH:</span> The grounds for divorce alleged are as follows:</p>
<p class="i1"><em>Irretrievable Breakdown in Relationship for at Least Six Months (DRL &sect;170(7)):</em></p>
<p class="i1">{cb(True)}&nbsp;That the relationship between Plaintiff and Defendant has broken down
irretrievably for a period of at least six (6) months.</p>
<div class="note">Only DRL &sect;170(7) is alleged. DRL &sect;170(1)&ndash;(6) are not checked.</div>

<p><span class="pb">SIXTH:</span> There is no judgment of divorce and no other matrimonial action
between the parties pending in this court or in any other court of competent jurisdiction.
<em>[Dan to confirm this is true before signing.]</em></p>

<p style="margin-top:0.15in;"><span class="pb">WHEREFORE,</span> Plaintiff demands judgment
against the Defendant as follows: A judgment dissolving the marriage between the parties AND
the following ancillary relief:</p>
<div class="ni-box">
<p><strong>Custody:</strong> Joint legal custody of {fi('Magnolia Z. Irving')} and {fi('Hazel E. Irving')}.</p>
<p>Primary physical custody of {fi('Magnolia Z. Irving')} with Defendant.
{fi('Plaintiff&rsquo;s parenting time with Magnolia Z. Irving to be determined upon agreement of the parties or petition to the court.')}</p>
<p>Joint physical custody of {fi('Hazel E. Irving')}: with Plaintiff {fi('every other weekend, every Monday, every Tuesday until 4:00 p.m., and every Sunday')}; remaining time with Defendant.</p>
<p>Child support pursuant to CSSA: {ni('BLOCKED &mdash; Defendant&rsquo;s income required; no amount entered')}</p>
<p>Plaintiff to claim {fi('Hazel E. Irving')} as tax dependent: {ni('pending Defendant&rsquo;s agreement')}</p>
</div>

<p class="i1">{cb(True)}&nbsp;Additional page describing ancillary relief is attached.</p>
<p class="i1"><strong>Marital property:</strong> Neither standard box below is checked because Plaintiff
is <em>requesting equitable distribution through the court</em> (Box B), not waiving it and not
proceeding under a settlement agreement. The additional-page checkbox above is checked to
flag this to the court.</p>
<p class="i1">{cb()}&nbsp;Property distributed per separation agreement/stipulation &nbsp; OR
{cb()}&nbsp;I waive distribution of marital property.</p>
<div class="note"><strong>Property confirmed:</strong> Former marital home (20 Landing Rd S) was
foreclosed &mdash; no equity to divide. Julia has a pension and possibly a 401(k) accumulated
during the marriage; both are marital assets subject to equitable distribution. A QDRO
(Qualified Domestic Relations Order) will be required to divide any pension or 401(k).
<strong>Attorney assistance is strongly recommended before proceeding to judgment on property
issues.</strong> Dan does NOT waive distribution.</div>
<p class="i1"><strong>Maintenance:</strong> {cb()}&nbsp;I am not seeking maintenance as payee &nbsp; OR
{cb(True)}&nbsp;I seek maintenance as payee as described in the Notice of Guideline Maintenance.</p>
<div class="note">Maintenance box checked: Plaintiff seeks guideline maintenance. Whether Plaintiff
qualifies and the amount depend on both parties&rsquo; incomes under DRL &sect;236(B)(6).
With Plaintiff&rsquo;s income at $27,674/yr (SSDI) and Defendant employed (income unknown),
Plaintiff likely qualifies &mdash; but the exact figure cannot be calculated until
Julia&rsquo;s income is confirmed. Checking this box preserves the claim; it can be waived
before judgment if the parties later agree or the formula yields $0.</div>
<p class="i1">{cb()}&nbsp;NONE &mdash; I am not requesting any ancillary relief. <em>[Do NOT check if seeking custody, support, or property relief above.]</em></p>
<p class="i1">AND any other relief the court deems fit and proper.</p>

<p>Dated: {bl()}</p>
<p>{cb(True)}&nbsp;Plaintiff &nbsp; {cb()}&nbsp;Attorney(s) for Plaintiff</p>
<p>Address: {DAN_ADDR}</p>

<p style="margin-top:0.2in;"><strong>VERIFICATION</strong></p>
<p>STATE OF NEW YORK, COUNTY OF MONROE, ss:</p>
<p>I, {fi('Daniel N. Irving')}, am the Plaintiff in the within action for a divorce. I have read
the foregoing complaint and know the contents thereof. The contents are true to my own knowledge
except as to matters therein stated to be alleged upon information and belief, and as to those
matters I believe them to be true.</p>
{notary()}
</div>"""

# UD-4 (Barriers to Remarriage) is OMITTED — civil ceremony confirmed.
# Not required when marriage was not performed by a clergyman/minister.

# ─── UD-6: AFFIDAVIT OF PLAINTIFF ────────────────────────────────────────────
UD6 = f"""
<div class="form-start">
{ct()}
<div class="fn">(Form UD-6 Rev. 1/25/16)</div>
{cap()}
<div class="ah">Affidavit of Plaintiff</div>

<p>{fi('Daniel N. Irving')}, being duly sworn, says:</p>

<p><span class="pb">1.</span> The Plaintiff&rsquo;s address is {DAN_ADDR},
and social security number is {ssn('Dan&rsquo;s')}. The Defendant&rsquo;s address is
{JULIA_ADDR}, and social security number is {ssn('Julia&rsquo;s')}.</p>

<p><span class="pb">2.</span></p>
<p class="i1">{cb(True)}&nbsp;A) The {cb(True)}&nbsp;Plaintiff {cb()}&nbsp;Defendant has resided
in New York State for a continuous period of at least two (2) years immediately preceding the
commencement of this divorce action.
<em>[Confirmed: no gaps in NY residency.]</em></p>
<p class="i1 or">OR</p>
<p class="i1">{cb()}&nbsp;B) The {cb()}&nbsp;Plaintiff {cb()}&nbsp;Defendant resided in NY on
commencement date and for one year immediately preceding AND: a.{cb()}&nbsp;parties married in NY
or b.{cb()}&nbsp;parties resided as married persons in NY.</p>
<p class="i1 or">OR</p>
<p class="i1">{cb()}&nbsp;C) Cause of action occurred in NY and {cb()}&nbsp;Plaintiff
{cb()}&nbsp;Defendant resided in NY for at least one year preceding commencement.</p>
<p class="i1 or">OR</p>
<p class="i1">{cb()}&nbsp;D) Cause of action occurred in NY and both parties were NY residents at
commencement.</p>

<p><span class="pb">3.</span> I married the Defendant on {fi('October 5, 2002')}, in the City, Town
or Village of {fi('Brighton')}, County of {fi('Monroe')}, State of {fi('New York')}.
The marriage was <strong>not</strong> performed by a clergyman, minister or by a leader of the
Society for Ethical Culture. <em>[Civil ceremony confirmed. Verify &ldquo;Glendoveer&rsquo;s&rdquo;
venue spelling against marriage certificate.]</em></p>

<p><span class="pb">4.</span> There is(are) {fi('2')} child(ren) of the marriage under the age
of 21:</p>
<table class="fin" style="margin-left:0.3in;width:95%;">
<tr><th>Name &amp; Social Security Number</th><th>Date of Birth</th></tr>
<tr><td>{fi('Magnolia Z. Irving')} &mdash; SSN: {ssn('Magnolia')}</td>
    <td>{fi('January 6, 2010')}</td></tr>
<tr><td>{fi('Hazel E. Irving')} &mdash; SSN: {ssn('Hazel')}</td>
    <td>{fi('March 6, 2013')}</td></tr>
</table>

<p class="i1">The present address of each minor child and all places where each has lived
within the last five (5) years:</p>
<p class="i2">{fi('Magnolia Z. Irving')}: {fi('28 Penbrooke Dr, Penfield, NY 14625')} (current, with Defendant);
{PRIOR_ADDR} (former family home, approx. until 2022&ndash;2023)</p>
<p class="i2">{fi('Hazel E. Irving')}: {fi('275 Alexander St, Apt 2, Rochester, NY 14607')} (with Plaintiff)
AND {fi('28 Penbrooke Dr, Penfield, NY 14625')} (with Defendant);
{PRIOR_ADDR} (former family home, approx. until 2022&ndash;2023)</p>
<div class="note">Prior family home 20 Landing Rd S, Rochester, NY 14610 confirmed from 2021 tax
records. Move-out approximately 2022&ndash;2023 (exact date to be confirmed by Dan before signing).
Both children lived there with both parents before the current arrangements.</div>

<p class="i1">The name(s) and present address(es) of the person(s) with whom each minor child
has lived within the last five (5) years:</p>
<p class="i2">{fi('Magnolia Z. Irving')} has lived with: {fi('Julia Diaz Irving, 28 Penbrooke Dr, Penfield, NY 14625')} (current);
{fi('Daniel N. Irving and Julia Diaz Irving, 20 Landing Rd S, Rochester, NY 14610')} (approx. until 2022&ndash;2023)</p>
<p class="i2">{fi('Hazel E. Irving')} has lived with: {fi('Daniel N. Irving, 275 Alexander St, Apt 2, Rochester, NY 14607')}
AND {fi('Julia Diaz Irving, 28 Penbrooke Dr, Penfield, NY 14625')} (current joint schedule);
{fi('Daniel N. Irving and Julia Diaz Irving, 20 Landing Rd S, Rochester, NY 14610')} (approx. until 2022&ndash;2023)</p>

<p class="i1">I have participated in other litigation concerning the custody of the minor
child(ren) in this or another state. {cb()}&nbsp;Yes &nbsp; {cb(True)}&nbsp;No</p>
<p class="i1">I have information of a custody proceeding concerning the minor child(ren) pending
in a court of this or another state. {cb()}&nbsp;Yes &nbsp; {cb(True)}&nbsp;No</p>
<p class="i1">I know of a person not a party to this proceeding who has physical custody or
claims custody or visitation rights with respect to such child(ren).
{cb()}&nbsp;Yes &nbsp; {cb(True)}&nbsp;No <em>[Dan confirmed no prior custody proceedings.]</em></p>

<p class="i1">The parties are covered by the following group health plans:</p>
<p class="i2">Plaintiff: {fi('Medicaid')} <em>(children covered by Child Health Plus/CHP under Plaintiff)</em></p>
<p class="i2">Defendant: {ni('Julia&rsquo;s health plan &mdash; unknown to Plaintiff')}</p>
<p class="i2">{cb()}&nbsp;Not Applicable. &nbsp;{cb()}&nbsp;No health plans available through employment.
<em>[See note on UD-2 &sect;FOURTH re: Medicaid vs. employer group plan.]</em></p>

<p><span class="pb">5.</span> The grounds for dissolution of the marriage are as follows:</p>
<p class="i1"><em>Irretrievable Breakdown in Relationship for at Least Six Months (DRL
&sect;170(7)):</em></p>
<p class="i1">{cb(True)}&nbsp;That the relationship between Plaintiff and Defendant has broken
down irretrievably for a period of at least six (6) months.</p>
<div class="note">Only DRL &sect;170(7) is alleged. DRL &sect;170(1)&ndash;(6) are not checked.</div>

<p><span class="pb">6a.</span> In addition to the dissolution of the marriage, I am seeking the
following ancillary relief:</p>
<div class="ni-box">
Joint legal custody of {fi('Magnolia Z. Irving')} and {fi('Hazel E. Irving')}.<br>
Primary physical custody of {fi('Magnolia Z. Irving')} with Defendant.
{fi('Plaintiff&rsquo;s parenting time with Magnolia Z. Irving to be determined upon agreement of the parties or petition to the court.')}<br>
Joint physical custody of {fi('Hazel E. Irving')}: with Plaintiff
{fi('every other weekend, every Monday, every Tuesday until 4:00 p.m., and every Sunday')};
remaining time with Defendant.<br>
Child support per CSSA: {ni('BLOCKED &mdash; Defendant&rsquo;s income required')}<br>
Guideline maintenance payable to Plaintiff per DRL &sect;236(B)(6): amount to be determined upon
disclosure of Defendant&rsquo;s income.<br>
{fi('Hazel E. Irving')} as Plaintiff&rsquo;s tax dependent: {ni('pending Defendant&rsquo;s agreement')}
</div>

<p><span class="pb">6b.</span> Since DRL &sect;170 subd. (7) is the ground alleged,
<strong>Plaintiff must check Box A, B, C, or D</strong> (only one):</p>
<p class="i1">{cb()}&nbsp;<strong>A.</strong> All economic issues and custody/visitation have been
resolved by the parties and are to be incorporated into the Judgment of Divorce &mdash; by
{cb()}&nbsp;oral settlement/stipulation on the record, or by {cb()}&nbsp;written
Settlement/Separation Agreement.</p>
<p class="i1">{cb(True)}&nbsp;<strong>B.</strong> Will be determined by the Court and incorporated into
the Judgment of Divorce.</p>
<p class="i1">{cb()}&nbsp;<strong>C.</strong> Were determined by Family Court order (custody/visitation
or child/spousal support only) which will be continued. <em>[N/A &mdash; no prior Family Court order.]</em></p>
<p class="i1">{cb()}&nbsp;<strong>D.</strong> Are not to be incorporated into the Judgment of Divorce,
since neither party has contested any such issues.</p>
<div class="note"><strong>Box B selected</strong> (confirmed by Plaintiff): The court will determine
all unsettled economic issues and custody/visitation terms. No written settlement agreement with
Defendant exists; mediation did not produce a finalized agreement. Box C eliminated (no prior
Family Court order). Box D not applicable (child support and property remain unresolved).
Box A available only if a written agreement with Julia is later signed and attached.</div>

<p><span class="pb">7.</span> {cb()}&nbsp;The Defendant is in the military service and
{cb()}&nbsp;has {cb()}&nbsp;has not waived rights under the Soldiers&rsquo; and Sailors&rsquo;
Civil Relief Act.</p>
<p class="or">OR</p>
<p>{cb(True)}&nbsp;Defendant is <strong>not</strong> in the active military service of this state,
any other state, or this nation. <em>[Confirmed by Plaintiff.]</em></p>

<p><span class="pb">8.</span> I am not receiving Public Assistance. To my knowledge the Defendant
is not receiving Public Assistance.
<span class="note" style="display:inline;border:none;padding:0;">
[Note: Dan&rsquo;s SSDI is federal disability insurance on his own work record &mdash; legally
distinct from &ldquo;Public Assistance&rdquo; (welfare/TANF); this statement is accurate for Dan.
Confirm Julia&rsquo;s status before signing.]</span></p>

<p><span class="pb">9.</span> No other matrimonial action is pending in this court or in any other
court, and the marriage has not been terminated by any decree of any court of competent jurisdiction.
<em>[Dan to confirm before signing.]</em></p>

<p><span class="pb">10.</span> Annexed to the &ldquo;Affidavit of Service&rdquo; of Summons and
Complaint is a photograph. It is a fair and accurate representation of the Defendant.
<em>[Applicable once service occurs &mdash; photograph is attached to UD-3, not here.]</em></p>

<p><span class="pb">11.</span></p>
<p class="i1">{cb(True)}&nbsp;<strong>11A.</strong> I am <strong>not</strong> the custodial parent
of the unemancipated child(ren) of the marriage.</p>
<p class="or">OR</p>
<p class="i1">{cb()}&nbsp;<strong>11B.</strong> I am the custodial parent of the unemancipated
child(ren) of the marriage entitled to receive child support pursuant to DRL &sect;236(B)(7)(b),
AND:</p>
<p class="i2">{cb()}&nbsp;(1) I request child support services through the Support Collection Unit (SCU)...</p>
<p class="i2">{cb()}&nbsp;(2) I am in receipt of SCU services and will continue to receive them...</p>
<p class="i2">{cb()}&nbsp;(3) I have applied for SCU services...</p>
<p class="i2">{cb()}&nbsp;(4) I am aware of but decline SCU services at this time.</p>
<div class="note"><strong>11A checked:</strong> Magnolia lives primarily with Defendant (Julia),
and Hazel&rsquo;s overnights give Defendant more time (~64%). For CSSA purposes Defendant is the
&ldquo;custodial parent.&rdquo; Plaintiff (Dan) is the non-custodial parent who may owe child support
to Defendant once Julia&rsquo;s income is known. Confirm this is your understanding before signing.
If you believe the overnight split entitles you to be treated as custodial parent for Hazel,
consult an attorney or DIY navigator before checking 11A.</div>

<p><span class="pb">21.</span> {cb()}&nbsp;Plaintiff&rsquo;s {cb()}&nbsp;Defendant&rsquo;s prior
surname is: {bl()}
<em>[Check only if either party is requesting to resume a prior surname. Julia&rsquo;s maiden name
is Diaz &mdash; if she wishes to resume it, she would note that in UD-7. Dan: do you wish to resume
any prior surname?]</em></p>

<p class="sec">Pursuant to DRL &sect;240 1(a-1) &mdash; Records Checking Requirements:</p>
<p>An Order of Protection {cb()}&nbsp;has &nbsp; {cb(True)}&nbsp;has never been issued
against me, enjoining me or requiring my compliance.</p>
<p>An Order of Protection {cb()}&nbsp;has &nbsp; {cb(True)}&nbsp;has never been issued
in favor of or protecting me, my child(ren), or a member of my household.</p>
<p>List all Family/Criminal Court Docket #&rsquo;s and Counties: {bl()}&nbsp;&nbsp;&nbsp;
Supreme Court Index #&rsquo;s and Counties: {bl()}</p>
<p>{cb()}&nbsp;I or my child(ren) or my spouse has been named in a Child Abuse/Neglect
Proceeding (FCA Art. 10) &mdash; Docket #&rsquo;s: {bls()} Counties: {bls()}</p>
<p>{cb(True)}&nbsp;I or my child(ren) or my spouse has <strong>never</strong> been named in a
Child Abuse/Neglect Proceeding (FCA Art. 10)</p>
<p>{cb()}&nbsp;I am registered under New York State&rsquo;s Sex Offender Registration Act
&mdash; names registered under: {bl()}</p>
<p>{cb(True)}&nbsp;I am <strong>not</strong> registered under New York State&rsquo;s Sex Offender
Registration Act</p>

<p><span class="pb">22.</span> {cb()}&nbsp;I acknowledge receipt of the Notice of Guideline
Maintenance from the Court. <em>[Check this box at filing after the Monroe County Clerk
provides the Notice of Guideline Maintenance &mdash; do not check until you have actually
received it.]</em></p>
<p><span class="pb">23.</span> {cb()}&nbsp;I have been provided a copy of the Notice Relating
to Health Care of the Parties.</p>

<p style="margin-top:0.15in;"><strong>WHEREFORE,</strong> I, {fi('Daniel N. Irving')},
respectfully request that judgment be entered for the relief sought herein and for such other
relief as the court deems fitting and proper.</p>

{notary()}
</div>"""

# ─── UD-8(1): ANNUAL INCOME WORKSHEET ────────────────────────────────────────
UD81 = f"""
<div class="form-start">
{ct()}
<div class="fn">(Form UD-8(1) Rev. 1/31/16 &mdash; Annual Income Worksheet / Appendix A)</div>
{cap()}
<div class="ah">Annual Income Worksheet</div>

<p>This Worksheet was prepared by {cb(True)}&nbsp;Plaintiff &nbsp; {cb()}&nbsp;Defendant</p>

<div class="note">Per the form&rsquo;s own instructions: &ldquo;If you do not know your
spouse&rsquo;s income write &lsquo;unknown.&rsquo;&rdquo; Julia&rsquo;s column uses
<strong>UNKNOWN</strong> throughout.
<strong>UD-8(2) (maintenance) and UD-8(3) (child support) cannot be completed until
Julia&rsquo;s income is known.</strong></div>

<div class="note" style="margin-top:0.1in;">
<strong>Income basis:</strong> Dan&rsquo;s current income is SSDI only: $2,306.17/month &times; 12
= <strong>$27,674.04/year</strong>. The 2024 federal return was a <em>transition year</em> that
also included TBK wages of $2,788.88 &mdash; Dan is no longer employed there. SSDI (Title II)
is reported as Social Security benefits on the federal return, so it belongs on <strong>Line 3e</strong>
below; Line&nbsp;1 (wages/salary) = $0. FICA is not withheld from SSDI benefit payments, so
Lines 15 and 16 = $0.</div>

<p class="sec">Appendix A &mdash; Itemization of Income and Deductions</p>
<table class="fin">
<tr><th class="d">Income / Deduction Item</th><th class="p">PLAINTIFF</th>
    <th class="q">DEFENDANT</th></tr>
<tr><td class="d"><strong>I. INCOME</strong></td><td class="p"></td><td class="q"></td></tr>
<tr><td class="d">1. Gross (total) income (wages/salary &mdash; per most recent federal tax return)<br>
    <em style="font-size:10pt;">[TBK wages $2,788.88 on 2024 return; no current employment]</em></td>
    <td class="p">{fi('$0')}<br><em style="font-size:9.5pt;">($2,788.88 TBK wages on 2024 return; no longer employed)</em></td>
    <td class="q">UNKNOWN</td></tr>
<tr><td class="d">2. Investment income</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">3a. Deferred compensation</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">3b. Worker&rsquo;s compensation</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">3c. Disability benefits (non-Social Security)</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">3d. Unemployment insurance benefits</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">3e. Social security benefits<br>
    <em style="font-size:10pt;">[SSDI Title II: $2,306.17/mo &times; 12]</em></td>
    <td class="p">{fi('$27,674.04')}</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">3f. Veterans benefits</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">3g. Pensions and retirement benefits</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">3h. Fellowships and stipends</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">3i. Annuity payments</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">4. Former income/resources voluntarily reduced</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">5. Self-employment deductions</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">6. Other income</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">7. Income from income-producing property</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr style="font-weight:bold;"><td class="d">8. GROSS ANNUAL INCOME (Add lines 1&ndash;7)</td>
    <td class="p">{fi('$27,674.04')}</td><td class="q">UNKNOWN</td></tr>

<tr><td class="d"><strong>II. DEDUCTIONS</strong></td><td class="p"></td><td class="q"></td></tr>
<tr><td class="d">9. Unreimbursed employee business expenses<br>
    <em style="font-size:10pt;">[No current employment; no unreimbursed work expenses]</em></td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">10. Alimony/maintenance paid to a non-party spouse</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">11. Child support paid for a non-party child</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">12. Public assistance</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">13. Supplemental Security Income (SSI)<br>
    <em style="font-size:10pt;">[Dan receives SSDI Title II, not SSI Title XVI]</em></td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">14. New York City or Yonkers income taxes</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">15. FICA Social Security taxes<br>
    <em style="font-size:10pt;">[SSDI is a benefit payment, not wages; FICA not withheld]</em></td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr><td class="d">16. FICA Medicare taxes<br>
    <em style="font-size:10pt;">[Same as line 15 &mdash; not withheld from SSDI]</em></td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>
<tr style="font-weight:bold;"><td class="d">17. TOTAL ANNUAL DEDUCTIONS (Add lines 9&ndash;16)</td>
    <td class="p">$0</td><td class="q">UNKNOWN</td></tr>

<tr><td class="d"><strong>III. NET INCOME</strong></td><td class="p"></td><td class="q"></td></tr>
<tr style="font-weight:bold;"><td class="d">18. NET ANNUAL INCOME (Line 8 minus Line 17)</td>
    <td class="p">{fi('$27,674.04')}</td><td class="q">UNKNOWN</td></tr>
</table>

<div class="note">
<strong>Income basis confirmed:</strong> Current SSDI = $2,306.17/mo &times; 12 = $27,674.04/yr (Line 3e).
No current wages or employment (Line 1 = $0). No FICA deductions (Lines 15&ndash;16 = $0) &mdash;
SSDI benefit payments are not subject to FICA. Net annual income = $27,674.04.<br><br>
<strong>Note on 2024 return:</strong> The 2024 federal return reflects a transition year: TBK wages
($2,788.88) plus partial-year SSDI. Dan is no longer employed at TBK. The income figures above
reflect current income, which is what courts use for child support purposes.<br><br>
<strong>UD-8(2) and UD-8(3) remain blocked.</strong> Both require Line 18 from this form
AND Julia&rsquo;s completed parallel column (currently UNKNOWN).
</div>

{notary()}
</div>"""

# ─── ASSEMBLE HTML ────────────────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8">
<title>NYS Divorce Forms — Irving v. Diaz Irving — Draft v4</title>
<style>{CSS}</style>
</head><body>
{COVER}
{UD1A}
{UD2}
{UD6}
{UD81}
</body></html>"""

# ─── GENERATE PDF ─────────────────────────────────────────────────────────────
print("Generating PDF...")
doc = weasyprint.HTML(string=HTML).write_pdf()
with open(OUT, 'wb') as f:
    f.write(doc)
print(f"Done: {OUT}")
print(f"Size: {len(doc):,} bytes")
