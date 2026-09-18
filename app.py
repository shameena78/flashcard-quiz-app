import streamlit as st

# 1. Page Setup & Configuration
st.set_page_config(page_title="Flashcard Quiz App", page_icon="📇", layout="centered")

# 2. Initialize Session State Variables
if "cards" not in st.session_state:
    # Default starter cards
    st.session_state.cards = [
        {"question": "What is Python?", "answer": "A high-level, interpreted programming language known for readability."},
        {"question": "What does 'st.session_state' do in Streamlit?", "answer": "It allows you to store and persist variables across app reruns."},
        {"question": "What is a dynamic data structure in Python?", "answer": "A List, because it can grow and shrink in size dynamically."}
    ]

if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False


# 3. Main Application Title & Clean UI Header
st.title("📇 Flashcard Quiz App")
st.write("Test your knowledge or customize your own study deck below!")
st.markdown("---")

cards = st.session_state.cards

# Check if there are any cards available
if len(cards) > 0:
    # Ensure index stays in valid range (e.g., after deletions)
    if st.session_state.current_index >= len(cards):
        st.session_state.current_index = len(cards) - 1
    if st.session_state.current_index < 0:
        st.session_state.current_index = 0

    idx = st.session_state.current_index
    current_card = cards[idx]

    # Display Current Progress Card Number
    st.subheader(f"Card {idx + 1} of {len(cards)}")

    # Clean UI Visual Box for the Flashcard
    with st.container(border=True):
        st.markdown(f"### **Question:**")
        st.markdown(f"#### {current_card['question']}")
        
        st.write("") # Spacer
        
        if st.session_state.show_answer:
            st.success(f"**Answer:** {current_card['answer']}")
        else:
            if st.button("👁️ Show Answer", use_container_width=True):
                st.session_state.show_answer = True
                st.rerun()

    st.write("") # Spacer

    # Navigation Controls (Previous / Next Side-by-Side)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Previous", use_container_width=True):
            if st.session_state.current_index > 0:
                st.session_state.current_index -= 1
                st.session_state.show_answer = False
                st.rerun()
    with col2:
        if st.button("Next ➡️", use_container_width=True):
            if st.session_state.current_index < len(cards) - 1:
                st.session_state.current_index += 1
                st.session_state.show_answer = False
                st.rerun()
else:
    st.warning("⚠️ No flashcards in your deck! Use the sidebar to add some cards.")

# 4. Sidebar Panel for Customization (Add, Edit, Delete)
st.sidebar.title("🛠️ Deck Customization")

# --- SECTION A: ADD NEW CARD ---
st.sidebar.subheader("➕ Add New Flashcard")
with st.sidebar.form("add_form", clear_on_submit=True):
    new_q = st.text_input("Front (Question):")
    new_a = st.text_area("Back (Answer):")
    submitted = st.form_submit_button("Add Card")
    if submitted:
        if new_q and new_a:
            st.session_state.cards.append({"question": new_q, "answer": new_a})
            st.sidebar.success("Card added successfully!")
            st.rerun()
        else:
            st.sidebar.error("Both fields are required!")

# --- SECTION B: EDIT OR DELETE CARDS ---
if len(cards) > 0:
    st.sidebar.markdown("---")
    st.sidebar.subheader("✏️ Edit / Delete Cards")
    
    # Dropdown selector to choose which card to modify
    card_options = [f"Card {i+1}: {c['question'][:20]}..." for i, c in enumerate(cards)]
    selected_card_idx = st.sidebar.selectbox("Select a card to Modify:", range(len(cards)), format_func=lambda x: card_options[x])
    
    # Text boxes loaded up with the selected card's current text
    edit_q = st.sidebar.text_input("Edit Question:", value=cards[selected_card_idx]['question'])
    edit_a = st.sidebar.text_area("Edit Answer:", value=cards[selected_card_idx]['answer'])
    
    edit_col1, edit_col2 = st.sidebar.columns(2)
    with edit_col1:
        if st.button("💾 Save Changes", use_container_width=True):
            st.session_state.cards[selected_card_idx]['question'] = edit_q
            st.session_state.cards[selected_card_idx]['answer'] = edit_a
            st.sidebar.success("Card updated!")
            st.rerun()
            
    with edit_col2:
        if st.button("🗑️ Delete Card", use_container_width=True):
            st.session_state.cards.pop(selected_card_idx)
            # Reset index tracker if we delete the last item
            if st.session_state.current_index >= len(st.session_state.cards):
                st.session_state.current_index = max(0, len(st.session_state.cards) - 1)
            st.session_state.show_answer = False
            st.rerun()