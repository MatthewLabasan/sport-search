COMS 4111 Project 1 Part 3
Sports Review Application


The PostgreSQL account name: bl3092

The URL of our web application: http://34.73.35.75:8111/ 

Description

The functionalities we implemented that follows our original proposal:

User Registration: Users are able to register and create new accounts, and log into their account based on their unique usernames.
Sports Search and Filtering: Users are able to search for sports by category, location, difficulty, prices, and ratings. We implemented the ability to search sports using filters like sport type, difficulty, rating, and price, and we also added the ability to filter based on proximity to the user's location.
Review and Likes Functionality: Users are able to leave reviews after completing an activity. They can like other users' reviews, which adds to the like count of each review.
Sport Status: Users can save a sport or mark it as completed after participating in it. The status is recorded in the "Status" table, allowing users to interact with different sports by saving or completing them.
Number of People Completed: After completing a sport, the "num_people_completed" attribute in the Sports entity is incremented accordingly.
Adding New Sports: Users can add new activity locations to the database, which makes the system more diverse and comprehensive. This was part of the original proposal and was successfully implemented.

The functionalities that we did not implement from our original proposal:

Recommendation Algorithm: Our original proposal mentioned recommending certain activities based on users' sports interests and the ratings given by similar users. This feature was not implemented in this iteration due to time constraints. Instead, we recommend users with all that are in their state (depending on location, this may  be equivalent to country) to simplify things.
Sorting of Results: Our original proposal stated that we would showcase filtered results by distance, with the first result being the sport closest to the user. However, this proved difficult as we were working with coordinates. Instead we could have sorted by the same state / then alphabetically outside states, though we ran out of time.

New features we implemented:

Interactive buttons (Save, Complete, Like). We added these buttons that change dynamically upon user action. This involves a lot of querying and filtering. For example, when a user is searching for sports and marks an interesting sport as "saved" by clicking the 'save' button below that sport, the button will then disappear and turn into an unclickable text saying "Saved". At the same time, the saved sport will appear in the saved_sport page.
Data Validation and Error Handling: We included more robust error handling, such as:
Checks to ensure users cannot save the same sport multiple times
Prevent user to register with an existing username
Ensure a user cannot like a review more than once

Two interesting web pages:

1. Find Sport Page

This page allows users to search for sports based on several criteria, including sport type, difficulty, rating, city, and price.

When a user enters their search criteria, multiple filters are applied through SQL queries. The query checks sport type, difficulty, rating, and price to provide a personalized list of sports that match the user's input.
After users specify their search criteria, an SQL query is generated to filter sports based on sport type, difficulty, rating, price, and proximity to the user.
The page retrieves and displays each sport's Trail Name, Sport Type, Difficulty, Rating, Price, and Number of People Completed.
Each sport item has an interactive "Save" button at the bottom, which allows users to save that sport if they are interested. However, the "Save" button is only displayed for sports that have neither been saved nor completed by the user.
If a sport has been saved, the page displays a blue "Saved" label instead of a button, and if a sport has been completed, it displays a green "Completed" label.
When users click the "Save" button, a new entry is created in the "Status" table with the user's information and the status set to "saved." This prevents them from saving the same sport multiple times.
At the end of the page, there is an additional section that allows users to add a new sport if they cannot find the sport they want. The user can fill in the forms by tying Trail name, Coordinates, selecting Sport Type and Difficulty, checking Equipment needed and finally click the “Add Sport” button. Given the input data, SQL will insert the new sport into the Sports table.

The interesting aspect of this page is that it utilizes different filtering methods to not only help users find sports but also interact (i.e. save) with the sport. The user can find their targeted sports through various filters like sport type, city, price, rating, etc, which provides a lot of flexibility. With these various filters, the query can become very complex, and we used a lot of if-else statements to ensure that the correct query would be constructed. The search result also contains sports that have already been saved or completed by the user, which make the search results more personalized. Additionally, the page also adds a functionality that allows users to add a new sport in case they don’t find the sport they want. This function allows users to enrich the database and gradually provide a significant amount of Sports for users to choose. 


2. Sport Reviews Page

This page displays all reviews for a specific sport, the equipment needed for the sport with pricing, the user’s status on this sport, as well as other related trails. It also allows users to like a review.

When a user clicks the "like" button on a review, a new entry is added to the "Likes" table, and the "like_count" in the "Review" table is incremented.
This requires two database operations: an insert operation to track the user’s like action and an update to reflect the new like count in the "Review" table.
The page also ensures users cannot like the same review multiple times by checking if an entry for that user and review already exists in the "Likes" table before proceeding.
At the bottom of the page, some related trails are displayed with links redirected to the sport’s own review page. Users can click any one of those trails to find more details about the sport. 

The interesting aspect of this page is that the user can see others’ reviews of the sport and react (i.e. like) if they find it helpful. To do this, we needed to ensure that we were passing around the correct sport_id / sport data to the backend so that we could correctly match up the page’s specific sport and review with the user, and push this data to the ‘status’ table accordingly. This took a lot of data passing and handling, which is what made not only the query but the creation of the API interesting. Additionally, below the review section, it also recommends other similar sports to the user with links to their own review page using the same data. This gives users more diverse options and improves their sport search efficiency.


AI tools Usage

We used AI tools like ChatGPT to help set up basic routing in Flask, and understand how to handle HTTP methods like POST and GET. We also utilized ChatGPT to understand how some Javascript functions work, and assist us in setting up calls to our backend API. It was also used in guiding us through styling and HTML template setup. Another thing that ChatGPT helped us with is converting coordinates to location metadata, in which it gave some libraries we could use. We then used these libraries’ APIs to develop our logic.

