UI = """
 <style>
    /* General Styling */
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f8f9fa;
    }

    /* Title and Header Styling */
    h1 {
        color: #2c3e50;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Chat Input Styling */
    .stChatInput {
        border-radius: 25px;
        padding: 10px 20px;
        border: 2px solid #4CAF50;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .stChatInput:focus {
        border-color: #45a049;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    /* Button Styling */
    .stButton button {
        border-radius: 25px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        padding: 10px 20px;
        border: none;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }

    .stButton button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transform: translateY(-2px);
    }

    /* Sidebar Styling */
    .stSidebar .sidebar-content {
        background-color: #ffffff;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        padding: 20px;
        margin: 10px;
    }

    .stSidebar .sidebar-content h2 {
        color: #2c3e50;
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 15px;
    }

    /* Chat Message Styling */
    .stChatMessage {
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .stChatMessage.user {
        background-color: #e3f2fd;
        border-left: 5px solid #2196F3;
    }

    .stChatMessage.assistant {
        background-color: #f5f5f5;
        border-left: 5px solid #4CAF50;
    }

    /* Radio Button Styling */
    .stRadio > div {
        display: flex;
        gap: 10px;
    }

    .stRadio label {
        font-weight: bold;
        color: #2c3e50;
    }

    /* Spinner Styling */
    .stSpinner {
        color: #4CAF50;
    }

    /* Success Message Styling */
    .stSuccess {
        border-radius: 15px;
        background-color: #d4edda;
        color: #155724;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    </style>
"""