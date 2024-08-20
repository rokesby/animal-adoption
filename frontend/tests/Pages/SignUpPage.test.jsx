import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { vi } from "vitest";
import SignUpPage from "../../src/Pages/SignUpPage/SignUpPage";

// Mocking React Router's useNavigate function
vi.mock("react-router-dom", () => {
  const navigateMock = vi.fn();
  const useNavigateMock = () => navigateMock;
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

  const firstNameInputEl = screen.getByLabelText("First Name");
  const lastNameInputEl = screen.getByLabelText("Last Name");
  const emailInputEl = screen.getByLabelText("Email");
  const passwordInputEl = screen.getByLabelText("Password");
  const confirmPasswordInputEl = screen.getByLabelText("Confirm Password");
  const shelterIDEl = screen.getByLabelText("Shelter ID");
  const submitEl = screen.getByTestId("submit-button");

  await user.type(firstNameInputEl, "Alex");
  await user.type(lastNameInputEl, "Stewart");
  await user.type(emailInputEl, "test@mail.com");
  await user.type(passwordInputEl, "Testing@9");
  await user.type(confirmPasswordInputEl, "Testing@9");
  await user.type(shelterIDEl, "1");
  await user.click(submitEl);
};

describe("Signup Page", () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  test("allows a user to signup", async () => {
    const { signup } = await import("../../src/Services/users.js"); // Use dynamic import
    signup.mockResolvedValue({ token: "mockToken" }); // Mock the resolved value of signup

    render(<SignUpPage />);

    await completeSignupForm();

    expect(signup).toHaveBeenCalledWith({
      first_name: "Alex",
      last_name: "Stewart",
      email: "test@mail.com",
      password: "Testing@9",
      confirmPassword: "Testing@9",
      shelter_id: "1"
    });
  });

  test("navigates to the next page on successful signUp", async () => {
    const { useNavigate } = await import("react-router-dom"); // Ensure useNavigate is correctly imported
    const navigateMock = useNavigate();
    
    const { signup } = await import("../../src/Services/users.js"); // Import signup here too
    signup.mockResolvedValue({ token: "mockToken" }); // Mock the resolved value of signup

    render(<SignUpPage />);

    await completeSignupForm();

    expect(navigateMock).toHaveBeenCalledWith("/create-advert", expect.anything());
  });
});