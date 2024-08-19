import React from 'react'; 
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useNavigate } from "react-router-dom";
import { vi } from 'vitest';

import SignUpPage from "../../src/Pages/SignUpPage/SignUpPage";

// Mocking React Router's useNavigate function
vi.mock("react-router-dom", () => {
  const navigateMock = vi.fn();
  const useNavigateMock = () => navigateMock; // Create a mock function for useNavigate
  return { useNavigate: useNavigateMock };
});

// Mocking the signup service
vi.mock("../../src/Services/users.js", () => {
  const signupMock = vi.fn();
  return { signup: signupMock };
});

// Reusable function for filling out signup form
const completeSignupForm = async () => {
  const user = userEvent.setup();

  const firstNameInputEl = screen.getByLabelText(/first name/i);
  const lastNameInputEl = screen.getByLabelText(/last name/i);
  const emailInputEl = screen.getByLabelText(/email/i);
  const passwordInputEl = screen.getByLabelText(/password/i);
  const confirmPasswordInputEl = screen.getByLabelText(/confirm password/i);
  const submitButtonEl = screen.getByRole("button", { name: /submit/i });

  await user.type(firstNameInputEl, "Alex");
  await user.type(lastNameInputEl, "Stewart");
  await user.type(emailInputEl, "test@mail.com");
  await user.type(passwordInputEl, "Testing@9");
  await user.type(confirmPasswordInputEl, "Testing@9");
  await user.click(submitButtonEl);
};

describe("SignUp Page", () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  test("allows a user to signup", async () => {
    const { signup } = require("../../src/Services/users.js");
    render(<SignUpPage />);

    await completeSignupForm();

    expect(signup).toHaveBeenCalledWith({
      first_name: "Alex",
      last_name: "Stewart",
      email: "test@mail.com",
      password: "Testing@9",
      confirmPassword: "Testing@9",
      shelter_id: ""  // Ensure all fields match your formData state
    });
  });

  test("navigates to next page on successful signUp", async () => {
    render(<SignUpPage />);

    const navigateMock = useNavigate();

    await completeSignupForm();

    expect(navigateMock).toHaveBeenCalledWith("/create-advert", expect.anything());
  });

  // test("navigates to signup page unsuccessfull", async () => {
  //   render(<SignUpPage />);

  //   const { signup } = require("../../src/Services/users.js");
  //   signup.mockRejectedValue(new Error("Error signing up"));
  //   const navigateMock = useNavigate();

  //   await completeSignupForm();

  //   expect(navigateMock).toHaveBeenCalledWith("/signup");
  // });
});