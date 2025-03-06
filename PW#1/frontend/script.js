function updateValues() {
    const data = {
        id: document.getElementById('meterId').value,
        day: document.getElementById('day').value,
        night: document.getElementById('night').value
    };

    fetch('http://localhost:8080/meters/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
}

function toggleHistory() {
    let modal = document.getElementById("modalContent");
    modal.style.display = (modal.style.display === "flex") ? "none" : "flex";
}

function addHistoryRecord(record) {
    let historyList = document.getElementById("historyList");
    let listItem = document.createElement("li");
    
    listItem.innerHTML = `
        <strong>Meter ID:</strong> ${record.meterId} 
        <strong>Date:</strong> ${record.date} 
        <strong>Day:</strong> ${record.day} 
        <strong>Night:</strong> ${record.night} 
        <strong>Charge:</strong> ${record.charge}
    `;
    historyList.appendChild(listItem);
}

async function fetchHistory() {
    try {
        const response = await fetch("http://localhost:8080/history/");
        if (response.ok) {
            const historyList = await response.json();
            document.getElementById("historyList").innerHTML = "";
            historyList.reverse().forEach(record => addHistoryRecord(record));
        }
    } catch (error) {
        console.error('Error fetching history:', error);
    }
}

function addMeterRecord(record) {
    let metertList = document.getElementById("metertList");
    let listItem = document.createElement("li");

    listItem.innerHTML = `
        <strong>Meter ID:</strong> ${record.id}<br>
        <strong>Day:</strong> ${record.day}
        <strong>Night:</strong> ${record.night}<br>
        <strong>Last charge:</strong> ${record.lastCharge}
    `;
    metertList.appendChild(listItem);
}

async function fetchMeters() {
    try {
        const response = await fetch("http://localhost:8080/meters/");
        if (response.ok) {
            const metersList = await response.json();
            document.getElementById("metertList").innerHTML = "";
            metersList.reverse().forEach(record => addMeterRecord(record));
        }
    } catch (error) {
        console.error('Error fetching meters:', error);
    }
}

async function fetchPunishmetsAndTariffs() {
    try {
        const tariffsResponse = await fetch("http://localhost:8080/tariffs/");
        const punishmentsResponse = await fetch("http://localhost:8080/punishments/");
        if (tariffsResponse.ok && punishmentsResponse.ok) {
            const tariffs = await tariffsResponse.json();
            const punishments = await punishmentsResponse.json();
            document.getElementById("massage").innerHTML = `
                <h3>Тарифи: day ${tariffs.dayTariff} - night ${tariffs.nightTariff}</h3>
                <p>Не накручуйте показники, за це передбаченно штрафи!</p>
                <p>Штрафи: day ${punishments.dayPunishment} - night ${punishments.nightPunishment}</p>
            `;
        }
    } catch (error) {
        console.error('Error fetching PunishmetsAndTariffs:', error);
    }
}

document.addEventListener("DOMContentLoaded", function() {
    fetchPunishmetsAndTariffs();
    fetchHistory();
    fetchMeters();
    setInterval(fetchMeters, 1000)
    setInterval(function() {
        const modal = document.getElementById("modalContent");
        if (modal.style.display === "flex") {
            fetchHistory();
        }
    }, 1000);
});
