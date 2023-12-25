function addTag() {
    const tagInput = document.getElementById('tagInput');
    const tagText = tagInput.value.trim();

    if (tagText !== '') {
      const tagsList = document.getElementById('tagsList');
      const tagElement = document.createElement('div');
      tagElement.textContent = tagText;
      tagsList.appendChild(tagElement);

      tagInput.value = '';
    }
  }

  document.getElementById('serverRegistrationForm').addEventListener('submit', function (event) {
    const errorMessage = document.getElementById('errorMessage');
    errorMessage.textContent = ''; // Clear previous error messages

    // Add your form validation logic here

    // Example: Check if server name is at least 3 characters long
    const serverName = document.getElementById('serverName').value;
    if (serverName.length < 3) {
      errorMessage.textContent = 'Имя сервера должно быть не менее 3 символов.';
      event.preventDefault(); // Prevent form submission
    }
  });

