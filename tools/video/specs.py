import json
import os
D = os.path.dirname(os.path.abspath(__file__)); L = D + '/logo/'; B = D + '/bg/'

def V(**k):
    base = dict(bg0='#0b0f1a', acc='#fff', acc2='#fff', txt='#ffffff', sub='#cfd6e4', kickfg='#fff', neg='#ff5a4f',
                card='rgba(255,255,255,.10)', barc='rgba(255,255,255,.35)', rad='12px', lmrad='50%', hcase='none',
                logobg='#ffffff', foot='rgba(255,255,255,.55)', gridop='0', photofilter='none',
                shade='linear-gradient(180deg,rgba(0,0,0,.45) 0%,rgba(0,0,0,.55) 35%,rgba(0,0,0,.88) 60%,rgba(0,0,0,.95) 100%)')
    base.update(k); return base

SPECS = {}

# 1. AI News Report — breaking-news alert, red/navy, uppercase, grid
SPECS['ainewsreport'] = dict(
  slug='artex-ai-agents-connectwise-attack',
  title='AI agents hacked 2,250 company cloud accounts',
  theme=dict(name='AI NEWS REPORT', tag='AI SECURITY ALERT', logo=L+'anr_dark.png', bg=B+'anr_c.jpg', font='inter', hfs=90,
    vars=V(bg0='#0a1424', acc='#e0312b', acc2='#ff5a4f', kickfg='#fff', hcase='uppercase', rad='6px', lmrad='8px', gridop='1',
           photofilter='grayscale(.6) brightness(.8)', card='rgba(31,58,95,.55)',
           shade='linear-gradient(180deg,rgba(10,20,36,.55),rgba(10,20,36,.75) 40%,rgba(10,20,36,.96) 62%)')),
  source='Source: Microsoft Threat Intelligence, TechCrunch (21–22 Oct 2026)',
  scenes=[
    dict(type='hook', dur=4.2, top=640, kicker='Breaking · AI security', head='AI agents just broke into', fs=96,
         count=dict(to=2250, label='company cloud accounts', at=0.5, dur=1.8)),
    dict(type='text', dur=4.6, top=700, kicker='Who did it', head='A China-aligned group Microsoft calls <span class=a>Storm-0940</span>', fs=84,
         lines=['Using ARTEX, an open-source AI hacking tool built for security testing.'], lat=1.6),
    dict(type='stats', dur=5.6, top=560, kicker='How fast it moved', step=1.0, items=[
         dict(v='151,000+', l='failed sign-ins in 4 days', count=dict(to=151000, suf='+')),
         dict(v='2,900', l='attempts per minute at the peak', count=dict(to=2900)),
         dict(v='&lt; 3 hrs', l='to admin-level access in some accounts')]),
    dict(type='text', dur=4.4, top=720, kicker='The way in', head='No Microsoft bug. <span class=a>Stolen vendor keys.</span>', fs=86,
         lines=['Credentials taken from ConnectWise\'s cloud backup let the agents sign straight in.'], lat=1.5),
    dict(type='list', dur=5.6, top=600, kicker='IT teams: check now', head='', mark='num', step=0.9, items=[
         'Keep ConnectWise app links disabled', 'Search your tenants by app ID', 'Review sign-in logs from 1 Oct', 'Rotate secrets, cut extra permissions']),
    dict(type='cta', dur=4.6, top=560, q='Who is to blame when an <span class=a>AI agent</span> hacks?', fs=78,
         url='ainewsreport.org', follow='Follow for AI news that matters'),
  ])

# 2. AI News Round — "3 things to know", purple neon, Poppins
SPECS['ainewsround'] = dict(
  slug='uber-chatgpt-work-30000-staff',
  title='Uber gives ChatGPT Work to all 30,000 staff',
  theme=dict(name='AI NEWS ROUND', tag='AI &amp; BUSINESS', logo=L+'anro.webp', bg=B+'anro_c.jpg', font='poppins', hfs=96,
    vars=V(bg0='#120a2a', acc='#6b4bd8', acc2='#b9a6ff', kickfg='#fff', rad='999px', lmrad='50%', card='rgba(107,75,216,.22)',
           shade='linear-gradient(180deg,rgba(18,10,42,.35),rgba(18,10,42,.7) 40%,rgba(18,10,42,.96) 62%)')),
  source='Source: TechCrunch, 22 Oct 2026',
  scenes=[
    dict(type='hook', dur=4.0, top=640, kicker='Uber × OpenAI', head='Uber just gave an AI agent to', fs=96,
         count=dict(to=30000, label='employees. Every single one.', at=0.5, dur=1.6)),
    dict(type='text', dur=3.0, top=820, head='<span class=a>3 things</span> you need to know', fs=120),
    dict(type='hook', dur=4.6, top=640, kicker='1 · The test', head='It started with a', fs=88,
         count=dict(to=1000, label='person pilot in finance, operations and product', at=0.4, dur=1.2)),
    dict(type='hook', dur=4.6, top=640, kicker='2 · The surprise', head='Most users were <span class=a>not engineers</span>', fs=88,
         count=dict(to=80, suf='%', label='of early adopters worked outside engineering', at=0.6, dur=1.2)),
    dict(type='text', dur=5.0, top=640, kicker='3 · The trick', head='"AI pods"', fs=120,
         lines=['30 AI engineers paired with teams across Uber.', '2 weeks to automate key parts of each job.'], lat=0.9, lstep=1.4),
    dict(type='cta', dur=4.8, top=560, q='Would you want an AI agent doing <span class=a>your</span> job tasks?', fs=78,
         sub='Yes or no? Comment &#8595;', url='ainewsround.com', follow='Follow for daily AI news'),
  ])

# 3. Opportunities to Apply — bright opportunity alert + checklist, white cards
SPECS['opportunities-to-apply'] = dict(
  slug='croatia-scholarships-without-ielts-2027',
  title='Study in Croatia without IELTS (2027 scholarships)',
  theme=dict(name='OPPORTUNITIES TO APPLY', tag='SCHOLARSHIP ALERT', logo=L+'ota.webp', bg=B+'ota_c.jpg', font='poppins', hfs=96,
    vars=V(bg0='#1b1206', acc='#f07c1a', acc2='#ffb35c', kickfg='#fff', rad='22px', lmrad='50%', card='rgba(255,255,255,.12)',
           shade='linear-gradient(180deg,rgba(27,18,6,.25),rgba(27,18,6,.55) 38%,rgba(27,18,6,.95) 60%)')),
  source='Full guide and links: opportunitiestoapply.com',
  scenes=[
    dict(type='hook', dur=4.2, top=700, kicker='2027 intake · Europe', head='No IELTS? You can still study in <span class=a>Croatia</span>', fs=104,
         lines=['Fully and partly funded scholarships are open.'], lat=1.4),
    dict(type='text', dur=4.6, top=680, kicker='Use this instead', head='An <span class=a>English Medium of Instruction</span> letter', fs=88,
         lines=['Ask your school or university registrar to confirm you studied in English.'], lat=1.5),
    dict(type='stats', dur=6.0, top=520, kicker='Scholarships to target', step=1.1, items=[
         dict(v='Government', l='Tuition waiver + monthly allowance + housing'),
         dict(v='Erasmus Mundus', l='Tuition, travel, and about €1,000–€1,400 a month'),
         dict(v='CEEPUS', l='Plus merit grants at Zagreb and Rijeka')]),
    dict(type='list', dur=5.6, top=520, kicker='Documents checklist', mark='check', step=0.6, items=[
         'Passport copy', 'Transcripts and certificates', 'MOI letter (replaces IELTS)', 'Motivation letter', 'Two recommendation letters', 'Updated CV']),
    dict(type='versus', dur=4.2, top=640, kicker='Cost of living', left=dict(t='From', v='€400', d='per month'), right=dict(t='Up to', v='€700', d='per month'),
         note='English is widely used in the big cities.'),
    dict(type='cta', dur=4.8, top=560, q='Tag a friend who said IELTS was <span class=a>stopping them</span>', fs=76,
         sub='Save this for your 2027 application', url='opportunitiestoapply.com', follow='Follow for new scholarships daily'),
  ])

# 4. Afrotech Horizon — leaderboard / ranking bars, green
SPECS['afrotech'] = dict(
  slug='nigeria-startup-funding-635m-top-spot',
  title='Nigeria is back on top of African startup funding',
  theme=dict(name='AFROTECH HORIZON', tag='STARTUPS &amp; FUNDING', logo=L+'afro.webp', bg=B+'afro_c.jpg', font='montserrat', hfs=94,
    vars=V(bg0='#06150d', acc='#1fa363', acc2='#5be39b', kickfg='#fff', rad='14px', lmrad='14px', card='rgba(31,163,99,.16)',
           barc='rgba(255,255,255,.28)', shade='linear-gradient(180deg,rgba(6,21,13,.4),rgba(6,21,13,.7) 38%,rgba(6,21,13,.96) 60%)')),
  source='Data: Africa: The Big Deal via Nairametrics · Jan–Sep 2026',
  scenes=[
    dict(type='hook', dur=4.2, top=640, kicker='Jan–Sep 2026', head='Nigeria just took back Africa\'s <span class=a>No. 1</span> spot', fs=92,
         count=dict(to=635, pre='$', suf='M', label='raised by Nigerian startups', at=0.6, dur=1.5)),
    dict(type='bars', dur=5.6, top=520, kicker='The leaderboard', head='Startup funding, first 9 months', fs=66, items=[
         dict(l='Nigeria', v=635, d='$635M', hl=True), dict(l='Egypt', v=445, d='$445M'), dict(l='Kenya', v=201, d='$201M'), dict(l='S. Africa', v=182, d='$182M')]),
    dict(type='versus', dur=4.6, top=640, kicker='Year on year', left=dict(t='2025', v='$247M', d='Jan–Sep'), right=dict(t='2026', v='$635M', d='Jan–Sep'),
         note='About 2.6 times more, and already above all of 2025.'),
    dict(type='bars', dur=6.0, top=520, kicker='But here\'s the catch', head='4 deals = <span class=a>69%</span> of the money', fs=78, items=[
         dict(l='Moove', v=250, d='$250M', hl=True), dict(l='Flutterwave', v=100, d='$100M', hl=True), dict(l='Jumia', v=50, d='$50M', hl=True), dict(l='Yellow Card', v=40, d='$40M', hl=True)]),
    dict(type='text', dur=4.2, top=700, kicker='The number to watch', head='<span class=a>77</span> startups raised $100K+', fs=96,
         lines=['Up 10%, while Egypt, Kenya and South Africa fell.'], lat=1.3),
    dict(type='cta', dur=4.8, top=560, q='Real comeback, or <span class=a>4 deals in a trench coat?</span>', fs=78,
         url='afrotechhorizon.com', follow='Follow for African tech, daily'),
  ])

# 5. Cameroon Business Review — "what it means for you" explainer, editorial green
SPECS['cameroonbusinessreview'] = dict(
  slug='cameroon-imf-talks-cfa300bn-2027',
  title='Cameroon\'s CFA300 billion IMF question',
  theme=dict(name='CAMEROON BUSINESS REVIEW', tag='ECONOMY &amp; MACRO', logo=L+'cbr.webp', bg=B+'cbr_c.jpg', font='inter', hfs=90,
    vars=V(bg0='#06130b', acc='#0f7a3d', acc2='#f5c518', kickfg='#fff', rad='4px', lmrad='4px', card='rgba(255,255,255,.09)', neg='#ff6a5a',
           shade='linear-gradient(180deg,rgba(6,19,11,.35),rgba(6,19,11,.7) 38%,rgba(6,19,11,.96) 60%)')),
  source='Sources: Business in Cameroon, Investir au Cameroun (21 Oct 2026)',
  scenes=[
    dict(type='hook', dur=4.4, top=620, kicker='Cameroon · 2027 budget', head='A hole could open in next year\'s budget', fs=92,
         count=dict(to=300, pre='CFA', suf='bn', fs=170, label='of budget support is at risk', at=0.6, dur=1.5)),
    dict(type='text', dur=5.0, top=660, kicker='Why', head='That money usually needs an <span class=a>IMF programme</span>', fs=86,
         lines=['Cameroon has not formally asked for one yet.', 'The last one ended in July 2025.'], lat=1.4, lstep=1.3),
    dict(type='stats', dur=5.6, top=520, kicker='Where things stand', step=0.9, items=[
         dict(v='44.7%', l='public debt to GDP (March 2026)'),
         dict(v='High', l='IMF rating for risk of debt distress'),
         dict(v='10.65%', l='record Eurobond yield after Fitch cut to B-')]),
    dict(type='list', dur=5.4, top=560, kicker='If talks don\'t start', mark='num', step=1.0, items=[
         'A CFA300bn financing gap', 'World Bank and AfDB money arrives later', 'Suppliers to the state get paid slower']),
    dict(type='text', dur=4.4, top=700, kicker='What it means for you', head='Selling to the state? <span class=a>Plan your 2027 cash flow now.</span>', fs=82),
    dict(type='cta', dur=4.8, top=560, q='Should Cameroon go back to the <span class=a>IMF</span>?', fs=82,
         url='cameroonbusinessreview.com', follow='Follow for Cameroon business news'),
  ])

# 6. Market Pulse Africa — deadline + key numbers, gold
SPECS['marketpulseafrica'] = dict(
  slug='dangote-refinery-ipo-final-days',
  title='Dangote refinery IPO: final days',
  theme=dict(name='MARKET PULSE AFRICA', tag='AFRICAN EQUITIES', logo=L+'mpa.webp', bg=B+'mpa_c.jpg', font='montserrat', hfs=94,
    vars=V(bg0='#091930', acc='#c99a13', acc2='#f2b01e', kickfg='#091930', rad='10px', lmrad='10px', card='rgba(42,74,120,.45)',
           shade='linear-gradient(180deg,rgba(9,25,48,.4),rgba(9,25,48,.7) 38%,rgba(9,25,48,.96) 60%)')),
  source='Source: Nairametrics, NGX, SEC Nigeria · Not investment advice',
  scenes=[
    dict(type='hook', dur=4.2, top=640, kicker='Dangote refinery IPO', head='The window closes <span class=a>27 October</span>', fs=96,
         count=dict(to=525, pre='N', label='per share. Minimum 10 shares (N5,250).', at=0.6, dur=1.3)),
    dict(type='stats', dur=5.8, top=520, kicker='The key numbers', step=1.0, items=[
         dict(v='$1.6bn', l='offer size (about N2.15 trillion)'),
         dict(v='4.1bn', l='shares on offer'),
         dict(v='700,000', l='barrels per day refinery capacity', count=dict(to=700000))]),
    dict(type='versus', dur=4.6, top=640, kicker='NGX\'s big claim', left=dict(t='Active investors', v='Today', d='a few hundred thousand'),
         right=dict(t='After IPO', v='3–5×', d='NGX estimate'), note='Apply via banks, fintech apps, WhatsApp or USSD.'),
    dict(type='list', dur=5.8, top=560, kicker='Before you apply', mark='num', step=0.9, items=[
         'Read the prospectus', 'You may get fewer shares than you ask for', 'Prices can swing after listing', 'Only invest money you can leave alone']),
    dict(type='cta', dur=4.8, top=560, q='Are you buying before <span class=a>27 October?</span>', fs=84,
         sub='Tell us how you applied &#8595;', url='marketpulseafrica.com', follow='Not investment advice · Follow for market updates'),
  ])

if __name__ == '__main__':
    import os
    os.makedirs(D + '/specs', exist_ok=True)
    for k, v in SPECS.items():
        json.dump(v, open(f'{D}/specs/{k}.json', 'w'), indent=1)
    print(list(SPECS))
