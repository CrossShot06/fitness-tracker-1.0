document.addEventListener("DOMContentLoaded", function () {
    const password1 = document.getElementById("id_password1");
    const password2 = document.getElementById("id_password2");
    const role = document.getElementById("id_role");

    if (password1) password1.placeholder = "Password";
    if (password2) password2.placeholder = "Confirm Password";

    if (role) {
      const defaultOption = document.createElement("option");
      defaultOption.text = "Register As";
      defaultOption.disabled = true;
      defaultOption.selected = true;
      role.insertBefore(defaultOption, role.firstChild);
    }
  });