const API_URL = "http://127.0.0.1:5001/recommend";

const symptoms = [
  'itching', 'skin_rash', 'nodal_skin_eruptions', 'chills', 'joint_pain',
  'vomiting', 'fatigue', 'weight_loss', 'cough', 'high_fever',
  'headache', 'sweating', 'malaise', 'pain_behind_the_eyes', 'back_pain',
  'stiff_neck', 'mood_swings', 'weight_gain', 'anxiety', 'irregular_heart_rate',
  'tremor', 'cramps', 'abdominal_pain', 'acidity', 'ulcers_on_tongue',
  'yellowish_skin', 'dark_urine', 'constipation'
];

// Dynamically render symptoms
const symptomContainer = document.getElementById("symptom-list");
symptoms.forEach(sym => {
  const col = document.createElement("div");
  col.classList.add("col-md-3");
  col.innerHTML = `
    <div class="form-check hover:scale-105 transition-transform duration-200">
      <input class="form-check-input symptom" type="checkbox" value="${sym}" id="${sym}">
      <label class="form-check-label" for="${sym}">
        ${sym.replaceAll('_', ' ')}
      </label>
    </div>
  `;
  symptomContainer.appendChild(col);
});

document.getElementById("submitBtn").addEventListener("click", async () => {
  const selected = [...document.querySelectorAll(".symptom:checked")].map(e => e.value);
  const age = document.getElementById("age").value;
  const gender = document.getElementById("gender").value;

  if (selected.length === 0) {
    alert("⚠️ Please select at least one symptom!");
    return;
  }

  const inputData = {};
  symptoms.forEach(s => {
    inputData[s] = selected.includes(s) ? 1 : 0;
  });
  inputData["Age"] = parseInt(age);
  inputData["Gender"] = gender;
  inputData["Blood_Pressure"] = "NORMAL";
  inputData["Cholesterol"] = "NORMAL";

  try {
    const res = await axios.post(API_URL, inputData);
    const result = res.data;

    document.getElementById("resultBox").classList.remove("hidden");
    document.getElementById("disease").innerHTML = `<b>Predicted Disease:</b> ${result.predicted_disease || "N/A"}`;
    document.getElementById("medicine").innerHTML = `<b>Recommended Medicine:</b> ${result.recommended_drug || "N/A"}`;
    document.getElementById("confidence").innerHTML = `<b>Confidence:</b> ${result.confidence}`;
    document.getElementById("notes").innerHTML = result.notes ? `<b>Note:</b> ${result.notes}` : "";

    window.scrollTo({ top: document.getElementById("resultBox").offsetTop, behavior: "smooth" });
  } catch (error) {
    alert("❌ API Connection Failed! Please make sure Flask API is running at " + API_URL);
    console.error(error);
  }
});
