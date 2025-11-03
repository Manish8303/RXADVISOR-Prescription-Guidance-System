const API_URL = "http://127.0.0.1:5001/recommend";

const ALL_SYMPTOMS = [
  'itching', 'skin_rash', 'joint_pain', 'vomiting', 'fatigue',
  'cough', 'high_fever', 'headache', 'malaise', 'pain_behind_the_eyes',
  'back_pain', 'stiff_neck', 'anxiety', 'cramps', 'abdominal_pain',
  'acidity', 'constipation', 'dark_urine', 'sweating', 'weight_loss'
];

// Populate checkboxes dynamically
const symptomList = document.getElementById('symptom-list');
ALL_SYMPTOMS.forEach(symptom => {
  const label = symptom.replace(/_/g, ' ').toUpperCase();
  const div = document.createElement('div');
  div.className = 'form-check';
  div.innerHTML = `
    <input class="form-check-input symptom-checkbox" type="checkbox" value="${symptom}" id="${symptom}">
    <label class="form-check-label text-gray-700" for="${symptom}">${label}</label>
  `;
  symptomList.appendChild(div);
});

// Check API status
fetch(API_URL)
  .then(() => document.getElementById('api-status').innerHTML = '<span class="text-green-300">🟢 Connected</span>')
  .catch(() => document.getElementById('api-status').innerHTML = '<span class="text-red-300">🔴 Offline</span>');

// Handle Analyze button
document.getElementById('analyzeBtn').addEventListener('click', async () => {
  const selected = [...document.querySelectorAll('.symptom-checkbox:checked')].map(cb => cb.value);
  const resultSection = document.getElementById('result-section');

  if (selected.length === 0) {
    alert('Please select at least one symptom!');
    return;
  }

  const payload = Object.fromEntries(ALL_SYMPTOMS.map(s => [s, selected.includes(s) ? 1 : 0]));

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const data = await response.json();

    document.getElementById('disease').innerHTML = `<b>Disease:</b> ${data.predicted_disease || 'N/A'}`;
    document.getElementById('medicine').innerHTML = `<b>Recommended Medicine:</b> ${data.recommended_drug || 'Not Available'}`;
    document.getElementById('confidence').innerHTML = `<b>Confidence:</b> ${data.confidence || '0%'}`;
    document.getElementById('notes').innerHTML = data.notes ? `Notes: ${data.notes}` : '';

    resultSection.classList.remove('hidden');
  } catch (err) {
    alert('API connection failed. Please check Flask server.');
  }
});
