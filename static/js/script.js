document.addEventListener("DOMContentLoaded", () => {
  const pirStatus = document.querySelector("#pir-status");

  async function fetchPirStatus() {
    try {
      const response = await fetch("/pir_status");
      const data = await response.json();
      const { status} = data;
      pirStatus.innerText = status;
    } catch (err) {
      console.error("Error fetching PIR status:", err);
    }
  }

  setInterval(fetchPirStatus, 1000);
  fetchPirStatus(); 
});
