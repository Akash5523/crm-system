// Sample JS file
console.log("CRM static JS loaded.");

// Auto-dismiss Bootstrap alerts after 3 seconds
document.addEventListener("DOMContentLoaded", function () {
    setTimeout(() => {
      document.querySelectorAll(".alert").forEach((alert) => {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        bsAlert.close();
      });
    }, 3000);
  });
  