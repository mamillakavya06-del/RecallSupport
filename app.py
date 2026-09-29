import os
import re
import requests
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# ============================================================
# CONFIGURATION
# ============================================================

load_dotenv()

HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

BASE_URL = os.getenv(
    "HINDSIGHT_BASE_URL",
    "https://api.hindsight.vectorize.io"
)

BANK_ID = os.getenv(
    "HINDSIGHT_BANK_ID",
    "resolveai_customer_demo"
)

MODEL = os.getenv(
    "GROQ_MODEL",
    "openai/gpt-oss-120b"
)

HINDSIGHT_HEADERS = {
    "Authorization": f"Bearer {HINDSIGHT_API_KEY}",
    "Content-Type": "application/json",
}

# ============================================================
# PAGE
# ============================================================

st.set_page_config(
    page_title="ResolveAI",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# DARK BLUE UI
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       MAIN BACKGROUND
       ====================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 15% 5%,
                rgba(30, 100, 255, 0.16),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(0, 183, 255, 0.12),
                transparent 25%
            ),
            #061426;
        color: #ffffff;
    }

    .main .block-container {
        max-width: 1280px;
        padding-top: 35px;
        padding-bottom: 50px;
    }

    header {
        background: transparent !important;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* ======================================================
       HERO
       ====================================================== */

    .hero-box {
        position: relative;
        overflow: hidden;
        padding: 55px 55px 50px 55px;
        border-radius: 28px;
        background:
            linear-gradient(
                135deg,
                #071a33 0%,
                #0a2850 50%,
                #063d63 100%
            );
        border: 1px solid #164b78;
        box-shadow:
            0 20px 55px rgba(0, 0, 0, 0.45),
            inset 0 1px 0 rgba(255,255,255,0.05);
        margin-bottom: 28px;
    }

    .hero-glow-one {
        position: absolute;
        width: 330px;
        height: 330px;
        right: -100px;
        top: -160px;
        border-radius: 50%;
        background: rgba(0, 153, 255, 0.20);
        filter: blur(4px);
    }

    .hero-glow-two {
        position: absolute;
        width: 220px;
        height: 220px;
        left: 48%;
        bottom: -170px;
        border-radius: 50%;
        background: rgba(0, 220, 255, 0.12);
    }

    .hero-content {
        position: relative;
        z-index: 5;
    }

    .brand-line {
        color: #62c8ff;
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 2.5px;
        text-transform: uppercase;
        margin-bottom: 16px;
    }

    .hero-title {
        color: #ffffff !important;
        font-size: 58px;
        line-height: 1;
        font-weight: 900;
        letter-spacing: -2px;
        margin: 0;
    }

    .hero-subtitle {
        color: #8fdcff !important;
        font-size: 22px;
        font-weight: 700;
        margin-top: 16px;
    }

    .hero-text {
        color: #d7eaff !important;
        font-size: 16px;
        line-height: 1.75;
        max-width: 850px;
        margin-top: 16px;
    }

    /* ======================================================
       STATUS CARDS
       ====================================================== */

    .status-card {
        background: #0a1d35;
        border: 1px solid #173d62;
        border-radius: 18px;
        padding: 20px 22px;
        min-height: 92px;
        box-shadow:
            0 12px 30px rgba(0,0,0,0.25),
            inset 0 1px 0 rgba(255,255,255,0.03);
    }

    .status-title {
        color: #7294b7;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.3px;
        margin-bottom: 9px;
    }

    .status-value {
        color: #ffffff;
        font-size: 16px;
        font-weight: 800;
    }

    .online {
        color: #31e6a0;
        margin-right: 7px;
        text-shadow: 0 0 10px rgba(49,230,160,0.5);
    }

    /* ======================================================
       SECTION TITLES
       ====================================================== */

    .section-title {
        color: #ffffff !important;
        font-size: 26px;
        font-weight: 850;
        margin-top: 38px;
        margin-bottom: 6px;
    }

    .section-subtitle {
        color: #8da9c4 !important;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* ======================================================
       FLOW
       ====================================================== */

    .flow-wrapper {
        background: #081a30;
        border: 1px solid #153c60;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.22);
    }

    .flow {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 9px;
        flex-wrap: wrap;
    }

    .flow-box {
        background: #0c2948;
        border: 1px solid #20577f;
        border-radius: 12px;
        padding: 12px 15px;
        color: #eaf7ff;
        font-size: 13px;
        font-weight: 750;
    }

    .flow-arrow {
        color: #35bfff;
        font-size: 21px;
        font-weight: 900;
    }

    /* ======================================================
       INPUT PANEL
       ====================================================== */

    .input-panel {
        background:
            linear-gradient(
                145deg,
                #091c32,
                #0b213b
            );
        border: 1px solid #194a72;
        border-radius: 23px;
        padding: 27px 28px 13px 28px;
        box-shadow:
            0 15px 40px rgba(0,0,0,0.30),
            inset 0 1px 0 rgba(255,255,255,0.03);
    }

    label {
        color: #eaf5ff !important;
        font-weight: 750 !important;
    }

    .stTextInput input,
    .stTextArea textarea {
        background: #061526 !important;
        color: #ffffff !important;
        border: 1px solid #28577d !important;
        border-radius: 12px !important;
        font-size: 15px !important;
    }

    .stTextInput input:focus,
    .stTextArea textarea:focus {
        border-color: #20b9ff !important;
        box-shadow:
            0 0 0 2px rgba(32,185,255,0.12),
            0 0 20px rgba(32,185,255,0.08) !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #607d99 !important;
    }

    /* ======================================================
       BUTTON
       ====================================================== */

    .stButton > button {
        width: 100%;
        min-height: 56px;
        border: 1px solid #25bfff;
        border-radius: 13px;
        background:
            linear-gradient(
                135deg,
                #087ed1,
                #00a9e8
            );
        color: #ffffff !important;
        font-size: 17px !important;
        font-weight: 850 !important;
        letter-spacing: 0.2px;
        box-shadow:
            0 8px 25px rgba(0, 165, 240, 0.24),
            inset 0 1px 0 rgba(255,255,255,0.20);
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow:
            0 12px 32px rgba(0, 190, 255, 0.34);
        border-color: #62d7ff;
    }

    /* ======================================================
       MEMORY
       ====================================================== */

    .memory-card {
        background: #081a2e;
        border: 1px solid #17476d;
        border-left: 4px solid #1dafff;
        border-radius: 14px;
        padding: 17px 20px;
        margin-bottom: 11px;
        color: #dceeff;
        font-size: 14px;
        line-height: 1.7;
        box-shadow: 0 8px 22px rgba(0,0,0,0.22);
    }

    .memory-label {
        color: #3fc7ff;
        font-size: 11px;
        font-weight: 850;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    /* ======================================================
       RESPONSE
       ====================================================== */

    .response-card {
        background:
            linear-gradient(
                145deg,
                #091d33,
                #0b263f
            );
        border: 1px solid #1b527c;
        border-radius: 23px;
        padding: 27px;
        box-shadow:
            0 15px 40px rgba(0,0,0,0.30);
    }

    .response-heading {
        display: flex;
        align-items: center;
        gap: 13px;
        color: #ffffff;
        font-size: 21px;
        font-weight: 850;
        margin-bottom: 10px;
    }

    .response-icon {
        width: 43px;
        height: 43px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #0a4670;
        border: 1px solid #218fc5;
        color: #62d7ff;
        font-size: 21px;
    }

    /* ======================================================
       SUCCESS
       ====================================================== */

    .success-card {
        background: #082a25;
        border: 1px solid #126b57;
        border-radius: 14px;
        padding: 15px 18px;
        color: #6ff0c7;
        font-size: 14px;
        font-weight: 750;
        margin-top: 18px;
    }

    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        text-align: center;
        margin-top: 55px;
        padding-top: 20px;
        border-top: 1px solid #153750;
        color: #66819b;
        font-size: 12px;
        line-height: 1.7;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
    <div class="hero-box">

        <div class="hero-glow-one"></div>
        <div class="hero-glow-two"></div>

        <div class="hero-content">

            <div class="brand-line">
                AI CUSTOMER SUPPORT SYSTEM
            </div>

            <div class="hero-title">
                ResolveAI
            </div>

            <div class="hero-subtitle">
                Persistent-Memory Customer Complaint Agent
            </div>

            <div class="hero-text">
                An intelligent customer support system that remembers
                previous interactions, retrieves relevant customer
                history, and uses AI reasoning to generate
                context-aware responses.
            </div>

        </div>

    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# STATUS
# ============================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">Memory Layer</div>
            <div class="status-value">
                <span class="online">●</span>
                Hindsight Connected
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">AI Reasoning</div>
            <div class="status-value">
                <span class="online">●</span>
                Groq Connected
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c3:
    st.markdown(
        """
        <div class="status-card">
            <div class="status-title">Context Engine</div>
            <div class="status-value">
                <span class="online">●</span>
                Persistent Memory Enabled
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ============================================================
# WORKFLOW
# ============================================================

st.markdown(
    '<div class="section-title">Intelligent Resolution Pipeline</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">Every complaint becomes part of a smarter, context-aware support experience.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="flow-wrapper">
        <div class="flow">

            <div class="flow-box">
                Customer Complaint
            </div>

            <div class="flow-arrow">→</div>

            <div class="flow-box">
                Hindsight Memory
            </div>

            <div class="flow-arrow">→</div>

            <div class="flow-box">
                Customer History
            </div>

            <div class="flow-arrow">→</div>

            <div class="flow-box">
                Groq Reasoning
            </div>

            <div class="flow-arrow">→</div>

            <div class="flow-box">
                AI Resolution
            </div>

            <div class="flow-arrow">→</div>

            <div class="flow-box">
                Memory Updated
            </div>

        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# COMPLAINT INPUT
# ============================================================

st.markdown(
    '<div class="section-title">Resolve a Complaint</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-subtitle">Provide the customer identity and describe the issue they are experiencing.</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="input-panel">',
    unsafe_allow_html=True,
)

input1, input2 = st.columns([1, 2])

with input1:
    customer_id = st.text_input(
        "Customer ID",
        placeholder="CUST001",
    )

with input2:
    complaint = st.text_area(
        "Customer Complaint",
        placeholder=(
            "Describe the customer's issue..."
        ),
        height=120,
    )

st.markdown("</div>", unsafe_allow_html=True)

st.write("")

resolve_button = st.button(
    "✦  RESOLVE COMPLAINT",
    use_container_width=True,
)

# ============================================================
# PROCESS
# ============================================================

if resolve_button:

    if not customer_id.strip():
        st.error("Please enter a Customer ID.")
        st.stop()

    if not complaint.strip():
        st.error("Please enter the customer's complaint.")
        st.stop()

    customer_id = customer_id.strip().upper()
    complaint = complaint.strip()

    # --------------------------------------------------------
    # HINDSIGHT RECALL
    # --------------------------------------------------------

    recall_url = (
        f"{BASE_URL}/v1/default/banks/"
        f"{BANK_ID}/memories/recall"
    )

    recall_payload = {
        "query": complaint,
        "max_tokens": 1000,
        "tags": [customer_id],
        "tags_match": "any_strict",
    }

    with st.spinner(
        "Retrieving customer history from Hindsight..."
    ):

        try:

            recall_response = requests.post(
                recall_url,
                headers=HINDSIGHT_HEADERS,
                json=recall_payload,
                timeout=30,
            )

            recall_response.raise_for_status()

            recall_data = recall_response.json()

        except Exception as e:

            st.error(
                f"Unable to retrieve Hindsight memory: {str(e)}"
            )

            st.stop()

    results = recall_data.get("results", [])

    raw_memories = []

    for item in results:

        text = item.get("text", "")

        if text:
            raw_memories.append(text)

    # --------------------------------------------------------
    # MEMORY DEDUPLICATION
    # --------------------------------------------------------

    def normalize_memory(text):

        cleaned = text.lower()

        cleaned = re.sub(
            r"\|\s*when.*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\|\s*involving.*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\|\s*the customer.*",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b",
            "",
            cleaned,
        )

        cleaned = re.sub(
            r"\s+",
            " ",
            cleaned,
        )

        return cleaned.strip()

    def word_overlap(text1, text2):

        words1 = set(
            re.findall(
                r"\b\w+\b",
                text1.lower()
            )
        )

        words2 = set(
            re.findall(
                r"\b\w+\b",
                text2.lower()
            )
        )

        if not words1 or not words2:
            return 0

        return len(words1 & words2) / min(
            len(words1),
            len(words2)
        )

    memories = []

    for memory in raw_memories:

        normalized = normalize_memory(memory)

        duplicate = False

        for existing in memories:

            existing_normalized = normalize_memory(
                existing
            )

            if (
                normalized == existing_normalized
                or
                word_overlap(
                    normalized,
                    existing_normalized
                ) >= 0.55
            ):

                duplicate = True
                break

        if not duplicate:
            memories.append(memory)

    # --------------------------------------------------------
    # PREVIOUS MEMORY
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">Previous Customer Memory</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="section-subtitle">Context retrieved for {customer_id}</div>',
        unsafe_allow_html=True,
    )

    if memories:

        for index, memory in enumerate(
            memories,
            start=1
        ):

            st.markdown(
                f"""
                <div class="memory-card">

                    <div class="memory-label">
                        MEMORY {index}
                    </div>

                    {memory}

                </div>
                """,
                unsafe_allow_html=True,
            )

    else:

        st.info(
            "No directly relevant previous memory was found "
            "for this customer."
        )

    # --------------------------------------------------------
    # GROQ CONTEXT
    # --------------------------------------------------------

    if memories:

        memory_text = "\n".join(
            [
                f"- {memory}"
                for memory in memories
            ]
        )

    else:

        memory_text = (
            "No relevant previous customer history was found."
        )

    # --------------------------------------------------------
    # GROQ
    # --------------------------------------------------------

    prompt = f"""
You are ResolveAI, an AI-powered customer complaint resolution assistant.

The current customer is:
{customer_id}

Current complaint:
{complaint}

Relevant previous memories retrieved specifically for this customer:
{memory_text}

Instructions:

1. Use only relevant memories belonging to this customer.
2. Ignore unrelated memories.
3. Do not repeat the same memory unnecessarily.
4. Do not claim that an issue is recurring unless the memory supports it.
5. Do not invent customer history.
6. Do not claim access to payment systems, order systems,
   account systems, internal company systems, or transaction records.
7. Do not claim that you issued refunds, contacted teams,
   checked transactions, or changed account information.
8. Give practical next-step guidance based only on available information.

Return exactly these six sections:

1. Customer Issue
2. Relevant Previous History
3. Irrelevant Previous History
4. Possible Cause
5. Suggested Next Step
6. Information Needed
"""

    with st.spinner(
        "Groq is reasoning over the customer context..."
    ):

        try:

            groq_client = Groq(
                api_key=GROQ_API_KEY
            )

            completion = (
                groq_client
                .chat
                .completions
                .create(
                    model=MODEL,
                    temperature=0.1,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a precise customer "
                                "support reasoning assistant."
                            ),
                        },
                        {
                            "role": "user",
                            "content": prompt,
                        },
                    ],
                )
            )

            response_text = (
                completion
                .choices[0]
                .message
                .content
            )

        except Exception as e:

            st.error(
                f"Groq reasoning failed: {str(e)}"
            )

            st.stop()

    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">ResolveAI Response</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="response-card">

            <div class="response-heading">

                <div class="response-icon">
                    ✦
                </div>

                <div>
                    Context-Aware Resolution
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(response_text)

    # --------------------------------------------------------
    # SAVE MEMORY
    # --------------------------------------------------------

    retain_url = (
        f"{BASE_URL}/v1/default/banks/"
        f"{BANK_ID}/memories"
    )

    retain_payload = {
        "items": [
            {
                "content": (
                    f"Customer {customer_id} complaint: "
                    f"{complaint}"
                ),
                "tags": [customer_id],
            }
        ]
    }

    with st.spinner(
        "Saving this interaction to persistent memory..."
    ):

        try:

            retain_response = requests.post(
                retain_url,
                headers=HINDSIGHT_HEADERS,
                json=retain_payload,
                timeout=30,
            )

            retain_response.raise_for_status()

            st.markdown(
                f"""
                <div class="success-card">
                    ✓ Interaction for {customer_id}
                    has been saved to Hindsight persistent memory.
                </div>
                """,
                unsafe_allow_html=True,
            )

        except Exception as e:

            st.warning(
                f"Response generated, but memory could not be saved: {str(e)}"
            )

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        <strong>ResolveAI</strong>
        <br>
        Persistent-Memory Customer Support Agent
        <br>
        Hindsight Memory • Groq Reasoning • Context-Aware AI
    </div>
    """,
    unsafe_allow_html=True,
)