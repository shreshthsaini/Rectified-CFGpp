const placesData = {
    "babylon.png": "Tower of Babel",
    "sf.png": "Golden Gate Bridge,<br>San Francisco",
    "stonehenge.png": "Stonehenge",
    "sydney.png": "Sydney Opera",
    "fiorence.png": "Cathedral of Santa Maria<br>del Fiore",
    "prague.png": "Prague",
    "rio.png": "Rio de Janeiro",
    "rome.png": "Colosseum",
    "seatle.png": "Space Needle,<br>Seattle",
    "taj.png": "Taj Mahal",
    "fuji.png": "Mount Fuji",
    "giza.png": "Great Pyramid of Giza",
    "grand_canion.png": "Grand Canyon",
    "beij.png": "Forbidden City,<br>Beijing",
    "ironer.png": "Flatiron Building,<br>New York",
    "jerusalem.png": "Jerusalem",
    "liberty.png": "Statue of Liberty",
    "louvre.png": "Louvre Museum,<br>Paris",
    "machu.png": "Machu Picchu, Peru",
    "grif.png": "Griffith Observatory,<br>Los Angeles",
    "matterhorn.png": "Matterhorn, Swiss Alps",
    "golden.png": "Golden Temple, Kyoto",
    "moon.png": "The Moon",
    "niagara.png": "Niagara Falls",
    "nss.png": "Neuschwanstein Castle,<br>Bavaria",
    "ny.png": "Empire State Building,<br>New York",
    "paris.png": "Eiffel Tower",
    "patagonia.png": "Perito Moreno Glacier,<br>Patagonia",
    "ams.png": "Amsterdam",
    "aurora.png": "Aurora, Norway Fjords",
    "barcelone.png": "La Sagrada Familia,<br>Barcelona",
    "berlin.png": "Alexanderplatz, Berlin",
    "budapest.png": "Parliament, Budapest",
    "burj.png": "Burj Khalifa, Dubai",
    "dracula.png": "Bran Castle<br>(Dracula's Castle),<br>Romania",
    "easter.png": "Easter Island",
    "titanic.png": "Titanic",
    "venice.png": "San Marco, Venice",
    "wall.png": "Great Wall of China",
    "zurich.png": "Zurich"
};

document.addEventListener('DOMContentLoaded', function() {
    const gridContainer = document.getElementById('grid-container');

    Object.entries(placesData).forEach(([src, description]) => {
        const card = document.createElement('div');
        card.className = 'card';

        card.innerHTML = `
            <div class="card-inner">
                <div class="card-front">
                    <img src="./data/places/${src}" alt="Image">
                </div>
                <div class="card-back">
                    <p>${description}</p>
                </div>
            </div>
        `;

        card.addEventListener('click', function() {
            card.classList.toggle('flipped');
            setTimeout(function() {
                card.classList.remove('flipped');
            }, 2500);
        });

        gridContainer.appendChild(card);
    });
});
