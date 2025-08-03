const list = document.getElementById("note-list");
let draggingEle;
let order = [];

// Function to update numbering
function updateNumbers() {
    const items = list.querySelectorAll("li");
    items.forEach((li, index) => {
        li.querySelector(".note-number").textContent = index + 1;
    });
}

list.addEventListener("dragstart", (e) => {
    draggingEle = e.target;
    e.target.classList.add("dragging");
});

list.addEventListener("dragend", () => {
    draggingEle.classList.remove("dragging");

    // Update numbers in UI
    updateNumbers();

    // Save new order to backend
    order = Array.from(list.querySelectorAll("li")).map(li => li.dataset.id);
    fetch("/reorder", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(order)
    });
});

list.addEventListener("dragover", (e) => {
    e.preventDefault();
    const afterElement = getDragAfterElement(list, e.clientY);
    if (afterElement == null) {
        list.appendChild(draggingEle);
    } else {
        list.insertBefore(draggingEle, afterElement);
    }
});

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll("li:not(.dragging)")];
    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}

// Initial numbering on page load
updateNumbers();
