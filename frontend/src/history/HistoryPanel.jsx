import "react";
import { useState, useEffect } from "react";
import { MCQChallenge } from "../challenge/MCQChallenge";

export function HistoryPannel() {
  const [history, setHistory] = useState([]); //array holding past challenges
  const [isLoading, setIsLoading] = useState(true); //tracks whether app is loading/fetching the history
  const [error, setError] = useState(null); //stores error messages when fetching data

  //runs ONCE after the componenet is mount bc dependency array is empty.
  useEffect(() => {
    fetchHistory();
  }, []);

  
  const fetchHistory = async () => {
    setIsLoading(false);
  };

  if (isLoading) {
    return <div className="loading">Loading history...</div>;
  }

  if (error) {
    return (
      <div className="error-message">
        <p>{error}</p>
        <button onClick={fetchHistory}>Retry</button>
      </div>
    );
  }

  return (
    <div className="history-panel">
      <h2>History</h2>
      {history.length === 0 ? (
        <p>No challenge history</p>
      ) : (
        <div className="history-list">
          {history.map((challenge) => {
            return (
              <MCQChallenge
                challenge={challenge}
                key={challenge.id}
                showExplanation
              />
            );
          })}
        </div>
      )}
    </div>
  );
}
