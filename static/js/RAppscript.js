const mealsEl = document.getElementById('meals');
const favoriteContainer = document.getElementById('fav-meals')

const searchTerm = document.getElementById('search-term');
const searchBtn = document.getElementById('search');

const mealPopup = document.getElementById('meal-popup');
const mealInfoEl = document.getElementById('meal-info');
const popupCloseBtn = document.getElementById('close-popup');

const tempFavs = ["52837", "52889", "52864", "52897", "52956"]

localStorage.setItem('mealIds', JSON.stringify(tempFavs) )

getRandomMeal();

fetchFavorites()

async function getRandomMeal() {

    const resp = await (await fetch('https://www.themealdb.com/api/json/v1/1/random.php')).json();
    const randomMeal = await resp.meals[0];

    displayMeal(randomMeal, true);
}

async function getMealById(id) {
    const resp = await (await fetch('https://www.themealdb.com/api/json/v1/1/lookup.php?i=' + id)).json();
    const meal = resp.meals[0];
    console.log(meal)
    return meal;

}

async function getMealBySearch(term) {
    const resp = await (await fetch('https://www.themealdb.com/api/json/v1/1/search.php?s=' + term)).json();

    const meals = resp.meals;

    return meals;
}

function displayMeal(mealData, random = false) {
    const meal = document.createElement('div');
    meal.classList.add('meal');

    meal.innerHTML =
        `
   
                <div class="meal">

                <div class="meal-header">
                    ${ random ? `<span class="random">
                    Something to try
                    </span>`: ' ' }

                    
                    <img src="${mealData.strMealThumb}"
                        alt="${mealData.strMeal}" />
                </div>
                <div class="meal-body">
                    <h4>${mealData.strMeal}</h4>
                    <button class="fav-btn">
                        <i class="fa fa-heart"></i>
                    </button>
                </div>
                </div>
        `;
        const btn = meal.querySelector(".meal-body .fav-btn");
        btn.addEventListener("click", () => {
            if(btn.classList.contains('active')){
                removeFromFavoritesLS(mealData.idMeal)
                btn.classList.remove("active");
            }else {
                addToFavoritesLS(mealData.idMeal)
                btn.classList.toggle("active");
            }
            
            fetchFavorites();
            });

            meal.addEventListener('click', () => {
                showMealInfo(mealData);
            })
        mealsEl.appendChild(meal);
}



function addToFavoritesLS(mealId) {
    const mealIds = getFavoritesFromLS();

    localStorage.setItem('mealIds', JSON.stringify([...mealIds, mealId]));
}

function removeFromFavoritesLS(mealId) {
    const mealIds = getFavoritesFromLS();

    localStorage.setItem('mealIds', JSON.stringify(
        mealIds.filter(id => id !== mealId)
    ));
}

function getFavoritesFromLS() {
    const mealIds = JSON.parse(localStorage.getItem('mealIds'));

    return mealIds === null ? [] : mealIds;
}

async function fetchFavorites(){
    favoriteContainer.innerHTML = "";

    const mealIds = getFavoritesFromLS();

    for(let i=0; i<mealIds.length; i++){
        const mealId = mealIds[i];

        meal = await getMealById(mealId);

       displayMealtoFavBar(meal);
    }

}

function showMealInfo(mealData) {
   //clear content
   mealInfoEl.innerHTML = '';

    //update meal info 
   const mealEl = document.createElement('div');

   const ingredients = [];
   //get ingredients and measures
   for (let i = 1; i <= 20; i++) {
    if (mealData["strIngredient" + i]) {
        ingredients.push(
            `${mealData["strIngredient" + i]} 
            
            - ${
                mealData["strMeasure" + i]
            }`
        );
    } else {
        break;
    }
}

    //display Data
    mealEl.innerHTML = 
    `
        <h1>${mealData.strMeal}</h1>
        <img src=${mealData.strMealThumb} alt="${mealData.strMeal}"/>
            <p>
                ${mealData.strInstructions}
            </p>
            <h3> Ingredients </h3>
            <ul>
                ${ingredients.map(
                    (ing) => `
                    <li>${ing}</li>
                `).join("")}
            </ul>
    `;

    mealInfoEl.appendChild(mealEl);
    
    mealPopup.classList.remove('hidden');
}

function displayMealtoFavBar(mealData) {

    const favMeals = document.createElement('li');
    favMeals.id = 'mealItem';
    favMeals.className = 'item';

    favMeals.innerHTML =
        `
            <img src="${mealData.strMealThumb}" 
            alt="${mealData.strMeal}">
            <span>${mealData.strMeal}</span>     
            <button class="clear">
                <i class="far fa-times-circle"></i>
            </button>   
        `;
        
        const btn = favMeals.querySelector('.clear');

        btn.addEventListener('click', () => {
            removeFromFavoritesLS(mealData.idMeal)
            fetchFavorites();
        });

        favMeals.addEventListener('click', () => {
            showMealInfo(mealData);
        })
    favoriteContainer.appendChild(favMeals);
}

searchBtn.addEventListener("click", async () => {
    //clear container
    mealsEl.innerHTML = '';

    const search = searchTerm.value;
    
    const meals = await getMealBySearch(search);
    
    if(meals){
        meals.forEach((meal) => {
            displayMeal(meal);
        })
    }
});

popupCloseBtn.addEventListener("click", () => {
    mealPopup.classList.add("hidden");
})