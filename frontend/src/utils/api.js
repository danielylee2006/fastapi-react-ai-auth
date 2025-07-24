//Clerk's React SDK -> custom hook called "useAuth"
//useAuth() -> returns authentication details of current user
import { useAuth } from "@clerk/clerk-react";

//Create Custom hook -> Javascript function that contains other react hooks. 
export const useAPI = () => {
  const { getToken } = useAuth(); //getToken() -> async function that retrieves current user's JWT token

  const makeRequest = async (endpoint, options = {}) => {
    const token = await getToken(); //get user JWT from Clerk

    //Defining default HTTP headers 
    const defaultOptions = {
      headers: {
        "Content-Type": "application/json", //tells the backend the body will be JSON 
        Authorization: `Bearer ${token}`, //standard format for JWT auth headers
      },
    };

    //Sends a Fetch request to the backend
    const response = await fetch(`http://localhost:8000/api${endpoint}`, {
      ...defaultOptions,
      ...options, 
    });

    //checks if the response status_code is valid (not between 200-299)
    if (!response.ok) {

      //parsing error data from the response body as a json
      //if parsing fails (response is not a valid json), return null.
      const errorData = await response.json().catch(() => null);

      if (response.status === 429) { //rate limit status code 
        throw new Error("Daily quota exceeded");
      }

      throw new Error(errorData?.detail || "An error occured");
    }

    return response.json(); //if no errors occurred returns response data as JSON (the actual data frontend will use)
  };

  return { makeRequest }; //return makeRequest function
};
