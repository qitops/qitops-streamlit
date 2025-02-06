# qitops-streamlit

## **📜 QitOps Streamlit App Specification**  

### **🛠️ Scope (MVP Features)**
The **QitOps Streamlit App** will serve as a **visual interface** for QA operations, leveraging **local JSON files** as data sources. It will have **two main tabs**:
1. **📊 Dashboard** – Displays JSON data insights in a structured, clean UI.
2. **💬 AI Chat (RAG)** – Enables users to interact with **Ollama**, incorporating **retrieval-augmented generation (RAG)** with JSON data.

---

## **📌 Features Breakdown**

### **1️⃣ Main Dashboard (Tab 1)**
- Displays **QA metrics & insights** based on JSON test data.
- Uses **Streamlit's DataFrame/Table components** for structured views.
- Supports **filtering & sorting** (e.g., by test type, priority, category).
- **File Upload** button to allow loading different JSON datasets.

#### **JSON Data Structure (Example)**
```json
{
  "tickets": [
    {
      "key": "QA-101",
      "summary": "Login Feature",
      "type": "Functional",
      "priority": "High",
      "test_cases": [
        {
          "id": "QA-101-TC-01",
          "description": "Verify successful login with valid credentials",
          "category": "Functional",
          "priority": "High"
        },
        {
          "id": "QA-101-TC-02",
          "description": "Verify error message for invalid credentials",
          "category": "Edge Case",
          "priority": "Medium"
        }
      ]
    }
  ]
}
```

#### **Dashboard View**
- **Key Metrics** (Total tickets, test cases, functional vs. edge cases, priorities).
- **Expandable Sections** for each ticket with test case breakdown.
- **Sorting & Filtering** (by priority, category).

---

### **2️⃣ AI Chat (Tab 2)**
- **Chat UI** powered by **Ollama** (local LLM).
- **Retrieval-Augmented Generation (RAG) Setup**:
  - Retrieves **relevant JSON data** as context for AI responses.
  - Enables **QA-specific queries** about test coverage, missing cases, and risk analysis.
  
#### **Example Queries**
- *"Summarize test coverage for all High-Priority tickets."*
- *"What edge cases are covered in the dataset?"*
- *"Suggest additional test scenarios for this feature."*

#### **Technical Approach**
- Uses **Ollama’s API** with a **custom system prompt**:
  - Injects **retrieved JSON data** into context.
  - Refines responses based on **QA-related patterns**.

---

## **🔧 Implementation Plan**
1. **Set up Streamlit app with two tabs** (`st.sidebar` for navigation).
2. **Implement JSON file loading & processing**.
3. **Build dashboard UI**:
   - Display key insights.
   - Implement filtering/sorting for test cases.
4. **Set up AI Chat**:
   - Connect to **Ollama**.
   - Implement RAG pipeline to inject JSON context.

---

## **🌱 Future Enhancements (Beyond MVP)**
- **Live GitHub/JIRA Data Integration**.
- **Test Automation Insights** (e.g., pass/fail trends).
- **Risk-Based Test Selection**.
- **Automated AI-Driven Test Case Suggestions**.
