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

// Formata telefones brasileiros no cadastro/edição de clientes.
// Aceita números nacionais com DDD (10 ou 11 dígitos) e prefixo opcional +55.
const phoneInput = document.querySelector('[data-phone-mask="br"]');

if (phoneInput) {
  const formatBrazilianPhone = (value) => {
    let digits = value.replace(/\D/g, "");

    // Remove o código do país quando informado antes do DDD.
    if ((digits.length === 12 || digits.length === 13) && digits.startsWith("55")) {
      digits = digits.slice(2);
    }

    digits = digits.slice(0, 11);
    if (!digits) return "";

    if (digits.length <= 2) return `(${digits}`;

    const areaCode = digits.slice(0, 2);
    const subscriber = digits.slice(2);

    if (digits.length <= 6) return `(${areaCode}) ${subscriber}`;
    if (digits.length <= 10) {
      return `(${areaCode}) ${subscriber.slice(0, 4)}-${subscriber.slice(4)}`;
    }

    return `(${areaCode}) ${subscriber.slice(0, 5)}-${subscriber.slice(5)}`;
  };

  const applyPhoneMask = () => {
    const cursor = phoneInput.selectionStart;
    const digitsBeforeCursor = phoneInput.value
      .slice(0, cursor === null ? phoneInput.value.length : cursor)
      .replace(/\D/g, "").length;

    const formattedValue = formatBrazilianPhone(phoneInput.value);
    phoneInput.value = formattedValue;

    // Preserva a posição aproximada do cursor durante a digitação/edição.
    if (cursor !== null && document.activeElement === phoneInput) {
      let newCursor = 0;
      let digitsSeen = 0;

      while (newCursor < formattedValue.length && digitsSeen < digitsBeforeCursor) {
        if (/\d/.test(formattedValue[newCursor])) digitsSeen += 1;
        newCursor += 1;
      }

      phoneInput.setSelectionRange(newCursor, newCursor);
    }
  };

  phoneInput.addEventListener("input", applyPhoneMask);

  // Também padroniza valores já existentes ao abrir a tela de edição.
  if (phoneInput.value) {
    phoneInput.value = formatBrazilianPhone(phoneInput.value);
  }
}

