import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Google Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠ GOOGLE_API_KEY not found! Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# Set up Streamlit page
st.set_page_config(page_title="Food Nutrition Analyzer", page_icon="🍽")

# Sidebar for file upload
st.sidebar.title("Navigation")
st.sidebar.header("Upload Section")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display main title
st.title("🍽 **Food Nutrition Analyzer**") # Highlighted Main Title

# Show the uploaded image if available
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Define function to prepare image data
def input_image_setup(uploaded_file):
    if uploaded_file:
        bytes_data = uploaded_file.getvalue()
        return [{"mime_type": uploaded_file.type, "data": bytes_data}]
    else:
        return None

# Define function to get AI response
def get_gemini_response(input_text, image_data):
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content([input_text, image_data[0]]) if image_data else None
    return response.text if response else "No valid image found for processing."

# Updated AI prompt with all new requirements and exact output order
input_prompt = """
Here is a detailed report for the food.
You are an expert nutritionist and food analyst. Analyze the food in the uploaded image and provide detailed information strictly adhering to the following structured format. Do NOT add any introductory sentences or phrases other than the first line provided ("Here is a detailed report for the food.").

If the food appears spoiled, rotten, molded, discolored, or unsafe to consume, clearly state this. In such a case, *do NOT* include nutritional information, health benefits, diet plans, advantages, disadvantages, age group recommendations, or a health rating. Just explain why the food is spoiled, the visible signs, and the specific health risks (diseases/symptoms) associated with consuming it.

Use the following format, ensuring all requested headings and key terms are bolded as specified:

### 🍛 **Food Name & Description**
- **Name of the food**: [Provide food name]
- **Description**: [Give a concise, two-line description or background about the food, suitable for both spoiled and good food.]

### 🛑 **Spoilage Status**
- **Status**: [Is the food spoiled? If yes, clearly say: "This food is spoiled and not safe for consumption." If no, say: "This food appears fresh and safe for consumption."]
- **Visible Signs of Spoilage**: [Mention specific visible signs like mold growth (e.g., green, white fuzz 🦠), significant discoloration (e.g., browning, blackening 🎨), slime formation (e.g., slippery texture 💧), foul odor (e.g., sour, putrid smell 🤢), abnormal texture (e.g., mushy, overly soft 🥔), etc. If not spoiled, state: "No visible signs of spoilage detected."]
- **Health Risks of Consumption**: [ONLY include this section if the food is spoiled. Explain why consuming spoiled food is dangerous, mentioning potential **infections** and **diseases** as bullet points below, along with common symptoms:]
  - **Infections/Diseases**:
    - **[Specific bacterial/viral infection, e.g., Salmonella, E. coli, Listeriosis, Botulism]**
    - **[Another specific infection/disease]**
    - [Continue with other relevant infections/diseases]
  - **Common Symptoms**: [e.g., nausea, vomiting, diarrhea, abdominal cramps, fever, headache, muscle aches]

[If food is *not spoiled*, continue with the details below:]

### 📝 **Ingredients and Their Nutrients**
- **Ingredient 1** 🥕: [Brief description of ingredient 1]. **Key Nutrients**: [List 2-3 prominent nutrients this ingredient provides, e.g., "Vitamin A, Fiber, Antioxidants"].
- **Ingredient 2** 🥦: [Brief description of ingredient 2]. **Key Nutrients**: [List 2-3 prominent nutrients this ingredient provides, e.g., "Vitamin C, K, Folate"].
- **Ingredient 3** 🍞: [Brief description of ingredient 3]. **Key Nutrients**: [List 2-3 prominent nutrients this ingredient provides, e.g., "Complex Carbohydrates, B Vitamins, Iron"].
- **Ingredient 4** 🥩: [Brief description of ingredient 4]. **Key Nutrients**: [List 2-3 prominent nutrients this ingredient provides, e.g., "High-Quality Protein, Iron, B12"].
- **Ingredient 5** 🥛: [Brief description of ingredient 5]. **Key Nutrients**: [List 2-3 prominent nutrients this ingredient provides, e.g., "Calcium, Vitamin D, Protein"].
- ... (Add more ingredients with appropriate emojis and their nutritional highlights)

### 📊 **Overall Nutrition Summary (per typical serving)**
- **Calories**: [X kcal]
- **Protein**: [X grams]
- **Carbohydrates**: [X grams]
- **Fats**: [X grams]
- **Fiber**: [X grams]
- **Key Vitamins & Minerals**: [List the most significant vitamins and minerals the overall dish provides, e.g., "Rich in Vitamin C, a good source of Iron, contains B vitamins."]. Briefly explain why these are important for health.

### 💪 **Benefits for Your Body**
- Based on the food and its key ingredients, here are some benefits for your overall well-being:
  - **Overall Health**: [Explain general benefits for the body, linking to key nutrients or food properties.]
  - **Hair Health**: [Explain how the food/its nutrients can support hair health/growth, if applicable.]
  - **Eye Health**: [Explain how the food/its nutrients can benefit eye health, if applicable.]
  - **Heart Health**: [Explain how the food/its nutrients can contribute to cardiovascular health, if applicable.]
  - **Muscle Development**: [Explain how the food/its nutrients support muscle growth/repair, if applicable.]
  - **Digestive Health**: [Explain how the food/its nutrients benefit digestion.]
  - **Immune System**: [Explain how the food/its nutrients boost immunity.]
  - **Bone Health**: [Explain how the food/its nutrients support bone strength.]
  - **Skin Health**: [Explain how the food/its nutrients contribute to healthy skin.]

### 🗓️ **Weekly Based Diet Guidance**
- **For Weight Loss**: [Provide general, weekly-based guidance or example meal ideas on how this food could be incorporated into a weight loss diet (e.g., "Include 2-3 times a week as a lean protein source," "Pair with large salads," "Focus on smaller portions").]
- **For Weight Gain**: [Provide general, weekly-based guidance or example meal ideas on how this food could be incorporated into a weight gain diet (e.g., "Include 4-5 times a week," "Pair with complex carbs and healthy fats," "Increase portion sizes").]

### ⚕️ **Food Suitability for Specific Health Conditions**
- **For Diabetes Patients**: [Discuss suitability, potential impact on blood sugar, and recommendations for consumption (e.g., portion control, preparation methods) based on the food's characteristics.]
- **For Cancer Patients**: [Discuss suitability, potential benefits (e.g., antioxidant content, immune support) or considerations (e.g., ease of digestion during treatment) based on the food's characteristics.]
- **For Heart Attack Patients**: [Discuss suitability, potential benefits for cardiovascular health (e.g., healthy fats, fiber, low sodium) or considerations (e.g., fat content, sodium content) based on the food's characteristics.]

### ✅ **Advantages & ❌ Disadvantages**
✅ **Advantages**:
1. [Benefit 1]
2. [Benefit 2]
3. [Benefit 3]

❌ **Disadvantages**:
1. [Risk 1]
2. [Risk 2]
3. [Risk 3]

### 👶 **Recommended Age Group**
- **Suitable for**: [Provide a point-wise list with emojis for suitable age groups and explanations:]
  - 👶 **Infants (6-12 months)**: [Explanation why suitable, e.g., "Suitable due to soft texture when pureed and essential nutrients for rapid growth."]
  - 🧒 **Young Children (1-12 years)**: [Explanation why suitable, e.g., "Excellent for energy and bone development due to its balanced nutrients."]
  - 🧑‍🎓 **Teenagers (13-18 years)**: [Explanation why suitable, e.g., "Supports rapid growth and high energy demands, providing essential protein and vitamins."]
  - 👨‍👩‍👧‍👦 **Adults (19-64 years)**: [Explanation why suitable, e.g., "Contributes to overall health, energy maintenance, and muscle repair."]
  - 👵 **Seniors (65+ years)**: [Explanation why suitable, e.g., "Provides easily digestible nutrients and supports muscle mass maintenance."]
  - ✨ **All Healthy Age Groups**: [Explanation if universally suitable, e.g., "A versatile and nutrient-dense food suitable for healthy individuals across all age ranges."]
- **Not recommended for**: [Provide a point-wise list with emojis for age groups to avoid and explanations:]
  - 🍼 **Infants (0-6 months)**: [Explanation why not recommended, e.g., "Not suitable due to undeveloped digestive systems and potential choking hazards for solids."]
  - 🚫 **Specific Allergies/Conditions**: [Explanation if applicable, e.g., "Individuals with [mention specific allergy/condition] should avoid due to [reason]."]
  - ✅ **N/A**: [If no specific restrictions for healthy individuals across all age groups.]

### ⭐ **Health Rating**
- Based on the nutritional value, this food gets a rating of **[X/10]** in terms of health benefits. [Provide a brief explanation for the rating, e.g., "High rating due to balanced macronutrients and rich vitamin content." or "Lower rating due to high saturated fat and sugar content."].
"""

# Button to analyze food
if st.button("🍽 **Analyse this Food**"): # Highlighted button
    if uploaded_file is None:
        st.warning("⚠ Please upload an image before clicking Analyse.")
    else:
        # The AI will now generate the intro phrase itself.
        with st.spinner("Analyzing food... Please wait for the results 🍕🥗🍎"):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data)

        # Display "Food analysis completed!" message after processing
        st.success("✅ Food Analysis Completed!")
        st.subheader("📊 **Food Analysis Report**") # Highlighted subheader
        st.write(response)