Feature: Create counter
    As a user
    i want to create a counter

    Scenario: private counter
        Given an user with id 3fa85f64-5717-4562-b3fc-2c963f66afa6
        And a private counter with id dbea948b-85b9-4f40-a701-de0383722af7
        When the user tries to create the counter
        Then the counter is createt as desired