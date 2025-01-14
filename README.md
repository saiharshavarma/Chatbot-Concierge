# Chatbot Concierge for Restaurant Recommendations

---

## Project Overview

This project implements a chatbot concierge for restaurant recommendations, leveraging **AWS Lex**, **SQS**, **Lambda**, **DynamoDB**, **OpenSearch**, and **SES**. The chatbot allows users to request dining suggestions by specifying a cuisine, and it responds with tailored restaurant recommendations. The project is designed to be scalable, decoupled, and highly available.

---

## Architecture

1. **AWS Lex Chatbot**: Handles user interactions and collects preferences (e.g., cuisine, email).
2. **AWS SQS**: Stores dining requests for asynchronous processing.
3. **AWS Lambda Functions**:
   - **LF1**: Processes user input and pushes requests to SQS.
   - **LF2**: Acts as a queue worker to process SQS messages, fetch restaurant details from DynamoDB and OpenSearch, and send email recommendations via SES.
4. **DynamoDB**: Stores restaurant details such as name, address, coordinates, reviews, ratings, and zip codes.
5. **OpenSearch**: Stores partial restaurant data (RestaurantID and Cuisine) for fast querying.
6. **SES (Simple Email Service)**: Sends restaurant recommendations to users via email.

---

## Features

- **Restaurant Recommendations**:
  - User specifies a cuisine and email through the chatbot.
  - The system provides random restaurant suggestions based on the requested cuisine.
- **Data Storage**:

  - Full restaurant data in DynamoDB.
  - Fast cuisine-based search using OpenSearch.

- **Email Notifications**:

  - Restaurant details are sent to the user’s email.

- **User State Management**:
  - The system remembers the user's last search (cuisine) and automatically provides recommendations based on it when the user returns to the chat.

---

## How It Works

1. **Interaction with Lex Chatbot**:

   - The user interacts with the chatbot, specifying a cuisine and email address.

2. **Request Processing**:

   - The chatbot triggers LF1, which pushes the dining request to the SQS queue.
   - LF2 processes the request by:
     - Fetching restaurant details from DynamoDB and OpenSearch.
     - Sending an email with the restaurant recommendation.

3. **State Management**:

   - The user’s last search (cuisine and email) is stored in DynamoDB.
   - Upon returning to the chat, the chatbot automatically retrieves this state and provides recommendations without requiring new input.

4. **Email Delivery**:
   - The user receives a restaurant recommendation email containing the restaurant name, address, and rating.

---

## Future Enhancements

1. **Enhanced Filtering**:

   - Add the ability to filter restaurants by location or neighborhood.

2. **Frontend Development**:
   - Create a web or mobile application for better user interaction and visual representation of restaurant recommendations.

---

## Author

- Sai Harsha Varma Sangaraju

---

## License

This project is licensed under the MIT License.
