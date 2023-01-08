Feature: Create counter
    In order to have counters in the app
    As a user
    I want to create a new counter

    Scenario: A private counter
        Given i send a POST request to "/counter/e94b2fe3-bd1e-4d1d-8d98-3d9d7e577623" with body:
            """
            {
                "ownerId": "dbea948b85b94f40a701de0383722af7",
                "private": true
            }
            """
        Then the response status code should be 201