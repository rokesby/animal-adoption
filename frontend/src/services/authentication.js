// docs: https://vitejs.dev/guide/env-and-mode.html
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;
// import getUserById from "../services/users"

export const login = async (email, password) => {
    const payload = {
        email: email,
        password: password,
      }
    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        // Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify(payload),
    };
    
    const response = await fetch(`${BACKEND_URL}/login`, requestOptions);
    if (response.status !== 200) {
      if (response.status == 401)
          throw new Error("Username or Password is incorrect");
      else {
          throw new Error("Unable to fetch user");
      }
    }
  
    const data = await response.json();
    return data;
  };

//   #################

// // services
//   export const login = async (email, password) => {
//     const payload = {
//       email: email,
//       password: password,
//     };
  
//     const requestOptions = {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(payload),
//     };
  
//     const response = await fetch(`${BACKEND_URL}/tokens`, requestOptions);
  
//     const data = await response.json();
  
//     if (response.status === 201) {
//       return data;
//     } else if (response.status === 401) {
//       return data.message;
//     }
//   };

// //   controllers - this is done on the back end
//   const User = require("../models/user");
// const { generateToken } = require("../lib/token");

// const createToken = async (req, res) => {
//   const email = req.body.email;
//   const password = req.body.password;

//   const user = await User.findOne({ email: email });
//   if (!user) {
//     console.log("Auth Error: User not found");
//     res.status(401).json({ message: "User not found" });
//   } else if (user.password !== password) {
//     console.log("Auth Error: Passwords do not match");
//     res.status(401).json({ message: "Password incorrect" });
//   } else {
//     const token = generateToken(user.id);
//     res.status(201).json({ token: token, message: "OK" });
//   }
// };

// const AuthenticationController = {
//   createToken: createToken,
// };

// module.exports = AuthenticationController;