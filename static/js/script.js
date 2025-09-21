document.addEventListener("DOMContentLoaded", () => {
  async function fetchPirStatus() {
    try {
      const response = await fetch("/pir_status");
      const data = await response.json();
      document.getElementById("pir-status").innerText = data.status;
    } catch (err) {
      console.error("Error fetching PIR status:", err);
    }
  }

  setInterval(fetchPirStatus, 1000);
  fetchPirStatus(); 
});
