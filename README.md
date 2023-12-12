# **Site Title**
## **Site Overview**
This is where you give a brief overview of the page so, like an intro to the business or project followed by a brief talk about who the page is targeted at for example for a retro gaming arcade.
​
Retro arcade is a local business in the Sheffield area looking to offer young people a place to come and hangout and play old school games in a relaxed and friendly environment. Due to lower turnout than expected they have asked for a page to be built to spread the word in the community and wider areas. Ideally the business is intended to target younger gamers primarily but also be appealing to older people interested in a gaming experience 
​
![Am I responsive screenshot](imagelocation so maybe docs/image.jpg)
​
## Table of contents:
1. [**Site Overview**](#site-overview)
1. [**Planning stage**](#planning-stage)
    * [*Target Audiences*](#target-audiences)
    * [*User Stories*](#user-stories)
    * [*Site Aims*](#site-aims)
    * [*Wireframes*](#wireframes)
    * [*Color Scheme*](#color-scheme)
    * [*Typography*](#typography)
    * [*Database Models*](#database-models)
1. [**Current Features**](#current-features)
    * [*Common on all pages*](#common-on-all-pages)
    * [*The rest of your features*](#features)
1. [**Future-Enhancements**](#future-enhancements)
1. [**Testing Phase**](#testing-phase)
1. [**Deployment**](#deployment)
1. [**Tech**](#tech)
1. [**Credits**](#credits)
    * [*Honorable mentions*](#honorable-mentions)
    * [*General reference*](#general-reference)
    * [*Content*](#content)
    * [*Media*](#media)
​
## **Planning stage**
### **Target Audiences:**
* Users who have a passion for Pokemon, e.g. Pokemon enthusiasts and collectors. 
* Users interested in engaging with Pokemon-related content in a gamified environment.
* Users who enjoy customization and creativity, looking to design and curate their own unique Pokemondexes. 
* Users are interested in the diverse world of Pokemon, including aspects of biology, strategy, and statistics in an entertaining way.
​
### **User Stories:**
* As a user, I want to create and login to my account.
* As a user, I want to be able to create my own pokedexes and choose their colours.
* As a user, I want to be able to choose pokemons from different generations.
* As a user, I want to get some basic information about my chosen pokemons.

### **Site Aims:**
* To provide a fun, engaging and interactive online game. 
* To be a go-to resource for Pokemon gamers.
* To provide a comprehensive Pokemon database.
* To offer an user-friendly environment with a variety of options to keep the user entertained.
​
​
### **Wireframes:**
#### *Desktop*
​![Wireframes desktop](docs/wireframes/wireframes-desktop.webp)

#### *Tablet*
​![Tablet home](docs/wireframes/wireframes-tablet.webp)

#### *Mobile*
​![Mobile home](docs/wireframes/wireframes-mobile.webp)
​
### **Color Scheme:**
​The color palette chosen for this Pokedex-themed website is not only visually striking but also strategically designed to enhance user experience and engagement. Each color has been selected for its psychological impact and functional purpose, ensuring that the website is not only delightful to interact with but also accessible and user-friendly.

![Color palette](docs/images/color-palette.webp)

#### *Color palette*
* **Tomato Red (#FF6347)**: A vibrant and energetic red, perfect for capturing attention and evoking excitement.
    * Primary usage: Link hover color, requirement astrix and alerts.

* **Gold (#FFD700)**: A bright and playful gold, adding a sense of fun and creativity.
    * Usage: Form buttons. 

* **Lime Green (#32CD32)**: A fresh and lively green, conveying growth and energy.
    * Primary usage: Primary buttons and links. 

* **Deep Sky Blue (#00BFFF)**: A clear and engaging blue, offering a sense of trust and reliability.
    * Primary usage: H1, header (gradient with Medium Orchid).

* **Medium Orchid (#BA55D3)**: A playful and imaginative purple, adding a touch of whimsy and innovation.
    * Primary usage: H2-H6, header (gradient with Deep sky blue).

* **Dark Grey (#171717)**: This dark gray offers a sleek and modern backdrop, ideal for highlighting brighter colors. Its deep tone creates a sophisticated and elegant atmosphere, enhancing the overall visual appeal of the website. 
    * Primary usage: Main background.

* **Crisp white (#FFFFFF)**: A classic and clear choice for text, offering the highest level of readability. Its purity and brightness make it an excellent choice against darker backgrounds, ensuring that text is easily legible. 
    * Primary usage: Main body text. 

![Eight shapes - Contrast grid](docs/screenshots/contrast-grid.webp)

Together, these colors create a visually appealing interface that prioritizes user experience. The palette is designed to be delightful to interact with while being easy on the eyes. All color combinations are tested with WebAIM AAA standards to ensure accessibility, making the website not only aesthetically pleasing but also inclusive and user-friendly. This thoughtful approach to color usage ensures that the website is engaging, functional, and accessible to a wide range of users.

​
### **Typography**
![Typography](docs/images/typography.webp)

In our quest to create a space that’s as engaging and fun as it is visually appealing, we’ve carefully selected the fonts we think is the perfect fit for our brand:

#### *[Poppins](https://fonts.google.com/specimen/Poppins?query=poppins) for headings*:
* **Why:** We chose Poppins for its geometric charm and playful roundness, reflecting our commitment to a modern and friendly interface. Its semi-bold and bold styles are perfect for making our headings stand out, just like the colorful characters in our Pokedex!
* **How we use it:** Expect to see Poppins in our main titles (H1-H2) in uppercase, bringing a dynamic and energetic vibe to our platform. For subheadings (H3-H6), we mix it up with both uppercase and lowercase to keep things fresh and engaging.

#### *[Open Sans](https://fonts.google.com/specimen/Open+Sans?query=open+sans) for body text and buttons:*
* **Why:** Open Sans is the unsung hero of our text. Its clean and legible style ensures that you can dive into detailed Pokedex entries without straining your eyes. It’s the perfect complement to Poppins, maintaining balance and readability.
* **How we use it:** 
Open Sans in regular adorns our body text, input forms and button labels. We stick to standard cases for clarity in our descriptions and go for uppercase on buttons to draw your attention to the most interactive elements.

* All fonts were sourced from Google fonts, as stated in the credits.

### **Database**
Pokedex Genius uses a relational database model which includes three tables: user, pokedex, userpokemon, each described below. The database model is thoughtfully designed to support the applications core functionalites; User management, Pokedex creation and tracking user-Pokemon relationships. By integrating an external API for Pokemon data provides depth and timeliness to the application without overburdening the local database.

#### *The design explained*
* Each table serves a clear purpose making the database easy to understand and maintain.
* We use appropriate data types and unique constraints enhance performance and ensure data integrity.
* BIGINT are used for IDs allowing a large number of records, which is crucial for a growing application.
* Our structure supports a flexible and rich user experience where users can manage multiple Pokemondexes and Pokemons.

![Database diagram](docs/screenshots/database-diagram.webp)

#### *Data tables explained*
* **User table:** Stores essential user information. 
Manages user authentication and profile information. Username and email are unique for individual identification and login purposes.

* **Pokedex table:** Represents a collection of Pokemon for each user. 
Allows the user to create multiple, uniquely named Pokedexes and choose a color for each. 
Userid is used as a foreign key linking to the user table.  

* **Userpokemon table:** Manage the relationship between users and their Pokemon.
Tracks  which Pokemon are added to each Pokedex and by which user.
UserID and PokemonID may form a composite key if a Pokemon can only appear once per
User.

#### *Relationships explained*
* **User → Pokedex:** One-to-Many relationship. A user can have multiple Pokedexes but each Pokedex is associated with only one user. 
* **Pokedex → Userpokemon:** One-to-Many relationship. A Pokedex can contain many userpokemon, linking the selected Pokemon to the Pokedex.


#### *Usage of API*
We have chosen to use PokeAPI to fetch dynamic comprehensive data about Pokemons without storing all of the Pokemon data locally.The application can retrieve detailed information on-demand from the API when needed. 

**Benefits of using PokeAPI:** 
* By not storing all Pokemon details, instead include fields to store identifiers/keys that reference data in the API we can ensure the database will be kept lean and manageable. 
* As the user base grows the API can handle the load of fetching POkemon data, reducing the strain on the local database.
* Helps us ensure that the Pokemon data provided is fresh, since the application always has access to the most current data without needing local updates. 
* Let us focus on user-related data management while leveraging a pool of data from the API for everything Pokemon related. 


​
## **Current Features**

### **Common on all pages**

#### *Navigation Bar*
* 
​
### **Features**

#### *Creating account*
* 

#### *Login/logout*
* The users can easily login to their account.

#### *Dashboard page*
* Gives the user an overall created Pokedexes.

#### *Account page*
* The user can easily change their account information.
* The user can add an avatar image.
* The user can add their pokemon trainer id.

#### *Creating Pokedex*
* User adds a name, description (optional) and chooses the colour of the Pokedex.
* 

​
## **Future-Enhancements**
​
* Build more of a community where users can interact and engage with each other and see their profiles. 
* Let users vote on and save other users' Pokemondexes. 
* Display a scoreboard of the best ranked (the one with most votes during a specific time range) Pokemondexes.

​
## **Testing Phase**
​
This is the hardest bit of the readme, when we have completed a page we need to discuss testing.
​
Here is a good idea to talk about how and why you have tested with certain tools and validators so here a list of things to talk through
​
* Responsiveness - How do you test this, dev tools? checking on multiple devices?
​
* Functionality - Each feature needs to be tested before something is complete, talk about the process, click each link check each image, does form validation work, if your using javascript or anything else, does it always behave as the user expects
​
* Validators - Here include images from w3c html validator and css jigsaw (jshint for js and pep8 for python) and the results that came from it
​
​
## **Bugs**
​
We always have bugs in development, a few bullet points here to talk about bugs you found and how you fixed them, in later projects this will be more detailed
​
* Issue - When the user filled the login form with invalid information, the form clears.
* Cause - The images had absolute positioning and caused them to go off screen
* Resolution - Changed the width of the image to stay within the confines of the screen.
​
***
## **Deployment**
I deployed the page on GitHub pages via the following procedure: -
​
1. From the project's [repository](pageurl), go to the **Settings** tab.
2. From the left-hand menu, select the **Pages** tab.
3. Under the **Source** section, select the **Main** branch from the drop-down menu and click **Save**.
4. A message will be displayed to indicate a successful deployment to GitHub pages and provide the live link.
​
You  can find the live site via the following URL - [live webpage](https://yoururlhere)
***
​
## **Tech**
- HTML
- CSS
​
## **Credits**
### **Honorable mentions**
​
It's always nice to mention those that helped you get there, if people gave you support on slack or the local cat scared you into completing give them a mention!
​
### **Content:**
​* Poppins and Open Sans fonts from [Google Fonts](https://fonts.google.com/specimen/Open+Sans?query=open+sans) 
  
### **Media:**
* Logotype, colour palette, typography are created by myself using [Adobe Illustrator](https://www.adobe.com/se/products/illustrator)​
* Wireframes are created by myself using [Adobe XD](https://helpx.adobe.com/se/xd/get-started.html)​
* Icons from [Font Awesome](https://fontawesome.com/)
* Images compressed with [TinyPNG](https://tinypng.com/)
