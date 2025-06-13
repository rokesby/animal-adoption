import { useState, useEffect, createContext, useContext } from "react";
import {
  loginService,
  logoutService,
  refreshToken,
  signupService,
} from "../../services/authService";
import { jwtDecode } from "jwt-decode";

const AuthContext = createContext(null);

const AuthProvider = ({ children }) => {
  const [token, setToken] = useState();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  // initAuth will run on mount
  useEffect(() => {
    const initAuth = async () => {
      try {
        console.log('useEffect attempt to refresh token')
        await handleRefreshToken();
      } catch (error) {
        console.error("Failed to initialize auth", error);
        setIsAuthenticated(false);
      } finally {
        setIsLoading(false);
        console.log("initAuth has finished");
      }
    };

    initAuth();
  }, []);

  const isTokenExpired = async (token) => {
    // if there isn't a token, return true
    if (!token) return true;
    try {
      // if there is a token, decode the token and check whether it has expired (30 seconds or less left)
      const decoded = jwtDecode(token);
      const isExpired = decoded.exp * 1000 < Date.now() - 30000;
      return isExpired;
    } catch (error) {
      return true;
    }
  };

  const handleRefreshToken = async () => {
    if (refreshing == true) return false;

    try {
      setRefreshing(true);
      console.log("attempting to refresh token");
      const data = await refreshToken();
      if (data && data.token) {
        setToken(data.token);
        setIsAuthenticated(true);
        const newAccessToken = data.token
        return newAccessToken;
      } else {
        console.error('token refresh failed - no token returned');
        setIsAuthenticated(false);
        return false;
      }
    } catch (error) {
      console.error("Token refresh error:", error);
      setIsAuthenticated(false);
      return false;
    } finally {
      console.info('refreshing finished')
      setRefreshing(false);
    }
  };

  const handleLogin = async (email, password) => {
    try {
      console.log("attempting login...");
      const data = await loginService(email, password);
      if (data && data.token) {
        setToken(data.token);
        setIsAuthenticated(true);
        return true;
      }
      return false;
    } catch (error) {
      setIsAuthenticated(false);
      return false;
    }
  };

  const handleSignUp = async (formData) => {
    try {
      console.log("attempting sign up...");
      const data = await signupService(formData);
      if (data && data.token) {
        console.log("Sign Up successful");
        setToken(data.token);
        setIsAuthenticated(true);
        return true;
      }
      return false;
    } catch (error) {
      console.error("sign up error", error);
      setIsAuthenticated(false);
      return false;
    }
  };

  const handleLogout = async () => {
    try {
      await logoutService();
      setToken(null);
      setIsAuthenticated(false);
      navigate("/login");
      return true;
    } catch (error) {
      return false;
    }
  };

  const authFetch = async (url, options = {}) => {
    if (isTokenExpired(token) == true) {
      console.log("Token expired, attempting refresh before fetch");
      await handleRefreshToken();
    }

    try {
      // make the request using the current token
      const authOptions = {
        ...options,
        headers: {
          ...options.headers,
          Authorization: `Bearer ${token}`,
        },
      };
      // fetch url passed in, with options passed in AND addition of token
      const response = await fetch(url, authOptions);

      if (response.status === 401) {
        console.log("Receved 401 from fetch, attempting token refresh");

        const refreshed_token = await handleRefreshToken();
        // if refreshed is True - update the authHeaders with token
        if (refreshed_token) {
          authOptions.headers.Authorization = `Bearer ${refreshed_token}`;
          return fetch(url, authOptions);
        } else {
          console.log("Token refresh failed after 401");
          throw new Error("Session expired");
        }
      }
      return response;
    } catch (error) {
      console.error("Auth fetch error:", error);
      throw error;
    }
  };

  const contextValue = {
    token,
    isAuthenticated,
    isLoading,
    signup: handleSignUp,
    login: handleLogin,
    logout: handleLogout,
    authFetch: authFetch,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {!isLoading && children}
    </AuthContext.Provider>
  );
};

const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export { AuthProvider, useAuth };
