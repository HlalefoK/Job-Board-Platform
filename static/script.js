// script.js

function showNextSection(nextSectionId) {
    const sections = document.querySelectorAll('.onboarding-section');
    sections.forEach(section => section.style.display = 'none');
    document.getElementById(nextSectionId).style.display = 'block';
}

function submitOnboarding() {
    // Placeholder for form submission logic
    alert('Onboarding completed! Redirecting to dashboard...');
    window.location.href = '/';
}
