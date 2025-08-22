

// static/js/weather.js

const API_KEY = "f4132cab04b54ab49f7113608252805";
const weatherWidget = document.getElementById('weather-widget');

// Function to get user's location
function getUserLocation() {
    // Check if the browser supports geolocation
    if (navigator.geolocation) {
        // Request the current position
        navigator.geolocation.getCurrentPosition(position => {
            const lat = position.coords.latitude;
            const lon = position.coords.longitude;
            getWeatherData(lat, lon);
        }, error => {
            // Handle cases where geolocation is denied or fails
            console.error("Geolocation error:", error);
            weatherWidget.innerHTML = "<p>Please enable location services to get local weather.</p>";
            // Fallback to a default location if geolocation fails
            // You can choose a city relevant to your user base, e.g., New Delhi
            getWeatherData(28.6139, 77.2090); 
        });
    } else {
        // Handle cases where geolocation is not supported
        weatherWidget.innerHTML = "<p>Geolocation is not supported by this browser.</p>";
    }
}

// Function to fetch weather data from the WeatherAPI
function getWeatherData(lat, lon) {
    const url = `https://api.weatherapi.com/v1/current.json?key=${API_KEY}&q=${lat},${lon}`;
    
    fetch(url)
        .then(response => {
            if (!response.ok) {
                // Throw an error if the response is not successful
                throw new Error('Weather data not found');
            }
            return response.json();
        })
        .then(data => {
            displayWeatherData(data);
        })
        .catch(error => {
            console.error("Error fetching weather data:", error);
            weatherWidget.innerHTML = "<p>Failed to load weather data.</p>";
        });
}

// Function to display weather data in the HTML
function displayWeatherData(data) {
    const location = data.location.name;
    const temperatureC = data.current.temp_c;
    const condition = data.current.condition.text;
    const iconUrl = data.current.condition.icon;

    const weatherHtml = `
        <img src="${iconUrl}" alt="${condition}" class="weather-icon">
        <div class="weather-info">
            <span class="temperature">${temperatureC}°C</span>
            <span class="description">${condition} in ${location}</span>
        </div>
    `;
    weatherWidget.innerHTML = weatherHtml;
}

// Run the function when the page loads
document.addEventListener('DOMContentLoaded', getUserLocation);