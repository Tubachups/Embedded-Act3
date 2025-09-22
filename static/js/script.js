document.addEventListener("DOMContentLoaded", () => {
  const pirStatus = document.querySelector("#pir-status");
  const buzzerStatus = document.querySelector("#buzzer");

  async function fetchPirStatus() {
    try {
      const response = await fetch("/pir_status");
      const data = await response.json();
      const { status, buzzer } = data;
      pirStatus.innerText = status;
      buzzerStatus.innerText = buzzer;
    } catch (err) {
      console.error("Error fetching PIR status:", err);
    }
  }

  async function fetchPirHistory() {
    try {
      const response = await fetch("/pir_history");
      const data = await response.json();
      console.log("PIR History:", data); // <-- just console log it
    } catch (err) {
      console.error("Error fetching PIR history:", err);
    }
  }

  setInterval(() => {
    fetchPirStatus();
    fetchPirHistory();
  }, 1000);

  fetchPirStatus();
  fetchPirHistory();
});
