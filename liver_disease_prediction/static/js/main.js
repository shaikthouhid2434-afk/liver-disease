/* ─────────────────────────────────────────
   LiverCare AI — Main JavaScript
   ───────────────────────────────────────── */

// ── Gender Selection ─────────────────────
function selectGender(gender) {
  document.getElementById('genderInput').value = gender;
  document.getElementById('genderMale').classList.toggle('active', gender === 'Male');
  document.getElementById('genderFemale').classList.toggle('active', gender === 'Female');
}

// ── Sample Data Fill ─────────────────────
const SAMPLES = {
  disease: {
    age: 65, gender: 'Male',
    total_bilirubin: 0.7, direct_bilirubin: 0.1,
    alkaline_phosphotase: 187, alamine_aminotransferase: 16,
    aspartate_aminotransferase: 18, total_proteins: 6.8,
    albumin: 3.3, albumin_globulin_ratio: 0.9
  },
  healthy: {
    age: 35, gender: 'Female',
    total_bilirubin: 0.6, direct_bilirubin: 0.1,
    alkaline_phosphotase: 80, alamine_aminotransferase: 22,
    aspartate_aminotransferase: 25, total_proteins: 7.5,
    albumin: 4.2, albumin_globulin_ratio: 1.5
  }
};

function fillSample(type) {
  const data = SAMPLES[type];
  const fields = [
    'age', 'total_bilirubin', 'direct_bilirubin',
    'alkaline_phosphotase', 'alamine_aminotransferase',
    'aspartate_aminotransferase', 'total_proteins',
    'albumin', 'albumin_globulin_ratio'
  ];
  fields.forEach(field => {
    const el = document.querySelector(`[name="${field}"]`);
    if (el) {
      el.value = data[field];
      el.classList.add('highlight-field');
      setTimeout(() => el.classList.remove('highlight-field'), 1500);
    }
  });
  selectGender(data.gender);
  document.querySelector('.form-section').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Form Submit with Loading ──────────────
const form = document.getElementById('predForm');
if (form) {
  form.addEventListener('submit', function (e) {
    const gender = document.getElementById('genderInput').value;
    if (!gender) {
      e.preventDefault();
      alert('Please select a gender.');
      return;
    }
    const btn = document.getElementById('submitBtn');
    btn.innerHTML = '<span class="spinner-inline"></span> Analyzing...';
    btn.classList.add('loading');
  });
}

// ── Reset Form ────────────────────────────
function resetForm() {
  document.getElementById('genderInput').value = '';
  document.getElementById('genderMale').classList.remove('active');
  document.getElementById('genderFemale').classList.remove('active');
}

// ── Highlight animation for filled fields ─
const style = document.createElement('style');
style.textContent = `
  .highlight-field {
    border-color: #00b4d8 !important;
    background-color: rgba(0,180,216,.06) !important;
    transition: all .3s;
  }
`;
document.head.appendChild(style);
