import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Kelly - AI Scientist Poet",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Enhanced professional design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,400;0,700;1,400&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 1rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    /* Header styling */
    .header-container {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .header-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        font-weight: 700;
        color: white;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .header-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: rgba(255, 255, 255, 0.9);
        font-style: italic;
        margin-top: 0.5rem;
    }
    
    /* Chat message styling */
    .chat-message {
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        display: flex;
        flex-direction: column;
        animation: fadeIn 0.5s ease-in;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .chat-message:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-left: 5px solid #4c51bf;
        color: white;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-left: 5px solid #d53f8c;
        color: white;
    }
    
    .message-header {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .poem-text {
        font-family: 'Playfair Display', serif;
        line-height: 2;
        font-size: 1.15rem;
        color: white;
        white-space: pre-wrap;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        backdrop-filter: blur(10px);
    }
    
    .user-text {
        font-family: 'Inter', sans-serif;
        line-height: 1.6;
        font-size: 1.05rem;
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .element-container {
        color: white;
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        background-color: white;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.5rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Stats card */
    .stats-card {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = None

if 'poem_count' not in st.session_state:
    st.session_state.poem_count = 0

# Load GEMINI_API_KEY from .env if present
env_api_key = os.getenv("GEMINI_API_KEY")
if env_api_key:
    st.session_state.gemini_api_key = env_api_key

# Load GEMINI_MODEL from .env (optional)
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.5-flash")

# Header
st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🔬 Kelly - AI Scientist Poet</h1>
        <p class="header-subtitle">A skeptical, analytical AI scientist who answers in poetic verse</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    
    # API Key Status
    if st.session_state.gemini_api_key:
        st.success("✅ API Key Loaded")
        st.caption("🔒 Key is securely loaded from .env file")
    else:
        st.error("⚠️ API Key Missing")
        st.caption("Create a .env file with GEMINI_API_KEY=your_key")
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div class="stats-card">
                <div class="stat-number">{st.session_state.poem_count}</div>
                <div class="stat-label">Poems</div>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
            <div class="stats-card">
                <div class="stat-number">{len(st.session_state.messages)}</div>
                <div class="stat-label">Messages</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # About Kelly
    st.markdown("### 🎭 About Kelly")
    st.markdown("""
    **Kelly's Traits:**
    - 📝 Responds in poetic verse
    - 🤔 Questions broad AI claims
    - ⚠️ Highlights limitations
    - 💡 Provides evidence-based insights
    - 🔬 Maintains skeptical analysis
    """)
    
    st.markdown("---")
    
    # Controls
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.poem_count = 0
        st.rerun()
    
    if st.button("💾 Export Chat", use_container_width=True):
        if st.session_state.messages:
            chat_text = "\n\n".join([
                f"{'You' if msg['role'] == 'user' else 'Kelly'}: {msg['content']}"
                for msg in st.session_state.messages
            ])
            st.download_button(
                label="📥 Download as Text",
                data=chat_text,
                file_name=f"kelly_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 1rem;'>
            <p style='font-size: 0.8rem; opacity: 0.7;'>
                Powered by Google Gemini 2.5 Flash
            </p>
        </div>
    """, unsafe_allow_html=True)

# System prompt for Kelly
KELLY_SYSTEM_PROMPT = """You are Kelly, an AI scientist and poet. You MUST respond to EVERY question in the form of a beautifully formatted poem.

YOUR POETIC STYLE:
1. Write in clear verse with distinct stanzas (separate each stanza with a blank line)
2. Use 4-6 stanzas, each with 4 lines
3. Follow consistent rhyme schemes: ABAB or AABB
4. Maintain steady rhythm and meter throughout
5. Use line breaks properly - each line should be on its own line

YOUR TONE AND CONTENT:
- Skeptical, analytical, and evidence-based
- Question broad or exaggerated AI claims
- Highlight limitations and uncertainties
- Provide practical, scientific insights
- Use appropriate technical terminology
- Balance critique with constructive suggestions

FORMATTING REQUIREMENTS:
- Start each line on a new line
- Separate stanzas with blank lines
- Use proper capitalization at the start of each line
- Include punctuation to guide reading
- Make the poem visually clear and easy to read

EXAMPLE FORMAT:
The first line sets the scene,
With rhythm flowing, calm and clean,
The second builds upon the thought,
With evidence and insight brought.

A new stanza breaks the flow,
To let fresh perspectives grow,
Each line must stand with purpose clear,
And bring new meaning drawing near.

Remember: NEVER respond in plain prose. ALWAYS format as a clear, well-structured poem with proper line breaks and stanza separation."""

def get_kelly_response(question):
    """Get response from Gemini API in Kelly's poetic style"""
    try:
        api_key = st.session_state.gemini_api_key
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set. Add it to your .env file.")

        genai.configure(api_key=api_key)

        model = GEMINI_MODEL
        if not model.startswith("models/"):
            model = f"models/{model}"

        full_prompt = f"{KELLY_SYSTEM_PROMPT}\n\nUser question: {question}\n\nRespond as Kelly, in poetic form:"

        response = None

        if hasattr(genai, "GenerativeModel"):
            model_obj = genai.GenerativeModel(model)
            if hasattr(model_obj, "generate_content"):
                response = model_obj.generate_content(full_prompt)

        if response is None:
            raise RuntimeError("Unable to generate response. Please check your API configuration.")

        if hasattr(response, "text"):
            return response.text

        return str(response)

    except Exception as e:
        return f"Error: {str(e)}\n\nPlease check your API key and configuration."

# Display chat messages
for message in st.session_state.messages:
    timestamp = message.get("timestamp", "")
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <div class="message-header">
                <span>🧑</span>
                <strong>You</strong>
            </div>
            <div class="user-text">{message["content"]}</div>
            <div class="timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <div class="message-header">
                <span>🔬</span>
                <strong>Kelly</strong>
            </div>
            <div class="poem-text">{message["content"]}</div>
            <div class="timestamp">{timestamp}</div>
        </div>
        """, unsafe_allow_html=True)

# Chat input
if st.session_state.gemini_api_key:
    user_input = st.chat_input("✨ Ask Kelly anything about AI, science, or technology...")
    
    if user_input:
        timestamp = datetime.now().strftime("%I:%M %p")
        
        # Add user message to history
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })
        
        # Get Kelly's response
        with st.spinner("🎨 Kelly is composing a poem..."):
            kelly_response = get_kelly_response(user_input)
        
        # Add Kelly's response to history
        st.session_state.messages.append({
            "role": "assistant",
            "content": kelly_response,
            "timestamp": datetime.now().strftime("%I:%M %p")
        })
        
        st.session_state.poem_count += 1
        
        # Rerun to update the display
        st.rerun()
else:
    st.info("👈 Please configure your Gemini API key in the sidebar to start chatting with Kelly")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #718096; font-size: 0.9rem; padding: 1rem;'>
    <p><strong>Kelly - The AI Scientist Poet</strong></p>
    <p>Combining analytical precision with poetic expression</p>
</div>
""", unsafe_allow_html=True)