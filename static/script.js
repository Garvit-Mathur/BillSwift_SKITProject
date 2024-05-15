// script.js
/*
document.getElementById('loginBtn').addEventListener('click', function() {
    toggleForm('loginForm');
  });
  
  document.getElementById('signupBtn').addEventListener('click', function() {
    toggleForm('signupForm');
  });
  
  document.getElementById('aboutBtn').addEventListener('click', function() {
    alert('This is the About page.');
  });
  
  document.getElementById('contactBtn').addEventListener('click', function() {
    alert('Please contact us at support@billswift.com');
  });
  
  function toggleForm(formId) {
    const form = document.getElementById(formId);
    const otherFormId = formId === 'loginForm' ? 'signupForm' : 'loginForm';
    const otherForm = document.getElementById(otherFormId);
  
    form.style.display = 'block';
    otherForm.style.display = 'none';
  }
  */
 // script.js

document.getElementById('loginBtn').addEventListener('click', function() {
    toggleForm('loginForm');
  });
  
  document.getElementById('signupBtn').addEventListener('click', function() {
    toggleForm('signupForm');
  });
  
  document.getElementById('aboutBtn').addEventListener('click', function() {
    window.location.href = 'about.html';
  });
  
  document.getElementById('contactBtn').addEventListener('click', function() {
    alert('Please contact us at support@billswift.com');
  });
  
  function toggleForm(formId) {
    const form = document.getElementById(formId);
    const otherFormId = formId === 'loginForm' ? 'signupForm' : 'loginForm';
    const otherForm = document.getElementById(otherFormId);
  
    form.style.display = 'block';
    otherForm.style.display = 'none';
  }
  