import streamlit as st
from PIL import Image
from datetime import datetime
import json

# -------------------------------
# Mock Inventory Database
# -------------------------------
INVENTORY = {
    "laptop": {"stock": 12, "status": "Available"},
    "mouse": {"stock": 0, "status": "Out of Stock"},
    "keyboard": {"stock": 3, "status": "Low Stock"}
}

# -------------------------------
# Vision Module (Image → Item)
# -------------------------------
def detect_item_from_image(image_name):
    name = image_name.lower()
    if "laptop" in name:
        return "Laptop"
    elif "mouse" in name:
        return "Mouse"
    elif "keyboard" in name:
        return "Keyboard"
    return "Unknown Item"

# -------------------------------
# Function Calling (Inventory)
# -------------------------------
def check_inventory(item):
    return INVENTORY.get(item.lower(), {"stock": 0, "status": "Item Not Found"})

# -------------------------------
# Agent Reasoning Engine
# -------------------------------
def agent_reasoning(image_name, location, priority):
    reasoning_steps = []

    reasoning_steps.append("Image received from user")
    item = detect_item_from_image(image_name)
    reasoning_steps.append(f"Identified item as {item}")

    inventory = check_inventory(item)
    reasoning_steps.append("Inventory function called")

    if inventory["stock"] < 5:
        action = "Reorder item"
        reasoning_steps.append("Stock below threshold → Reorder required")
    else:
        action = "No action needed"
        reasoning_steps.append("Stock sufficient → No action required")

    response = {
        "item": item,
        "inventory": inventory,
        "action": action,
        "metadata": {
            "location": location,
            "priority": priority,
            "timestamp": datetime.now().isoformat()
        },
        "agent_reasoning": reasoning_steps
    }

    return response

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="Smart Inventory Auditor", layout="centered")

st.title("🧠 Smart Inventory Auditor (Agentic AI)")
st.write("Upload an image and let the agent analyze inventory automatically.")

uploaded_file = st.file_uploader("Upload item image", type=["jpg", "png", "jpeg"])
location = st.selectbox("Warehouse Location", ["Warehouse A", "Warehouse B", "Warehouse C"])
priority = st.selectbox("Priority", ["Low", "Normal", "High"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze Inventory"):
        result = agent_reasoning(
            uploaded_file.name,
            location,
            priority
        )

        st.success("✅ Analysis Completed")

        st.subheader("📌 Agent Reasoning Steps")
        for step in result["agent_reasoning"]:
            st.write("•", step)

        st.subheader("📊 Final Structured Output")
        st.json(result)
