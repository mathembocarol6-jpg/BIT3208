package com.quantstore.foundation;

public class MainApplication {
    public static void main(String[] args) {
        String testUsername = "JohnDoe26";
        String testEmail = "johndoe@yahoo.com";
        String testPassword = "J@Doe#6";

        System.out.println("--- Starting Form Validation ---");
        
        boolean isFormValid = true;

        if (!FormValidator.validateUsername(testUsername)) {
            System.out.println("Validation Error: Username must be 3-20 alphanumeric characters.");
            isFormValid = false;
        }

        if (!FormValidator.validateEmail(testEmail)) {
            System.out.println("Validation Error: Invalid email format syntax.");
            isFormValid = false;
        }

        if (!FormValidator.validatePassword(testPassword)) {
            System.out.println("Validation Error: Password must be at least 8 characters long and contain 1 uppercase letter, 1 lowercase letter, and 1 number.");
            isFormValid = false;
        }

        if (isFormValid) {
            System.out.println("Form Verification Status: SUCCESS");
            UserRepository repo = new UserRepository();
            boolean isRegistered = repo.registerUser(testUsername, testEmail, testPassword);
            System.out.println("Database Execution Status: " + isRegistered);
        } else {
            System.out.println("Form Verification Status: FAILED. Database pipeline aborted.");
        }
    }
}