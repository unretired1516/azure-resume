window.addEventListener('DOMContentLoaded', (event) => {
    getVisitCount();
});

const functionApiURL = 'https://getazureresumecounteruniqueidentifierhere.azurewebsites.net/api/VisitorCounter?code=wiNDrGe0UJcCdSuLC18Z90TqErEZVNVThmLsFedWnNK0AzFuWKh58A==';
const localfunctionApi = 'http://localhost:7071/api/VisitorCounter';

// Set variable to 0, call the API, get the current count, then set the count variable to equal the response.
const getVisitCount = async () => {
    try {
        const response = await fetch(functionApiURL);
        const data = await response.json();
        console.log("Website called function API.");
        // Update the count element on the webpage
        document.getElementById("counter").innerText = data.count;
    } catch (error) {
        console.error('Error fetching the visit count:', error);
        // Optionally handle error display here
    }
};