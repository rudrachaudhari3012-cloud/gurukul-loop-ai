<style>
:root {
    color-scheme: dark;
    --bg: #050816;
    --bg-secondary: #09132B;
    --panel: #0D1933;
    --panel-hover: #122544;
    --emerald: #073D38;
    --cyan: #00D6FF;
    --mint: #00F5B8;
    --text: #F2FAFF;
    --muted: #A8BED8;
    --border: rgba(0, 214, 255, 0.30);
}

/* CYBER AI — MIXED BACKGROUND + ULTRA GLOW */
.stApp {
    background:
        radial-gradient(ellipse at 8% 4%,
            rgba(0, 214, 255, 0.18), transparent 30%),
        radial-gradient(ellipse at 92% 20%,
            rgba(0, 245, 184, 0.13), transparent 30%),
        radial-gradient(ellipse at 50% 100%,
            rgba(55, 78, 255, 0.13), transparent 40%),
        linear-gradient(135deg, #050816 0%, #09132B 48%, #061A25 100%);
    color: var(--text);
}

/* Main layout */
.block-container {
    max-width: 1440px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Background glow */
.stApp::before {
    content: "";
    position: fixed;
    z-index: 0;
    width: 400px;
    height: 400px;
    right: -10%;
    top: 10%;
    border-radius: 50%;
    background: rgba(0, 214, 185, 0.10);
    filter: blur(65px);
    pointer-events: none;
}

/* Text */
.stApp,
.stApp p,
.stApp label,
.stApp li {
    color: var(--text);
}

.stMarkdown,
.stCaption,
[data-testid="stCaptionContainer"] {
    color: var(--muted);
}

h1, h2, h3, h4 {
    color: var(--text);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background:
        radial-gradient(circle at 10% 5%,
            rgba(0, 214, 255, 0.13), transparent 35%),
        linear-gradient(180deg, #080F24 0%, #071D25 100%);
    border-right: 1px solid rgba(0, 245, 184, 0.28);
    box-shadow: 5px 0 28px rgba(0, 214, 255, 0.06);
}

[data-testid="stSidebar"] * {
    color: #F2FAFF;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2 {
    color: var(--mint);
}

[data-testid="stSidebar"] input {
    color: #F2FAFF !important;
    background: #0D1933 !important;
}

/* Select boxes */
[data-baseweb="select"] > div {
    background-color: #0D1933;
    border-color: rgba(0, 214, 255, 0.38);
    border-radius: 10px;
    color: #F2FAFF;
}

[data-baseweb="popover"],
[data-baseweb="menu"] {
    background: #0D1933;
}

[data-baseweb="menu"] * {
    color: #F2FAFF;
}

/* Hero — electric cyan + neon mint */
.hero {
    position: relative;
    overflow: hidden;
    padding: 2.5rem 2.3rem;
    border-radius: 26px;
    color: white;
    background:
        radial-gradient(circle at 90% 10%,
            rgba(0, 214, 255, 0.24), transparent 34%),
        radial-gradient(circle at 8% 100%,
            rgba(0, 245, 184, 0.15), transparent 40%),
        linear-gradient(120deg,
            #080F24 0%, #0A3040 52%, #073D38 100%);
    border: 1px solid rgba(0, 214, 255, 0.55);
    box-shadow:
        0 0 20px rgba(0, 214, 255, 0.18),
        0 0 45px rgba(0, 214, 255, 0.10),
        0 18px 48px rgba(0, 0, 0, 0.35),
        inset 0 0 28px rgba(0, 245, 184, 0.05);
}

.hero:after {
    content: '✦';
    position: absolute;
    right: 5%;
    top: -55px;
    font-size: 190px;
    color: rgba(0, 214, 255, 0.13);
    text-shadow: 0 0 35px rgba(0, 214, 255, 0.35);
    pointer-events: none;
}

.eyebrow {
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-size: 0.75rem;
    font-weight: 800;
    color: var(--mint);
    text-shadow: 0 0 12px rgba(0, 245, 184, 0.30);
}

.hero h1 {
    color: #FFFFFF !important;
    font-size: clamp(2rem, 4vw, 3.35rem);
    line-height: 1.08;
    margin: 0.55rem 0 0.75rem 0;
    text-shadow:
        0 0 14px rgba(0, 214, 255, 0.32),
        0 0 32px rgba(0, 214, 255, 0.14);
}

.hero p {
    color: #D9F7FF;
    font-size: 1.05rem;
    max-width: 740px;
    margin-bottom: 0;
    line-height: 1.7;
}

.pill-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 1.35rem;
}

.pill {
    border: 1px solid rgba(0, 214, 255, 0.42);
    background: rgba(5, 8, 22, 0.60);
    border-radius: 999px;
    padding: 0.48rem 0.8rem;
    font-size: 0.82rem;
    color: #E8FFFF;
    backdrop-filter: blur(8px);
    box-shadow: 0 0 12px rgba(0, 214, 255, 0.07);
}

/* Section headings */
.section-kicker {
    color: var(--mint);
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

.section-title {
    color: #F2FAFF;
    font-size: 1.55rem;
    font-weight: 800;
    margin-top: 0;
    margin-bottom: 0.45rem;
    text-shadow: 0 0 16px rgba(0, 214, 255, 0.08);
}

.subtle {
    color: #A8BED8;
}

/* Glass cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background:
        linear-gradient(145deg,
            rgba(13, 25, 51, 0.97),
            rgba(7, 20, 39, 0.97));
    border: 1px solid rgba(0, 214, 255, 0.23);
    border-radius: 18px;
    box-shadow:
        0 8px 24px rgba(0, 0, 0, 0.20),
        0 0 12px rgba(0, 214, 255, 0.035);
    transition:
        border-color 0.25s ease,
        box-shadow 0.25s ease,
        transform 0.25s ease;
}

[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: rgba(0, 245, 184, 0.65);
    box-shadow:
        0 0 18px rgba(0, 214, 255, 0.15),
        0 0 30px rgba(0, 245, 184, 0.08),
        0 12px 30px rgba(0, 0, 0, 0.24);
    transform: translateY(-1px);
}

/* Metrics */
div[data-testid="stMetric"] {
    background:
        linear-gradient(145deg,
            rgba(0, 214, 255, 0.12),
            rgba(9, 19, 43, 0.97) 60%,
            rgba(0, 245, 184, 0.06));
    border: 1px solid rgba(0, 214, 255, 0.35);
    padding: 1rem 1.1rem;
    border-radius: 17px;
    box-shadow:
        0 0 17px rgba(0, 214, 255, 0.09),
        inset 0 0 18px rgba(0, 214, 255, 0.025);
}

div[data-testid="stMetricLabel"] {
    color: #A8BED8;
}

div[data-testid="stMetricValue"] {
    color: var(--mint);
    text-shadow: 0 0 14px rgba(0, 245, 184, 0.20);
}

div[data-testid="stMetricDelta"] {
    color: var(--cyan);
}

/* Inputs */
.stTextInput input,
.stNumberInput input {
    background: #080F24 !important;
    color: #F2FAFF !important;
    border: 1px solid rgba(0, 214, 255, 0.34) !important;
    border-radius: 10px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {
    border-color: var(--cyan) !important;
    box-shadow:
        0 0 0 1px rgba(0, 214, 255, 0.35),
        0 0 15px rgba(0, 214, 255, 0.12) !important;
}

/* Sliders */
.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: var(--mint);
    border-color: var(--mint);
    box-shadow: 0 0 12px rgba(0, 245, 184, 0.35);
}

.stSlider [data-testid="stTickBar"] {
    background: rgba(0, 214, 255, 0.40);
}

/* Buttons */
div.stButton > button {
    border: 1px solid rgba(0, 214, 255, 0.38);
    border-radius: 12px;
    background: linear-gradient(110deg, #0D1933, #10283B);
    color: #F2FAFF;
    font-weight: 700;
    transition: all 0.25s ease;
}

div.stButton > button[kind="primary"] {
    border: 1px solid rgba(0, 214, 255, 0.85);
    border-radius: 13px;
    background: linear-gradient(100deg, #00D6FF 0%, #00F5B8 100%);
    color: #04101D;
    font-weight: 850;
    min-height: 3rem;
    box-shadow:
        0 0 16px rgba(0, 214, 255, 0.34),
        0 0 30px rgba(0, 245, 184, 0.16);
}

div.stButton > button[kind="primary"]:hover {
    border-color: #FFFFFF;
    color: #04101D;
    filter: brightness(1.08);
    box-shadow:
        0 0 22px rgba(0, 214, 255, 0.50),
        0 0 40px rgba(0, 245, 184, 0.24);
    transform: translateY(-2px);
}

div.stButton > button:not([kind="primary"]):hover {
    border-color: var(--mint);
    color: var(--mint);
    background: #10283B;
    box-shadow: 0 0 14px rgba(0, 245, 184, 0.10);
}

/* Download button */
[data-testid="stDownloadButton"] button {
    background: linear-gradient(100deg, #073D38, #0A3040);
    border: 1px solid rgba(0, 245, 184, 0.60);
    color: #EFFFF8;
    border-radius: 12px;
    font-weight: 750;
    transition: all 0.25s ease;
}

[data-testid="stDownloadButton"] button:hover {
    border-color: var(--mint);
    box-shadow: 0 0 20px rgba(0, 245, 184, 0.20);
}

/* Radio buttons */
[data-testid="stRadio"] label {
    color: #F2FAFF;
}

[data-testid="stRadio"] label:hover {
    color: var(--mint);
}

/* Expanders */
[data-testid="stExpander"] {
    background: rgba(9, 19, 43, 0.90);
    border: 1px solid rgba(0, 214, 255, 0.30);
    border-radius: 14px;
    box-shadow: 0 0 14px rgba(0, 214, 255, 0.04);
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid rgba(0, 214, 255, 0.30);
    background: rgba(9, 25, 43, 0.95);
}

[data-testid="stAlert"] p {
    color: #F2FAFF;
}

/* Dividers */
hr {
    border-color: rgba(0, 214, 255, 0.23);
}

/* Captions */
[data-testid="stCaptionContainer"] {
    color: #A8BED8;
}

/* Footer */
.footer {
    color: #8EAAC5;
    font-size: 0.82rem;
    text-align: center;
    padding: 1.5rem 0 0.5rem;
    border-top: 1px solid rgba(0, 214, 255, 0.22);
    margin-top: 1.8rem;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #050816;
}

::-webkit-scrollbar-thumb {
    background: #07556A;
    border-radius: 8px;
}

::-webkit-scrollbar-thumb:hover {
    background: #00F5B8;
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        transition: none !important;
        animation: none !important;
    }
}
</style>
