//Top level helper functions section
  //if you are reading this, this is learning project so ignore the odd names.
function fisherYatesShuffle(arr) {
    for(let i = arr.length -1; i > 0; i--){
        const j = Math.floor(Math.random() * (i +1));
        [arr[i], arr[j]] = [arr[j]], arr[i]];
    }
    return arr;
}
function applyTheme() {
    document.body.classList.toggle("dark-mode", theme === "dark");
}
    //TODO update this to change the CSS classes rather than the style
    //this was done this way because i wanted thought it looked cooler but upon further inspection this doesnt seem
    // - to be optimal
function initCollapsible() {
    document.querySelectorAll(".profile-section").forEach(section => {
        const header = section.querySelector("h3");
        const subsections = Array.from(section.children)
            .filter(node => node.tagName !== "H3");
        subsections.forEach(n => n.style.display = "none");
        header.style.cursor = "pointer";
        header.addEventListener("click", () => {
            const isHidden = subsections[0].style.display === "none";
            subsections.forEach(n => n.style.display = isHidden ? "" : "none");
        });
    });
}
function initRecs() {
    const recList = document.getElementById("recList");
    if (!recList) return;
    const defaultRecs = [
        { title: "All My Exes Live In Texas", artist: "George Strait" },
        { title: "El Diablo Anda Suelto", artist: "La Santa Grifa" },
        { title: "Beat Box", artist: "SpottemGottem" },
        { title: "полковнику никто не пишет", artist: "Би-2" },
        { title: "Давай За", artist: "любе" }
    ];
    const shuffled = fisherYatesShuffle(defaultRecs.slice());
    const selected = shuffled.slice(0,3);
    recList.innerHTML = "";
    selected.forEach(({title, artist}) => {
        const card = document.createElement("div");
        card.className = "recCard";
        card.innerHTML = `
            <h3>"${title}"</h3>
            <p>by ${artist}</p>
            <div class="buttons">
                <button>Like</button>
                <button>Dislike</button>
                <button>Known</button>
            </div>
            `;
            recList.appendChild(card)
    });
}
async function initProfile() {
    const profile = document.getElementById("profileContainer");
    if (!profile) return;
        const defaults = {
    userEmail:        "Douglas@email.com",
    userUsername:     "DouglasDig32",
    userFullName:     "Douglas Digs",
    userAge:          "—",
    userGender:       "Not set",
    userRace:         "Not specified",
    userEthnicity:    "Not specified",
    userLang:         "English",
    userDevice:       "Not specified",
    userAddLangs:     "None",
    userCountries:    "None selected",
    userPrefArtist:   "no preference",
    ratedArtistCount: "None Rated",
    userPrefGenre:    "None Rated",
    ratedSongCount:   "None Rated"
    }
    let savedData = {};
    try {
        const res = await fetch("TBD");
        if (res.ok) {
        savedData = await res.json();
    } else {
    console.warn("no res from database", res.status);
    console.log("Douglas is displeased");
    }
    } catch(e) {
    console.warn("could not load users profile data.", e);
    }
    const data = {...defaults,...savedData};
    Object.keys(defaults).forEach(key => {
        const element = document.getElementById(key);
            if (element) element.textContent = data[key];
    });
}
function initSettings() {
    const section = document.getElementById("userSettings");
    if (!section) return;
        const themeSelector = document.getElementById("themeSelector");
        const savedTheme = localStorage.getItem("theme") || "dark";
        themeSelector.value = savedTheme;
        applyTheme(savedTheme);
    themeSelector.addEventListener("change", (e) => {
    const val = e.target.value;
    if (val === "light"){
    alert("Wrong Choice lol");
    localStorage.setItem("theme", "dark");
    applyTheme("dark");
    } else {
    localStorage.setItem("theme", val);
    applyTheme(val);
    }
    });
    const filterButtons = section.querySelectorAll(".filterButtons button");
    const savedFilter = localStorage.getItem("contentFilter");
    filterButtons.forEach((button) => {
        if (button.id === savedFilter) button.classList.add("active");

        button.addEventListener("click", () => {
        filterButtons.forEach(b => b.classList.remove("active"));
        button.classList.add("active");
        localStorage.setItem("contentFilter", button.id);
        });
    });
}
document.addEventListener("DOMContentLoaded", () => {
    initRecs();
    initProfile();
    initSettings();
    initCollapsible();
});