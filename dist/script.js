const previewImage = document.querySelector("#workbook-preview-image");
const previewTitle = document.querySelector("#preview-title");
const previewTabs = document.querySelectorAll(".preview-tab");

previewTabs.forEach((tab) => {
  tab.addEventListener("click", () => {
    previewTabs.forEach((item) => item.classList.remove("active"));
    tab.classList.add("active");
    previewImage.src = tab.dataset.src;
    previewImage.alt = tab.dataset.alt;
    previewTitle.textContent = tab.dataset.title;
  });
});
