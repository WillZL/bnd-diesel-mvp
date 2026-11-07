"use strict";

// Menu responsivo: o botão controla a navegação lateral em telas pequenas.
const menuToggle = document.getElementById("menu-toggle");
const sidebar = document.getElementById("sidebar");
if (menuToggle && sidebar) {
  menuToggle.addEventListener("click", () => {
    const isOpen = sidebar.classList.toggle("open");
    menuToggle.setAttribute("aria-expanded", String(isOpen));
  });
  document.addEventListener("click", (event) => {
    if (window.innerWidth <= 720 && sidebar.classList.contains("open") &&
        !sidebar.contains(event.target) && !menuToggle.contains(event.target)) {
      sidebar.classList.remove("open");
      menuToggle.setAttribute("aria-expanded", "false");
    }
  });
}

// Adiciona itens ao formset Django sem alterar o prefixo de segurança/validação.
const addItemButton = document.getElementById("add-item");
const itemContainer = document.getElementById("item-formset");
const emptyItemTemplate = document.getElementById("empty-item-form");
const totalForms = document.getElementById("id_itens-TOTAL_FORMS");

if (addItemButton && itemContainer && emptyItemTemplate && totalForms) {
  addItemButton.addEventListener("click", () => {
    const index = Number.parseInt(totalForms.value, 10);
    const html = emptyItemTemplate.innerHTML.replaceAll("__prefix__", String(index));
    itemContainer.insertAdjacentHTML("beforeend", html);
    totalForms.value = String(index + 1);
    const newSelect = itemContainer.lastElementChild?.querySelector("select");
    if (newSelect) newSelect.focus();
  });

  itemContainer.addEventListener("click", (event) => {
    const removeButton = event.target.closest(".remove-item");
    if (!removeButton) return;
    const row = removeButton.closest(".item-row");
    const deleteField = row.querySelector('input[name$="-DELETE"]');
    if (!deleteField) return;
    deleteField.checked = true;
    row.hidden = true;
    const nextSelect = itemContainer.querySelector('.item-row:not([hidden]) select');
    nextSelect?.focus();
  });
}
