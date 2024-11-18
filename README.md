**The PostgreSQL account name:** bl3092

**The URL of our web application:**

**A description of the parts of your original proposal in Part 1 that you implemented, the parts you did not (which hopefully is nothing or something very small), and possibly new features that were not included in the proposal and that you implemented anyway.** 

The functionalities we implementd that follows our original proposal:

1. Sports Search and Filtering: Users are able to search for sports by category, location, difficulty, prices, and ratings. We implemented the ability to search sports using filters like sport type, difficulty, rating, and price, and we also added the ability to filter based on proximity to the user's location.

2. Review and Likes Functionality: Users are able to leave reviews after completing an activity. They can like other users' reviews, which adds to the like count of each review.

3. Sport Status: Users can save a sport or mark it as completed after participating in it. The status is recorded in the "Status" table, allowing users to interact with different sports by saving or completing them.

4. Number of People Completed: After completing a sport, the "num_people_completed" attribute in the Sports entity is incremented accordingly.

5. Adding New Sports: Users can add new activity locations to the database, which makes the system more diverse and comprehensive. This was part of the original proposal and was successfully implemented.

6. Sorting by Distance: In our original proposal, we mentioned that we want to sort sports by distance from the user's location. We implemented a simple version which filter sports that are within +- 5 degree from user's location in terms of both latitude and longitude.


The functionalities that we did not implement from our original proposal:

1. Recommendation Algorithm: Our original proposal mentioned recommending certain activities based on users' sports interests and the ratings given by similar users. This feature was not implemented in this iteration due to time constraints.

New featrues we implemented:

1. Interactive buttons (Save, Complete, Like). We added these buttons that change dynamically upon user action. This involves a lot of querying and filtering. For example, when a user is searching sports and marks an interesting sport as "saved" by clicking the 'save' button below that sport, the button will then disappear and turns into an unclickable text saying "Saved". At the same time, the saved sport will appear in saved_sport page. 

2. Data Validation and Error Handling: We included more robust error handling, such as:
- Checks to ensure users cannot save the same sport multiple times
- Prevent user to register with an existing username
- Ensure a user cannot like a review more than once 


**Briefly describe two of the web pages that require (what you consider) the most interesting database operations in terms of what the pages are used for, how the page is related to the database operations (e.g., inputs on the page are used in such and such way to produce database operations that do such and such), and why you think they are interesting.**

1. Find Sport Page

- This page allows users to search for sports based on several criteria, including sport type, difficulty, rating, city, and price.

- When a user enters their search criteria, multiple filters are applied through SQL queries. The query checks sport type, difficulty, rating, and price to provide a personalized list of sports that match the user's input.

- After users specify their search criteria, an SQL query is generated to filter sports based on sport type, difficulty, rating, price, and proximity to the user.

- The page retrieves and displays each sport's Trail Name, Sport Type, Difficulty, Rating, Price, and Number of People Completed.

- Each sport item has an interactive "Save" button at the bottom, which allows users to save that sport if they are interested. However, the "Save" button is only displayed for sports that have neither been saved nor completed by the user.

- If a sport has been saved, the page displays a blue "Saved" label instead of a button, and if a sport has been completed, it displays a green "Completed" label.

- When users click the "Save" button, a new entry is created in the "Status" table with the user's information and the status set to "saved." This prevents them from saving the same sport multiple times.

The query leverages filtering by both numeric ranges (for latitude, longitude, and price) and string matching (for city and sport type).


Why interesting:



2. Sport Reviews Page

- This page displays all reviews for a specific sport and allows users to like a review.

- When a user clicks the "like" button on a review, a new entry is added to the "Likes" table, and the "like_count" in the "Review" table is incremented.

- This requires two database operations: an insert operation to track the user’s like action and an update to reflect the new like count in the "Review" table.

- The page also ensures users cannot like the same review multiple times by checking if an entry for that user and review already exists in the "Likes" table before proceeding.


Why Interesting:




**AI tools**