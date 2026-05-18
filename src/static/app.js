document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");

  function renderActivityCard(name, details) {
    const activityCard = document.createElement("article");
    activityCard.className = "activity-card";

    const spotsLeft = details.max_participants - details.participants.length;
    const participantsMarkup =
      details.participants.length > 0
        ? details.participants.map((participant) => `<li class="participant-item"><span>${participant}</span><button class="delete-btn" data-activity="${name}" data-email="${participant}" title="Remove participant">✕</button></li>`).join("")
        : '<li class="participant-empty">No participants yet</li>';

    activityCard.innerHTML = `
      <div class="activity-card-header">
        <div>
          <h4>${name}</h4>
          <p class="activity-description">${details.description}</p>
        </div>
        <span class="availability-pill">${spotsLeft} spots left</span>
      </div>
      <div class="activity-meta">
        <p><strong>Schedule:</strong> ${details.schedule}</p>
      </div>
      <div class="participants-section">
        <div class="participants-heading-row">
          <p class="participants-title">Participants</p>
          <span class="participants-count">${details.participants.length}</span>
        </div>
        <ul class="participants-list">
          ${participantsMarkup}
        </ul>
      </div>
    `;

    // Add delete button event listeners
    const deleteButtons = activityCard.querySelectorAll(".delete-btn");
    deleteButtons.forEach((btn) => {
      btn.addEventListener("click", async (event) => {
        event.preventDefault();
        const activity = btn.dataset.activity;
        const email = btn.dataset.email;
        await unregisterParticipant(activity, email);
      });
    });

    return activityCard;
  }

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities");
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        activitiesList.appendChild(renderActivityCard(name, details));

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
        }
      );

      const result = await response.json();

      if (response.ok) {
        signupForm.reset();
        await fetchActivities();
        messageDiv.textContent = result.message;
        messageDiv.className = "message success";
      } else {
        messageDiv.textContent = result.detail || "An error occurred";
        messageDiv.className = "message error";
      }

      messageDiv.classList.remove("hidden");

      // Hide message after 5 seconds
      setTimeout(() => {
        messageDiv.classList.add("hidden");
      }, 5000);
    } catch (error) {
      messageDiv.textContent = "Failed to sign up. Please try again.";
      messageDiv.className = "message error";
      messageDiv.classList.remove("hidden");
      console.error("Error signing up:", error);
    }
  });

  // Function to unregister a participant
  async function unregisterParticipant(activity, email) {
    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
        }
      );

      if (response.ok) {
        messageDiv.textContent = `Removed ${email} from ${activity}`;
        messageDiv.className = "message success";
        messageDiv.classList.remove("hidden");
        await fetchActivities();
        setTimeout(() => {
          messageDiv.classList.add("hidden");
        }, 5000);
      } else {
        const result = await response.json();
        messageDiv.textContent = result.detail || "Failed to remove participant";
        messageDiv.className = "message error";
        messageDiv.classList.remove("hidden");
      }
    } catch (error) {
      messageDiv.textContent = "Failed to remove participant. Please try again.";
      messageDiv.className = "message error";
      messageDiv.classList.remove("hidden");
      console.error("Error unregistering participant:", error);
    }
  }

  // Initialize app
  fetchActivities();
});
