// Function to update switch state
function updateSwitchState(status) {
    const switchElement = document.getElementById("alarmSwitch");
    const statusLabel = document.getElementById("alarmStatus");

    if (status === "ON") {
        switchElement.checked = true;
        statusLabel.textContent = "Alarm is ON";
        statusLabel.classList.remove("text-danger");
        statusLabel.classList.add("text-success");
    } else if (status === "OFF") {
        switchElement.checked = false;
        statusLabel.textContent = "Alarm is OFF";
        statusLabel.classList.remove("text-success");
        statusLabel.classList.add("text-danger");
    }
}

// Function to update dashboard time period
function updateDashboardPeriod(period) {
    const dashboard1 = document.getElementById("dashboard1");
    const dashboard2 = document.getElementById("dashboard2");
    
    // Base URLs for both dashboards
    const baseUrl1 = "http://localhost:3000/d-solo/506e1d49-0304-4e67-814b-b3f1f20a91d5/info?orgId=1&timezone=browser&refresh=5s&theme=light&panelId=1";
    const baseUrl2 = "http://localhost:3000/d-solo/506e1d49-0304-4e67-814b-b3f1f20a91d5/info?orgId=1&timezone=browser&refresh=5s&theme=light&panelId=2";
    
    // Update URLs with new time period
    dashboard1.src = `${baseUrl1}&from=now-${period}&to=now&__feature.dashboardSceneSolo`;
    dashboard2.src = `${baseUrl2}&from=now-${period}&to=now&__feature.dashboardSceneSolo`;
}

// Event listener for time period dropdown
document.addEventListener("DOMContentLoaded", function() {
    const timePeriodSelect = document.getElementById("timePeriod");
    
    timePeriodSelect.addEventListener("change", function() {
        const selectedPeriod = this.value;
        updateDashboardPeriod(selectedPeriod);
    });
});