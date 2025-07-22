# streamlit_app.py
import streamlit as st
from agent import ask_llm
from tools.search_tool import search_web
from tools.summarize_tool import summarize_text
from tools.email_tool import send_email, test_email_connection
from tools.launcher_tool import open_file_by_name

# Page configuration with modern styling
st.set_page_config(
    page_title="AI Task Assistant", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🤖"
)

# Custom CSS for dark modern styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Global dark theme styling */
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 25%, #2d1b69 50%, #1a1a1a 75%, #0c0c0c 100%);
        background-attachment: fixed;
        color: #ffffff;
    }
    
    /* Main container styling */
    .main-container {
        background: rgba(15, 15, 15, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 25px;
        padding: 2.5rem;
        margin: 1rem;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5), 
                    inset 0 1px 0 rgba(255, 255, 255, 0.1),
                    0 0 0 1px rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Title styling */
    .main-title {
        text-align: center;
        color: #ffffff;
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        background: linear-gradient(135deg, #00d4ff 0%, #9c40ff 50%, #ff006e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 30px rgba(156, 64, 255, 0.3);
    }
    
    .subtitle {
        text-align: center;
        color: #a0a0a0;
        font-size: 1.3rem;
        font-weight: 400;
        margin-bottom: 3rem;
        opacity: 0.9;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1cypcdb {
        background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Task cards */
    .task-card {
        background: linear-gradient(135deg, 
                    rgba(20, 20, 20, 0.9) 0%, 
                    rgba(30, 30, 30, 0.8) 50%, 
                    rgba(25, 25, 25, 0.9) 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .task-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(156, 64, 255, 0.5), transparent);
    }
    
    .task-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4),
                    0 0 30px rgba(156, 64, 255, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: rgba(156, 64, 255, 0.3);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #9c40ff 0%, #00d4ff 100%);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 1rem 2.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 8px 25px rgba(156, 64, 255, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.2);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(156, 64, 255, 0.6),
                    0 0 20px rgba(0, 212, 255, 0.3);
        background: linear-gradient(135deg, #b350ff 0%, #00e4ff 100%);
    }
    
    /* Input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(30, 30, 30, 0.8);
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        padding: 1rem;
        font-size: 1rem;
        color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #9c40ff;
        box-shadow: 0 0 0 3px rgba(156, 64, 255, 0.2),
                    0 0 20px rgba(156, 64, 255, 0.1);
        background: rgba(40, 40, 40, 0.9);
    }
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {
        color: #666666;
    }
    
    /* Response containers */
    .response-container {
        background: linear-gradient(135deg, 
                    rgba(25, 25, 25, 0.9) 0%, 
                    rgba(35, 35, 35, 0.8) 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 4px solid #9c40ff;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Icons */
    .task-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 0 10px rgba(156, 64, 255, 0.3));
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #00ff88 0%, #00cc6a 100%);
        border-radius: 15px;
        color: #000000;
        font-weight: 600;
    }
    
    .stError {
        background: linear-gradient(135deg, #ff4757 0%, #ff3742 100%);
        border-radius: 15px;
        color: #ffffff;
        font-weight: 600;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: rgba(30, 30, 30, 0.8);
        border-radius: 15px;
        border: 2px solid rgba(255, 255, 255, 0.1);
        color: #ffffff;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff;
    }
    
    /* Spinner styling */
    .stSpinner > div {
        border-top-color: #9c40ff !important;
    }
    
    /* Text styling */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }
    
    p, div, span {
        color: #e0e0e0;
    }
    
    /* Code block styling */
    .stCode {
        background: rgba(20, 20, 20, 0.9) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }
    
    /* Markdown styling */
    .stMarkdown {
        color: #e0e0e0;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(20, 20, 20, 0.5);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #9c40ff, #00d4ff);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #b350ff, #00e4ff);
    }
</style>
""", unsafe_allow_html=True)

# Main container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-title">🤖 AI Task Assistant</div>
<div class="subtitle">Your intelligent companion for seamless productivity and automation</div>
""", unsafe_allow_html=True)

# Sidebar with modern styling
with st.sidebar:
    st.markdown("### 🎯 Select Your Task")
    st.markdown("---")
    
    task = st.selectbox(
        "Choose what you'd like to do:",
        [
            "💬 Ask AI anything",
            "🔍 Search the web", 
            "📝 Summarize text",
            "📧 Send email",
            "🤖 Smart email assistant",
            "📁 Open file"
        ],
        format_func=lambda x: x
    )
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #a0a0a0; font-size: 0.9rem; margin-top: 2rem;'>
        <p>✨ Dark Modern AI Assistant</p>
        <p>🌙 Enhanced Night Mode</p>
        <p>🚀 Built with Streamlit</p>
    </div>
    """, unsafe_allow_html=True)

# Main content area with task-specific interfaces
if "💬 Ask AI anything" in task:
    st.markdown("""
    <div class="task-card">
        <div class="task-icon">🧠</div>
        <h3 style="color: #2d3748; margin-bottom: 1rem;">Ask AI Anything</h3>
        <p style="color: #718096; margin-bottom: 1.5rem;">Get intelligent responses to any question or request</p>
    """, unsafe_allow_html=True)
    
    query = st.text_input(
        "What would you like to know?",
        placeholder="Ask me anything... e.g., 'Explain quantum computing in simple terms'"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submit_btn = st.button("✨ Get Answer", use_container_width=True)
    
    if submit_btn and query:
        with st.spinner("🤔 Thinking..."):
            response = ask_llm(query)
        
        st.markdown('<div class="response-container">', unsafe_allow_html=True)
        st.markdown("### 💡 AI Response")
        st.write(response)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif "🔍 Search the web" in task:
    st.markdown("""
    <div class="task-card">
        <div class="task-icon">🌐</div>
        <h3 style="color: #2d3748; margin-bottom: 1rem;">Web Search & Summary</h3>
        <p style="color: #718096; margin-bottom: 1.5rem;">Search the internet and get intelligent summaries</p>
    """, unsafe_allow_html=True)
    
    query = st.text_input(
        "Search Query",
        placeholder="Enter your search terms... e.g., 'latest AI developments 2024'"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        search_btn = st.button("🔍 Search & Summarize", use_container_width=True)
    
    if search_btn and query:
        with st.spinner("🌐 Searching the web..."):
            response = search_web(query)
        
        st.markdown('<div class="response-container">', unsafe_allow_html=True)
        st.markdown("### 📊 Search Results & Summary")
        st.write(response)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif "📝 Summarize text" in task:
    st.markdown("""
    <div class="task-card">
        <div class="task-icon">📄</div>
        <h3 style="color: #2d3748; margin-bottom: 1rem;">Text Summarization</h3>
        <p style="color: #718096; margin-bottom: 1.5rem;">Transform long text into concise, meaningful summaries</p>
    """, unsafe_allow_html=True)
    
    text = st.text_area(
        "Paste your text here",
        placeholder="Paste the text you want to summarize...",
        height=200
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        summarize_btn = st.button("📝 Create Summary", use_container_width=True)
    
    if summarize_btn and text:
        with st.spinner("📊 Analyzing and summarizing..."):
            summary = summarize_text(text)
        
        st.markdown('<div class="response-container">', unsafe_allow_html=True)
        st.markdown("### 📋 Summary")
        st.write(summary)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif "📧 Send email" in task:
    st.markdown("""
    <div class="task-card">
        <div class="task-icon">✉️</div>
        <h3 style="color: #2d3748; margin-bottom: 1rem;">Email Sender</h3>
        <p style="color: #718096; margin-bottom: 1.5rem;">Send emails quickly and efficiently</p>
    """, unsafe_allow_html=True)
    
    # Add email test button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔧 Test Email Config"):
            with st.spinner("Testing email configuration..."):
                test_result = test_email_connection()
            if "✅" in test_result:
                st.success(test_result)
            else:
                st.error(test_result)
    
    col1, col2 = st.columns(2)
    with col1:
        to = st.text_input("📧 Recipient Email", placeholder="recipient@example.com")
    with col2:
        subject = st.text_input("📋 Subject", placeholder="Email subject")
    
    body = st.text_area(
        "💬 Message Body",
        placeholder="Write your email message here...",
        height=150
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        send_btn = st.button("📤 Send Email", use_container_width=True)
    
    if send_btn:
        if not to or not subject or not body:
            st.error("❌ Please fill in all fields: recipient, subject, and message body.")
        else:
            with st.spinner("📤 Sending email..."):
                result = send_email(subject, body, to)
            
            if "✅" in result or "successfully" in result.lower():
                st.success(result)
            else:
                st.error(result)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif "🤖 Smart email assistant" in task:
    st.markdown("""
    <div class="task-card">
        <div class="task-icon">🤖</div>
        <h3 style="color: #2d3748; margin-bottom: 1rem;">Smart Email Assistant</h3>
        <p style="color: #718096; margin-bottom: 1.5rem;">Describe your email task and let AI write and send it for you</p>
    """, unsafe_allow_html=True)
    
    prompt = st.text_input(
        "📝 Email Task Description",
        placeholder="e.g., 'write email to john@company.com about project deadline extension'"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_btn = st.button("🤖 Generate Email", use_container_width=True)
    
    if generate_btn and prompt:
        import re
        
        # Extract email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+', prompt)
        if not email_match:
            st.error("❌ Could not find an email address in your prompt.")
        else:
            to_email = email_match.group(0)
            task_desc = prompt.replace(to_email, "").replace("email", "").replace("to", "").strip()
            if not task_desc:
                st.error("❌ Couldn't understand the prompt. Use: 'write email to someone@example.com about ...'")
            else:
                with st.spinner("🤖 Crafting your email..."):
                    # Create prompts
                    body_prompt = (
                        f"Write the body of a professional but friendly email about: {task_desc}. "
                        "Do not include the subject line. Address the recipient directly without placeholders. "
                        "Keep it concise and natural."
                    )
                    subject_prompt = (
                        f"Generate only one short, professional subject line for an email about: {task_desc}. "
                        "Do not include multiple options or extra text."
                    )
                    
                    # Get responses from LLM
                    email_body = ask_llm(body_prompt)
                    email_subject = ask_llm(subject_prompt)
                
                # Store in session state for confirmation
                st.session_state.generated_email = {
                    'to': to_email,
                    'subject': email_subject,
                    'body': email_body
                }
    
    # Display email preview if generated
    if hasattr(st.session_state, 'generated_email') and st.session_state.generated_email:
        email_data = st.session_state.generated_email
        
        st.markdown('<div class="response-container">', unsafe_allow_html=True)
        st.markdown("### 📧 Email Preview")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown("**📧 To:**")
            st.markdown("**📋 Subject:**")
        with col2:
            st.code(email_data['to'])
            st.write(email_data['subject'])
        
        st.markdown("**💬 Body:**")
        st.text_area("", email_data['body'], height=200, key="preview_body", disabled=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            if st.button("✅ Confirm & Send", use_container_width=True):
                with st.spinner("📤 Sending email..."):
                    result = send_email(email_data['subject'], email_data['body'], email_data['to'])
                st.success(f"✅ {result}")
                # Clear the session state after sending
                del st.session_state.generated_email
        
        with col2:
            if st.button("🔄 Regenerate", use_container_width=True):
                # Clear session state to allow regeneration
                del st.session_state.generated_email
                st.rerun()
        
        with col3:
            if st.button("❌ Cancel", use_container_width=True):
                del st.session_state.generated_email
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

elif "📁 Open file" in task:
    st.markdown("""
    <div class="task-card">
        <div class="task-icon">📂</div>
        <h3 style="color: #2d3748; margin-bottom: 1rem;">File Launcher</h3>
        <p style="color: #718096; margin-bottom: 1.5rem;">Open files and applications by name</p>
    """, unsafe_allow_html=True)
    
    file_name = st.text_input(
        "📁 File Name",
        placeholder="Enter filename (e.g., resume.pdf, document.docx)"
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        open_btn = st.button("📂 Open File", use_container_width=True)
    
    if open_btn and file_name:
        with st.spinner("📁 Opening file..."):
            result = open_file_by_name(file_name)
        
        st.markdown('<div class="response-container">', unsafe_allow_html=True)
        st.markdown("### 📋 Result")
        st.write(result)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #a0a0a0; padding: 2rem 0;'>
    <p style='font-size: 1rem; font-weight: 600;'>🌟 Powered by Next-Gen AI Technology</p>
    <p style='font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.8;'>Elevate your workflow with intelligent dark-mode automation</p>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)