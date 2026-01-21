import requests
import streamlit as st

# UCANBLEHUB ESSENTIAL NEVER DELETE OR CHANGE
from config import BACKEND_BASE_URL
from utils import send_message

# -------------------------
# STREAMLIT PAGE SETTINGS
# -------------------------
st.set_page_config(
    page_title="AegisVerify - Information Verification System",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------
# CUSTOM CSS (Professional Security UI)
# -------------------------
st.markdown("""
<style>
/* Main container */
.main {
    background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
}

/* Header section */
.header-container {
    background: linear-gradient(135deg, #1E40AF 0%, #3B82F6 100%);
    padding: 40px 30px;
    border-radius: 16px;
    margin-bottom: 30px;
    box-shadow: 0 10px 40px rgba(59, 130, 246, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.header-title {
    font-size: 42px;
    font-weight: 800;
    color: #FFFFFF;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
    margin-bottom: 10px;
}

.header-subtitle {
    font-size: 18px;
    color: #E0E7FF;
    font-weight: 400;
    line-height: 1.6;
}

.shield-icon {
    font-size: 48px;
    display: inline-block;
    margin-right: 15px;
    filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
}

/* Info cards */
.info-cards {
    display: flex;
    gap: 20px;
    margin-bottom: 30px;
}

.info-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    flex: 1;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}

.info-card-title {
    font-size: 14px;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
    font-weight: 600;
}

.info-card-value {
    font-size: 24px;
    color: #FFFFFF;
    font-weight: 700;
}

/* Chat container */
.chat-container {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    margin-bottom: 25px;
    min-height: 400px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

/* Chat bubbles */
.user-msg {
    background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
    padding: 16px 22px;
    border-radius: 16px 16px 4px 16px;
    max-width: 75%;
    margin-bottom: 16px;
    margin-left: auto;
    font-size: 15px;
    color: #FFFFFF;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.bot-msg {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(10px);
    padding: 20px 24px;
    border-radius: 16px 16px 16px 4px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    max-width: 85%;
    margin-bottom: 16px;
    font-size: 15px;
    color: #F1F5F9;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    line-height: 1.7;
}

/* Markdown styling in bot messages */
.bot-msg h3 {
    color: #60A5FA;
    font-size: 18px;
    margin-top: 20px;
    margin-bottom: 12px;
    border-bottom: 2px solid rgba(96, 165, 250, 0.3);
    padding-bottom: 8px;
}

.bot-msg h3:first-child {
    margin-top: 0;
}

.bot-msg ul, .bot-msg ol {
    margin: 10px 0;
    padding-left: 25px;
}

.bot-msg li {
    margin: 6px 0;
}

.bot-msg strong {
    color: #93C5FD;
    font-weight: 600;
}

.bot-msg code {
    background: rgba(0, 0, 0, 0.3);
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-size: 14px;
}

/* Risk indicators */
.risk-high {
    color: #EF4444;
    font-weight: 700;
}

.risk-medium {
    color: #F59E0B;
    font-weight: 600;
}

.risk-low {
    color: #10B981;
    font-weight: 600;
}

/* Score badges */
.score-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-weight: 600;
    font-size: 14px;
    margin-left: 8px;
}

.score-high {
    background: rgba(16, 185, 129, 0.2);
    color: #10B981;
    border: 1px solid rgba(16, 185, 129, 0.4);
}

.score-medium {
    background: rgba(245, 158, 11, 0.2);
    color: #F59E0B;
    border: 1px solid rgba(245, 158, 11, 0.4);
}

.score-low {
    background: rgba(239, 68, 68, 0.2);
    color: #EF4444;
    border: 1px solid rgba(239, 68, 68, 0.4);
}

/* Features section */
.features-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.feature-box {
    background: rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(10px);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    transition: all 0.3s ease;
}

.feature-box:hover {
    background: rgba(255, 255, 255, 0.06);
    border-color: rgba(59, 130, 246, 0.5);
    transform: translateY(-2px);
}

.feature-icon {
    font-size: 32px;
    margin-bottom: 12px;
}

.feature-title {
    font-size: 16px;
    color: #FFFFFF;
    font-weight: 600;
    margin-bottom: 8px;
}

.feature-desc {
    font-size: 13px;
    color: #94A3B8;
    line-height: 1.5;
}

/* Input area styling */
.stChatInputContainer {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 8px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
}

::-webkit-scrollbar-thumb {
    background: rgba(59, 130, 246, 0.5);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(59, 130, 246, 0.7);
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# INIT SESSION STATES
# -------------------------
if "session" not in st.session_state:
    st.session_state.session = requests.Session()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "analysis_count" not in st.session_state:
    st.session_state.analysis_count = 0

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<div class='header-container'>
    <span class='shield-icon'>🛡️</span>
    <div style='display: inline-block; vertical-align: middle;'>
        <div class='header-title'>AegisVerify</div>
        <div class='header-subtitle'>Global Information Verification & Risk Analysis System</div>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------
# INFO CARDS
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class='info-card'>
        <div class='info-card-title'>⚡ Analysis Speed</div>
        <div class='info-card-value'>Real-time</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='info-card'>
        <div class='info-card-title'>🎯 Accuracy</div>
        <div class='info-card-value'>Enterprise-Grade</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='info-card'>
        <div class='info-card-title'>📊 Analyses Performed</div>
        <div class='info-card-value'>{st.session_state.analysis_count}</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# FEATURES SECTION
# -------------------------
if len(st.session_state.messages) == 0:
    st.markdown("### 🔍 Core Capabilities")
    
    features_html = """
    <div class='features-grid'>
        <div class='feature-box'>
            <div class='feature-icon'>✓</div>
            <div class='feature-title'>Truthfulness Scoring</div>
            <div class='feature-desc'>Evidence-based verification with 0-100 accuracy ratings</div>
        </div>
        <div class='feature-box'>
            <div class='feature-icon'>🔬</div>
            <div class='feature-title'>Source Cross-Check</div>
            <div class='feature-desc'>Global fact verification against trusted institutions</div>
        </div>
        <div class='feature-box'>
            <div class='feature-icon'>⚠️</div>
            <div class='feature-title'>Fraud Detection</div>
            <div class='feature-desc'>Identify phishing, scams, and manipulative patterns</div>
        </div>
        <div class='feature-box'>
            <div class='feature-icon'>🎭</div>
            <div class='feature-title'>Bias Analysis</div>
            <div class='feature-desc'>Detect political, emotional, and agenda-driven framing</div>
        </div>
        <div class='feature-box'>
            <div class='feature-icon'>📈</div>
            <div class='feature-title'>Risk Assessment</div>
            <div class='feature-desc'>Comprehensive safety and reliability evaluation</div>
        </div>
        <div class='feature-box'>
            <div class='feature-icon'>🌐</div>
            <div class='feature-title'>Multi-Language</div>
            <div class='feature-desc'>Analyze content in any language with equal accuracy</div>
        </div>
    </div>
    """
    st.markdown(features_html, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 💡 How to Use")
    st.markdown("""
    <div style='color: #94A3B8; font-size: 15px; line-height: 1.8;'>
        Simply paste any text, claim, URL, email, or social media content you want to verify.
        AegisVerify will provide a comprehensive analysis including truthfulness score,
        fraud risk assessment, bias detection, and actionable recommendations.
    </div>
    """, unsafe_allow_html=True)

# -------------------------
# CHAT HISTORY
# -------------------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style='text-align: center; padding: 60px 20px; color: #64748B;'>
        <div style='font-size: 48px; margin-bottom: 20px;'>🔒</div>
        <div style='font-size: 18px; font-weight: 600; margin-bottom: 10px;'>Ready to Verify</div>
        <div style='font-size: 14px;'>Enter your content below to begin analysis</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        if role == "user":
            st.markdown(f"<div class='user-msg'>{content}</div>", unsafe_allow_html=True)
        else:
            # Render markdown for bot messages
            st.markdown(f"<div class='bot-msg'>{content}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# USER INPUT
# -------------------------
if prompt := st.chat_input("Enter content to verify (text, URL, claim, email, etc.)..."):

    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.analysis_count += 1
    
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    st.markdown(f"<div class='user-msg'>{prompt}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    try:
        # Backend request
        response, error = send_message(
            st.session_state.session,
            "ask",
            prompt
        )

        if error:
            assistant_response = f"⚠️ **Analysis Error**\n\n{error}"
            st.error(assistant_response)
        else:
            assistant_response = response or "⚠️ No response received from analysis engine."
            
            # Enhance response with better formatting if it contains structured data
            if assistant_response:
                # The response is already formatted markdown from backend
                # Just ensure it's properly displayed
                pass

        # Save assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_response
        })

        # Show assistant message with markdown rendering
        st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
        st.markdown(f"<div class='bot-msg'>{assistant_response}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    except requests.exceptions.ConnectionError:
        assistant_response = (
            "❌ **Connection Error**\n\n"
            "Unable to reach verification engine.\n\n"
            "➡️ Please ensure the backend service is running on port 8002."
        )
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.error("Connection Error: Unable to reach backend service. Please check if backend is running.")

    except requests.exceptions.RequestException as e:
        assistant_response = f"⚠️ Request failed: {e}"
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        st.error(assistant_response)

    # Force rerun to update analysis count
    st.rerun()