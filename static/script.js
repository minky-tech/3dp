
async function loadGcodeFiles() {
    const response = await fetch("/api/gcodes");
    const files = await response.json();

    const table = document.getElementById("file-list");
    table.innerHTML = ""; // Clear existing content

    const tableTitle = document.createElement('div');
    tableTitle.className = 'table header';
    tableTitle.textContent = 'Print Queue';
    table.appendChild(tableTitle);

    const tableHeader = document.createElement('div');
    tableHeader.className = 'row header';
    tableHeader.innerHTML = `
        <div class="cell">Name</div>
        <div class="cell">Filament</div>
        <div class="cell">Weight</div>
        <div class="cell">Length</div>
        <div class="cell">Time</div>
    `;
    table.appendChild(tableHeader);

    files.forEach(file => {

        const row = document.createElement('div');
        row.className = 'row';

        const nameCell = document.createElement('div');
        nameCell.className = 'cell';
        nameCell.innerHTML = file.name;

        const filamentCell = document.createElement('div');
        filamentCell.className = 'cell';
        filamentCell.textContent = file.filament_type;

        const weightCell = document.createElement('div');
        weightCell.className = 'cell';
        weightCell.innerHTML = file.filament_weight;

        const lengthCell = document.createElement('div');
        lengthCell.className = 'cell';
        lengthCell.innerHTML = file.filament_length;

        const timeCell = document.createElement('div');
        timeCell.className = 'cell';
        timeCell.innerHTML = file.print_time;

        row.appendChild(nameCell);
        row.appendChild(filamentCell);
        row.appendChild(weightCell);
        row.appendChild(lengthCell);
        row.appendChild(timeCell);
        
        table.appendChild(row);


        //listItem.innerHTML = `
        //    <strong>${file.name}</strong> - ${file.size} bytes
        //    <a href="${file.path}" download>Download</a>
        //`;
        //fileList.appendChild(listItem);

    });
}

// Load G-code files on page load
window.onload = loadGcodeFiles;

/*
fetch("/api/wishlist")
    .then(response => response.json())
    .then(data => {
        const table = document.querySelector('.table');

        data.forEach(entry => {
            const row = document.createElement('div');
            row.className = 'row';

            const itemCell = document.createElement('div');
            itemCell.className = 'cell';
            itemCell.innerHTML = entry.item;

            const categoryCell = document.createElement('div');
            categoryCell.className = 'cell';
            categoryCell.textContent = entry.category;

            const costCell = document.createElement('div');
            costCell.className = 'cell';
            costCell.innerHTML = entry.cost;

            const notesCell = document.createElement('div');
            notesCell.className = 'cell';
            notesCell.innerHTML = entry.notes;

            row.appendChild(itemCell);
            row.appendChild(categoryCell);
            row.appendChild(costCell);
            row.appendChild(notesCell);
            
            table.appendChild(row);
        });
    })
    .catch(error => console.error("Error fetching wish list data:", error));
*/
