(function () {
  const STORAGE_KEY = "manipal_teaching_materials_access";
  const allowedDomains = window.TEACHING_MATERIALS_DOMAINS || ["manipal.edu"];

  function isAllowedManipalEmail(email) {
    const normalized = String(email || "")
      .trim()
      .toLowerCase();
    const parts = normalized.split("@");
    if (parts.length !== 2 || !parts[0] || !parts[1]) {
      return false;
    }

    const domain = parts[1];
    return allowedDomains.some(function (allowed) {
      return domain === allowed || domain.endsWith("." + allowed);
    });
  }

  function unlockMaterials(email) {
    sessionStorage.setItem(STORAGE_KEY, email);
    document.getElementById("teaching-materials-gate").hidden = true;
    document.getElementById("teaching-materials-content").hidden = false;
  }

  function initTeachingMaterialsGate() {
    const root = document.getElementById("teaching-materials");
    if (!root) {
      return;
    }

    const savedEmail = sessionStorage.getItem(STORAGE_KEY);
    if (savedEmail && isAllowedManipalEmail(savedEmail)) {
      unlockMaterials(savedEmail);
      return;
    }

    const form = document.getElementById("teaching-materials-form");
    const emailInput = document.getElementById("teaching-materials-email");
    const error = document.getElementById("teaching-materials-error");

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      const email = emailInput.value;

      if (!isAllowedManipalEmail(email)) {
        error.hidden = false;
        emailInput.focus();
        return;
      }

      error.hidden = true;
      unlockMaterials(email);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initTeachingMaterialsGate);
  } else {
    initTeachingMaterialsGate();
  }
})();
