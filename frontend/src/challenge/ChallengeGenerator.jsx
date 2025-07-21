import "react";
import { useState, useEffect } from "react";
import { MCQChallenge } from "./MCQChallenge.jsx"; //child component

export function ChallengeGenerator() {
  const [challenge, setChallenge] = useState(null); //holds challenge object
  const [isLoading, setIsLoading] = useState(false); //tracks whether challenge is being generated
  const [error, setError] = useState(null); //holds errors from api calls
  const [difficulty, setDifficulty] = useState("easy"); //store selected difficulty by user
  const [quota, setQuota] = useState(null); //how many challenges allowed per day

  const fetchQuota = async () => {};
  const generateChallenge = async () => {};
  const getNextResetTime = () => {};

  return (
    <div className="challenge-container">
      <h2> Coding Challenge Generator </h2>

      <div className="quota-display">
        <p>Challenges remaining today: {quota?.quota_remaining || 0}</p>
        {quota?.quota_remaining === 0 && <p>Next reset: {0}</p>}
      </div>

      <div className="difficulty-selector">
        <label htmlFor="difficulty">Select Difficulty</label>
        <select
          id="difficulty"
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          disabled={isLoading}
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>

      <button
        onClick={generateChallenge}
        disabled={isLoading || quota?.quota_remaining === 0}
        className="generate-button"
      >
        {isLoading ? "Generating..." : "Generate Challenge"}
      </button>
      {error && (
        <div className="error-message">
          <p>{error}</p>
        </div>
      )}

      {challenge && <MCQChallenge challenge={challenge} />}
    </div>
  );
}

/* 

This file contains code for the Coding Challenge Generator Component (main page "/")

notes:

- ".?" is optional chaining which is used to access nested properties of an object
without throwing an error if the nested property is null. 

- The "challenges remaining today:" paragraph has a default operator with remaining count and default value of 0.
- There is conditional rendering for "Next Reset". 
    - Only if quote.?quota_remaining is 0 --> render "Next Reset: 0"

-Select drop down element:
    - value={difficulty} binds the drop down selected value as the state variable "difficulty"
    - onChange={(e) => setDifficulty(e.target.value)} 
        1. Event 'e' is passed on when user changes the value of select drop down menu.
        2. e.target.value acesses the changed value
        3. setter method setDifficulty is called to save the changed value in the state variable "difficulty"

    - disabled={isLoading} the select element is disabled when isLoading=True (challenging is loading).

- Button: 
    -button is disabled when the challenge is loading or if the quota remaining = 0.
    -button text is dynamically set in js --> if loading "Generating...", if not "Generate challenge".

-Conditional error rendering below the button: if error exists, output error div element.
*/
